"""
Module responsible for initializing the flask app that provides the backend
service of the process miner.
"""
import logging
from pathlib import Path

from flask import Flask
from flask_caching import Cache
from flask_cors import CORS

import process_miner.configuration_loader as cl
import process_miner.graylog_access as ga
import process_miner.log_retriever as lr
import process_miner.log_tagger as lt
import process_miner.logs_process_miner as pm
import process_miner.mining.graph_factory as gf
import process_miner.mining.metadata_factory as mf
from process_miner.access.blueprints import logs, request_result, graphs, \
                                            metadata
from process_miner.access.work.request_processing import RequestManager

CONFIG_FILENAME = 'process_miner_config.yaml'

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def setup_components(config_file=CONFIG_FILENAME):
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

    log.info('setting up graph factory')
    graph_factory = gf.GraphFactory(Path(global_cfg['log_directory']))

    log.info('setting up metadata factory')
    metadata_factory = mf.MetadataFactory(Path(global_cfg['log_directory']))

    miner = pm.Miner(global_cfg['graph_directory'])
    return retriever, graph_factory, metadata_factory, miner


def create_app():
    """
    Factory method for creating the Flask object representing the actual
    flask app.
    :return: the Flask object
    """
    (retriever, graph_factory, metadata_factory, _) = setup_components()
    log.info('setting up flask app')
    process_miner_app = Flask(__name__)
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
        graphs.create_blueprint(request_manager, cache, graph_factory),
        metadata.create_blueprint(request_manager, cache, metadata_factory)
    ]
    # register created blueprints on the flask app
    for blueprint in used_blueprints:
        process_miner_app.register_blueprint(blueprint)

    return process_miner_app
