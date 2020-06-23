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
        if 'mappings' in config:
            for (label, expressions) in config['mappings'].items():
                tagger.add_mapping(label, expressions)
        # add all extractors to the tagger
        if 'extractors' in config:
            for pattern in config['extractors']:
                tagger.add_extractor(pattern)

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
        self.extractors = list()
        self.mappings = dict()

    def __str__(self):
        return f'{self.__class__.__name__} [' \
               f'source_field <{self.source_field}>, ' \
               f'target_field <{self.target_field}>, ' \
               f'tag_all <{self.tag_all}>, ' \
               f'default_value <{self.default_value}>, ' \
               f'extractors <{self.extractors}>]' \
               f'mappings <{self.mappings}>]'

    def add_mapping(self, value: str, expressions: List[str]) -> None:
        """
        Adds a mapping from a tag field value to one or more RegEx.
        :param value: value that should be inserted into field if any of the
        RegEx match the source field.
        :param expressions: expressions that used to determine if the supplied
        value should be added to the target field.
        """
        self.mappings[value] = [re.compile(expr) for expr in expressions]

    def add_extractor(self, pattern: str):
        """
        Adds an extractor pattern to the LogTagger. The pattern has to contain
        at least one capture group. In case there are more than one group only
        the first group will be used to extract values from the source field.
        :param pattern: the pattern
        """
        pattern = re.compile(pattern)
        if not pattern.groups:
            log.warning('pattern "%s" contains no groups and will be ignored',
                        pattern.pattern)
            return
        if pattern.groups > 1:
            log.warning('pattern "%s" contains more than one group -> '
                        'only first group will be used', pattern.pattern)
        self.extractors.append(pattern)

    def tag_entries(self, entries: List[Dict[str, str]]) -> None:
        """
        Processes log entries and adds values to the target field if one of
        the patterns matches or one of the extractors was able to capture a
        value on its first capture group.
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
        source_field_content = entry[self.source_field]
        # try to find a static mapping
        tag_value = self._calculate_mapped_tag_value(source_field_content)
        if tag_value:
            log.debug('found mapping "%s" in value "%s" of field "%s"',
                      tag_value, source_field_content, self.source_field)
            return tag_value
        # try to extract values via available extractor patterns
        tag_value = self._calculate_extracted_tag_value(source_field_content)
        if tag_value:
            log.debug('extracted tag "%s" from value "%s" of field "%s"',
                      tag_value, source_field_content, self.source_field)
            return tag_value

        log.debug('no matching tag value for field "%s" found on entry "%s"',
                  self.target_field, entry)
        return None

    def _calculate_mapped_tag_value(self, field_value):
        for label, patterns in self.mappings.items():
            for pattern in patterns:
                if pattern.search(field_value):
                    return label
        return None

    def _calculate_extracted_tag_value(self, field_value):
        for extractor in self.extractors:
            match = extractor.search(field_value)
            if match:
                return match.group(1)
        return None

    def _tag_all_entries(self, label, log_entries):
        log.debug('tagging all entries with value "%s" on field "%s"', label,
                  self.target_field)
        for entry in log_entries:
            entry[self.target_field] = label
