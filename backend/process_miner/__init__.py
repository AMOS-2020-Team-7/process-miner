"""
Module responsible for initializing the flask app that provides the backend
service of the process miner.
"""
import logging
from pathlib import Path

from flask import Flask

from process_miner.configuration_loader import ConfigurationLoader
from process_miner.log_retriever import LogRetriever

CONFIG_FILENAME = 'process_miner_config.yaml'

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

log.info('setting up configuration')
cfg_loader = ConfigurationLoader(Path(CONFIG_FILENAME))
global_cfg = cfg_loader.get_section('global')
log_retriever_cfg = cfg_loader.get_section('log_retriever')

log.info('setting up log retriever')
retriever = LogRetriever(log_retriever_cfg['url'],
                         log_retriever_cfg['api_token'],
                         global_cfg['log_directory']
                         )

log.info('setting up flask app')
process_miner_app = Flask(__name__)


@process_miner_app.route('/logs/refresh')
def refresh_logs():
    """
    Triggers the retrieval of logs from Graylog.
    """
    #  TODO CPU intensive tasks should be executed asynchronously but this will
    #   do for now as this just serves as an example endpoint
    retriever.retrieve_logs()
    return 'Done'


def create_app():
    """
    Factory method for creating the Flask object representing the actual
    flask app.
    :return: the Flask object
    """
    return process_miner_app
