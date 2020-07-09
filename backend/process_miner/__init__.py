"""
Module responsible for initializing the flask app that provides the backend
service of the process miner.
"""
import logging
from pathlib import Path

from flasgger import Swagger
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS

import process_miner.configuration_loader as cl
import process_miner.log_handling.graylog_access as ga
import process_miner.log_handling.log_retriever as lr
import process_miner.log_handling.log_tagger as lt
import process_miner.mining.dataset_factory as dsf
from process_miner.access.blueprints import logs, request_result, graphs, \
    metadata
from process_miner.access.work.request_processing import RequestManager

_DEFAULT_CONFIG_FILE = 'process_miner_config.yaml'

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def setup_components(config_file=_DEFAULT_CONFIG_FILE):
    """
    Sets up all components needed for running the process miner.
    :param config_file: path to the configuration file that should be used
    :return: a tuple containing the fully set up components of the process
    miner backend
    """
    log.info('setting up configuration')
    cfg_loader = cl.ConfigurationLoader(Path(config_file))
    global_cfg = cfg_loader.get_section('global')
    log_retriever_cfg = cfg_loader.get_section('log_retriever')
    filter_cfg = cfg_loader.get_section('filters')
    tag_cfg = cfg_loader.get_section('tags')

    log.info('setting up Graylog access')
    graylog = ga.GraylogAccess(log_retriever_cfg['url'],
                               log_retriever_cfg['api_token'])

    log.info('setting up log taggers')
    taggers = lt.create_log_taggers(tag_cfg)

    log.info('setting up log retriever')
    retriever = lr.LogRetriever(graylog,
                                global_cfg['log_directory'],
                                filter_cfg['filter_expressions'],
                                taggers)

    log.info('setting up metadata factory')
    dataset_factory = dsf.DatasetFactory(Path(global_cfg['log_directory']))

    return cfg_loader, retriever, dataset_factory


def create_app():
    """
    Factory method for creating the Flask object representing the actual
    flask app.
    :return: the Flask object
    """
    (_, retriever, dataset_factory) = setup_components()
    log.info('setting up flask app')
    process_miner_app = Flask(__name__)
    Swagger(process_miner_app)
    # TODO create that url dynamically
    log.info('SwaggerUI reachable at http://localhost:5000/apidocs/index.html')
    # enable cross origin resource sharing
    # TODO evaluate if this is required in the final application
    CORS(process_miner_app)
    log.info('setting up cache')
    cache = Cache(process_miner_app, config={'CACHE_TYPE': 'simple'})
    log.info('linking request manager to flask app')
    request_manager = RequestManager(process_miner_app)

    # create all required blueprints
    used_blueprints = [
        request_result.create_blueprint(request_manager),
        logs.create_blueprint(request_manager, cache, retriever),
        graphs.create_blueprint(request_manager, cache, dataset_factory),
        metadata.create_blueprint(request_manager, cache, dataset_factory)
    ]
    # register created blueprints on the flask app
    for blueprint in used_blueprints:
        process_miner_app.register_blueprint(blueprint)

    log.info('updating log storage contents')
    retriever.retrieve_logs()

    return process_miner_app
