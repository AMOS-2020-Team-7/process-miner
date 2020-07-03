"""
Tests for the log_tagger module
"""
import copy

from process_miner.log_handling.log_tagger import LogTagger

DEFAULT_VALUE = 'default'


def _create_single_tagger():
    tagger_single = LogTagger('source', 'target_single', False, DEFAULT_VALUE)
    tagger_single.add_mapping('single_tagger_value',
                              [
                                  'single'
                              ])
    return tagger_single


def _create_all_tagger():
    tagger_all = LogTagger('source', 'target_all', True, DEFAULT_VALUE)
    tagger_all.add_mapping('all_tagger_value',
                           [
                               'all'
                           ])
    return tagger_all


def _create_extractor_tagger():
    tagger_extract = LogTagger('source', 'target_extract', True, DEFAULT_VALUE)
    tagger_extract.add_extractor('value=(\\d+)')
    return tagger_extract


def _tag_entries(entries, taggers):
    for tagger in taggers:
        tagger.tag_entries(entries)


def test_tag_entries_no_matches():
    """
    Checks if default values get inserted properly if no entry matches.
    """
    entries = [
        {'unrelated_field': 'value', 'source': 'some value'},
        {'unrelated_field': 'value', 'source': 'another value'}
    ]

    expected_entries = copy.deepcopy(entries)
    for entry in expected_entries:
        entry['target_single'] = DEFAULT_VALUE

    _create_single_tagger().tag_entries(entries)

    assert entries == expected_entries


def test_tag_entries_single_matches():
    """
    Checks if single entry matcher inserts its values properly
    """
    entries = [
        {'unrelated_field': 'value', 'source': 'single'},
        {'unrelated_field': 'value', 'source': 'sing but no le'}
    ]

    expected_entries = copy.deepcopy(entries)
    expected_entries[0]['target_single'] = 'single_tagger_value'
    expected_entries[1]['target_single'] = DEFAULT_VALUE

    _create_single_tagger().tag_entries(entries)

    assert entries == expected_entries


def test_tag_entries_all_matches():
    """
    Checks if all entries get tagged properly if tag_all was enabled.
    """
    entries = [
        {'unrelated_field': 'value', 'source': 'all'},
        {'unrelated_field': 'value', 'source': 'some'}
    ]

    expected_entries = copy.deepcopy(entries)
    for entry in expected_entries:
        entry['target_all'] = 'all_tagger_value'

    _create_all_tagger().tag_entries(entries)

    assert entries == expected_entries


def test_tag_entries_extract():
    """
    Checks if all entries get tagged properly if tag_all was enabled.
    """
    entries = [
        {'unrelated_field': 'value', 'source': 'some'},
        {'unrelated_field': 'value', 'source': 'another'},
        {'unrelated_field': 'value', 'source': 'value=123456'}
    ]

    expected_entries = copy.deepcopy(entries)
    for entry in expected_entries:
        entry['target_extract'] = '123456'

    _create_extractor_tagger().tag_entries(entries)

    assert entries == expected_entries
