"""
Main module of the process miner package used to start the process miner.
"""
import logging

from process_miner import setup_components
from process_miner.log_importer import concat_files

log = logging.getLogger(__name__)


def _main():
    (retriever) = setup_components()
    log.info('starting log retrieval')
    retriever.retrieve_logs()
    concat_files()



if __name__ == '__main__':
    _main()
