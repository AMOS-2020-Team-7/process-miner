import logging

from process_miner.log_retriever import LogRetriever
from process_miner.process_miner_config import log_retriever as log_retriever_cfg

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    log.info("process miner backend started")

    log_retriever = LogRetriever(log_retriever_cfg["url"], log_retriever_cfg["api_token"],
                                 log_retriever_cfg["target_dir"])
    log_retriever.retrieve_logs()


if __name__ == '__main__':
    main()
