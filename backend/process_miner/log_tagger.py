"""
Module used to add new fields to log entries based on existing fields.
"""
import logging
import re
from distutils.util import strtobool
from typing import Dict, List

log = logging.getLogger(__name__)


def create_log_taggers(cfg):
    """
    Factory method for creating LogTaggers from a configuration.
    :param cfg: configuration containing the settings
    :return: list containing the created taggers
    """
    taggers = []
    for tag, config in cfg.items():
        # allow bool and str in 'tag_all' value
        tag_all = strtobool(str(config['tag_all']))
        tagger = LogTagger(config['source'], tag, tag_all,
                           config['default_value'])
        # add all mappings to the tagger
        for (label, expressions) in config['mappings'].items():
            tagger.add_mapping(label, expressions)

        taggers.append(tagger)
    return taggers


class LogTagger:
    """
    Class that handles creation of a single log entry field based on values
    from an existing field.
    """
    def __init__(self, source_field: str, target_field: str, tag_all: bool,
                 default_value=''):
        self.source_field = source_field
        self.target_field = target_field
        self.tag_all = tag_all
        self.default_value = default_value
        self.mapping = dict()

    def __str__(self):
        return f'{self.__class__.__name__} [' \
               f'source_field <{self.source_field}>, ' \
               f'target_field <{self.target_field}>, ' \
               f'tag_all <{self.tag_all}>, ' \
               f'default_value <{self.default_value}>, ' \
               f'mapping <{self.mapping}>]'

    def add_mapping(self, value: str, expressions: List[str]) -> None:
        """
        Adds a mapping from a tag field value to one or more RegEx.
        :param value: value that should be inserted into field if any of the
        RegEx match the source field.
        :param expressions: expressions that used to determine if the supplied
        value should be added to the target field.
        """
        self.mapping[value] = [re.compile(expr) for expr in expressions]

    def tag_entries(self, entries: List[Dict[str, str]]) -> None:
        """
        Processes log entries and adds values to the target field if one of
        their respective patterns matches.
        :param entries: a list of log entries
        """
        for entry in entries:
            label = self._get_tag_value(entry)

            if label and self.tag_all:
                self._tag_all_entries(label, entries)
                return

            if label:
                entry[self.target_field] = label
            else:
                entry[self.target_field] = self.default_value

    def _get_tag_value(self, entry) -> str:
        for label, patterns in self.mapping.items():
            for pattern in patterns:
                source_field_content = entry[self.source_field]
                if pattern.search(source_field_content):
                    log.debug('matched "%s" in field "%s" with value "%s"',
                              pattern.pattern, self.source_field,
                              source_field_content)
                    return label
        log.debug('no matching tag value for field "%s" found on entry "%s"',
                  self.target_field, entry)
        return None

    def _tag_all_entries(self, label, log_entries):
        log.debug('tagging all entries with value "%s" on field "%s"', label,
                  self.target_field)
        for entry in log_entries:
            entry[self.target_field] = label
