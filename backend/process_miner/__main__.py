"""
Main module of the process miner package used to start the process miner.
"""
import logging

from process_miner import setup_components
from process_miner.logs_process_miner import create_results

log = logging.getLogger(__name__)

# embedded, redirect, OAuth, Decoupled, all, not available
APPROACH = "embedded"


def _main():
    retriever = setup_components()
    log.info('starting log retrieval')
    retriever.retrieve_logs()
    create_results(APPROACH)


if __name__ == '__main__':
    _main()
