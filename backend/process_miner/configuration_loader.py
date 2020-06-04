"""
Module for loading configuration files
"""
import logging
from pathlib import Path

import yaml

log = logging.getLogger(__name__)


def _load_config(path: Path):
    log.info('loading config from %s', path)
    with path.open('r') as cfg_file:
        return yaml.safe_load(cfg_file)


class ConfigurationLoader:
    """
    Class for loading and accessing configuration files
    Supported formats:

    - YAML
    """
    def __init__(self, path: Path):
        self.path = path
        self.cfg = _load_config(path)

    def get_section(self, section: str):
        """
        Gets section of config file.
        :param section: name of the section
        :return: dictionary containing contents of the section
        """
        return self.cfg[section]

    def get_entry(self, section: str, name: str):
        """
        Gets the value of an entry from the config file.
        :param section: name of the section the entry is located in
        :param name: name of the entry
        :return: value of the entry
        """
        return self.cfg[section][name]

    def reload_config(self):
        """
        Reloads the config file from disk.
        """
        self.cfg = _load_config(self.path)
