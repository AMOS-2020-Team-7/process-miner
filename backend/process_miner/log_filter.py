"""
Module used for filtering irrelevant log entries.
"""
import logging
import re
from typing import List, Dict

log = logging.getLogger(__name__)


class LogFilter:
    """
    Class used for removing log entries that do not add any value to the data
    generated during process mining.
    """
    def __init__(self, required_fields: List[str], filter_field: str,
                 filter_expressions: List[str]):
        self.required_fields = required_fields
        self.filter_field = filter_field
        self.patterns = [re.compile(expr) for expr in filter_expressions]

    def __str__(self):
        return f'{self.__class__.__name__} [' \
               f'required_fields <{self.required_fields}>, ' \
               f'filter_field <{self.filter_field}>, ' \
               f'patterns <{self.patterns}>]'

    def filter_log_entries(self, entries: List[Dict[str, str]]):
        """
        Filters the supplied log entries by checking for missing required
        fields or matching filter expressions.
        :param entries: list of log entries that should be filtered
        """
        for entry in entries.copy():
            if entry not in entries:
                continue
            if not self._required_fields_present(entry):
                log.debug('removing incomplete entry %s', entry)
                entries.remove(entry)
            elif self._entry_matches_filter_expressions(entry):
                log.debug('removing filtered entry %s', entry)
                entries.remove(entry)

    def _required_fields_present(self, entry: Dict[str, str]) -> bool:
        for field in self.required_fields:
            if field not in entry.keys() or not entry[field]:
                log.debug('missing/empty required field "%s" for entry %s',
                          field, entry)
                return False

        return True

    def _entry_matches_filter_expressions(self, entry: Dict[str, str]):
        for pattern in self.patterns:
            filter_target_field = entry[self.filter_field]
            if pattern.search(filter_target_field):
                log.debug('pattern "%s" matches field "%s" on entry %s',
                          pattern.pattern, self.filter_field, entry)
                return True

        return False
