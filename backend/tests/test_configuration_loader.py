"""
Tests for the configuration_loader module
"""
import pytest

from process_miner.configuration_loader import ConfigurationLoader

FILE_CONTENT = '''section1:
  key1: value1
  key2: value2
section2:
'''


def _create_test_config(tmpdir):
    config_file = tmpdir.join("config.yaml")
    config_file.write(FILE_CONTENT)
    return config_file


def _create_loader(tmpdir):
    config_file = _create_test_config(tmpdir)
    return ConfigurationLoader(config_file)


def test_get_section_missing(tmpdir):
    """
    Checks if the appropriate error is raised if section is not present.
    """
    cfg = _create_loader(tmpdir)
    with pytest.raises(KeyError):
        cfg.get_section('missing section')


def test_get_section_valid_section(tmpdir):
    """
    Checks if sections are read correctly.
    """
    cfg = _create_loader(tmpdir)
    assert cfg.get_section('section1') == {'key1': 'value1', 'key2': 'value2'}
    assert not cfg.get_section('section2')


def test_get_entry_missing_section(tmpdir):
    """
    Checks if the appropriate error is raised if section is missing.
    """
    cfg = _create_loader(tmpdir)
    with pytest.raises(KeyError):
        cfg.get_entry('missing section', 'value')


def test_get_entry_missing_key(tmpdir):
    """
    Checks if the appropriate error is raised if entry key is missing.
    """
    cfg = _create_loader(tmpdir)
    with pytest.raises(KeyError):
        cfg.get_entry('section2', 'missing key')


def test_get_entry_valid_section(tmpdir):
    """
    Checks if a valid entry gets read correctly.
    """
    cfg = _create_loader(tmpdir)
    assert cfg.get_section('section1') == {'key1': 'value1', 'key2': 'value2'}
    assert not cfg.get_section('section2')


def test_reload_config(tmpdir):
    """
    Checks if config gets reloaded correctly.
    """
    config_path = _create_test_config(tmpdir)
    cfg = ConfigurationLoader(config_path)
    assert cfg.get_entry('section1', 'key1') == 'value1'
    new_content = FILE_CONTENT.replace('value1', 'modified value1')
    config_path.write(new_content)
    cfg.reload_config()
    assert cfg.get_entry('section1', 'key1') == 'modified value1'
