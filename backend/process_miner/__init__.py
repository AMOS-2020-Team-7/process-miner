"""
Module responsible for initializing the flask app that provides the backend
service of the process miner.
"""
import logging

from flask import Flask

from process_miner.log_retriever import LogRetriever
from .process_miner_config import log_retriever as log_retriever_cfg

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)
log.info("setting up log retriever")
retriever = LogRetriever(log_retriever_cfg["url"],
                         log_retriever_cfg["api_token"],
                         log_retriever_cfg["target_dir"]
                         )

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
    flask app
    :return: the Flask object
    """
    return process_miner_app
