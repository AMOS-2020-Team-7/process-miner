"""
Module responsible for initializing the flask app that provides the backend
service of the process miner.
"""
import logging
import os
import threading
import time
from pathlib import Path

from flasgger import Swagger
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from numpy.compat import os_PathLike

import process_miner.configuration_loader as cl
import process_miner.log_handling.graylog_access as ga
import process_miner.log_handling.log_retriever as lr
import process_miner.log_handling.log_tagger as lt
import process_miner.mining.dataset_factory as dsf
from process_miner.access.blueprints import logs, request_result, graphs, \
    metadata
from process_miner.access.work.request_processing import RequestManager

_DEFAULT_CONFIG_FILE = 'process_miner_config.yaml'
_DEFAULT_LOG_RETR_CONFIG_FILE = 'log_retriever_config.yaml'

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def setup_components(process_miner_config_file=_DEFAULT_CONFIG_FILE,
                     log_retriever_config_file=_DEFAULT_LOG_RETR_CONFIG_FILE):
    """
    Sets up all components needed for running the process miner.
    :param process_miner_config_file: path to the configuration file that
    should be used
    :param log_retriever_config_file: path to the log retriever configuration
    file that should be used (setting API token and URL via environment is
    preferred)
    :return: a tuple containing the fully set up components of the process
    miner backend
    """
    log.info('setting up configuration')
    pm_cfg_loader = cl.ConfigurationLoader(Path(process_miner_config_file))
    global_cfg = pm_cfg_loader.get_section('global')
    filter_cfg = pm_cfg_loader.get_section('filters')
    tag_cfg = pm_cfg_loader.get_section('tags')

    log.info('setting up Graylog access')
    if os.environ.get('GRAYLOG_URL') and os.environ.get('GRAYLOG_API_TOKEN'):
        graylog_url = os.environ.get('GRAYLOG_URL')
        api_token = os.environ.get('GRAYLOG_API_TOKEN')
    else:
        log.warning('Graylog URL and API token not provided via environment. '
                    'Trying to read credentials from file %s',
                    log_retriever_config_file)
        lr_cfg_loader = cl.ConfigurationLoader(Path(log_retriever_config_file))
        log_retriever_cfg = lr_cfg_loader.get_section('log_retriever')
        graylog_url = log_retriever_cfg['url']
        api_token = log_retriever_cfg['api_token']
    graylog = ga.GraylogAccess(graylog_url, api_token)

    log.info('setting up log taggers')
    taggers = lt.create_log_taggers(tag_cfg)

    log.info('setting up log retriever')
    retriever = lr.LogRetriever(graylog,
                                global_cfg['log_directory'],
                                filter_cfg['filter_expressions'],
                                taggers)

    log.info('setting up metadata factory')
    dataset_factory = dsf.DatasetFactory(Path(global_cfg['log_directory']))

    return pm_cfg_loader, retriever, dataset_factory


def create_app():
    """
    Factory method for creating the Flask object representing the actual
    flask app.
    :return: the Flask object
    """
    (cfg, retriever, dataset_factory) = setup_components()
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

    # set up periodic log retrieval
    def _periodic_log_refresh():
        try:
            sleep_interval = 60 * int(cfg.get_entry('global',
                                                    'reload_interval'))
        except KeyError:
            sleep_interval = 60 * 60
            log.info('reload interval not set; using default: %sm',
                     sleep_interval)
        if sleep_interval <= 0:
            log.info('automatic log retrieval disabled')
            return
        while True:
            retriever.retrieve_logs()
            time.sleep(sleep_interval)
    log.info('setting up periodic log retrieval')
    log_reload_thread = threading.Thread(target=_periodic_log_refresh)
    log_reload_thread.daemon = True
    log_reload_thread.start()

    return process_miner_app
