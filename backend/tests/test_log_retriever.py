"""
Tests for log_retriever module
"""
import os
from csv import DictReader

from process_miner import log_retriever
from process_miner.log_retriever import LogRetriever


def test___str___token_is_redacted():
    """
    Checks if token is redacted in string representation of LogRetriever
    object.
    """
    token = 'token123'
    retriever = LogRetriever('test_url', token, 'directory')
    assert token not in retriever.__str__()


def test_retrieve_logs_no_new_logs(tmp_path, requests_mock):
    """
    Check target directory remains empty if there are no new log entries.
    """
    test_url = 'http://test.test'
    requests_mock.get(f'{test_url}/api/search/universal/absolute/export',
                      text='')
    log_directory = tmp_path / 'retrieved_logs'
    retriever = LogRetriever(test_url, 'token', log_directory)
    retriever.retrieve_logs()
    assert len(os.listdir(log_directory)) == 0


def test_retrieve_logs_consecutive_requests(tmp_path, requests_mock):
    """
    Check if log entries get stored correctly during two consecutive retrieval
    processes.
    """
    test_url = 'http://test.test'
    requests_mock.get(f'{test_url}/api/search/universal/absolute/export',
                      text='''timestamp,correlationId,message
2020-01-01T01:00:02.000Z,1,message2
2020-01-01T01:00:01.000Z,2,message1
2020-01-01T01:00:00.000Z,1,message0
2020-01-01T01:00:03.000Z,2,message3
''')
    log_directory = tmp_path / 'retrieved_logs'
    retriever = LogRetriever(test_url, 'token', log_directory)
    retriever.retrieve_logs()

    #  number of files and last retrieved timestamp after first request
    assert len(os.listdir(log_directory)) == 3
    timestamp_file_path = log_directory / log_retriever.TIMESTAMP_FILENAME
    with timestamp_file_path.open('r') as timestamp_file:
        assert timestamp_file.readline() == '2020-01-01T01:00:03.000Z'
    #  file with correlationId 1
    file1 = log_directory / '2020-01-01T01_00_00.000Z_1.csv'
    with file1.open('r') as csv_file_2:
        reader = DictReader(csv_file_2)
        assert reader.fieldnames == ['timestamp', 'correlationId',
                                     'message', 'approach', 'consent']
        rows = list(reader)
        assert rows[0]['timestamp'] == '2020-01-01T01:00:00.000Z'
        assert rows[0]['correlationId'] == '1'
        assert rows[0]['message'] == 'message0'
        assert rows[1]['timestamp'] == '2020-01-01T01:00:02.000Z'
        assert rows[1]['correlationId'] == '1'
        assert rows[1]['message'] == 'message2'
    #  file with correlationId 2
    file2 = log_directory / '2020-01-01T01_00_01.000Z_2.csv'
    with file2.open('r') as csv_file_2:
        reader = DictReader(csv_file_2)
        assert reader.fieldnames == ['timestamp', 'correlationId',
                                     'message', 'approach', 'consent']
        rows = list(reader)
        assert rows[0]['timestamp'] == '2020-01-01T01:00:01.000Z'
        assert rows[0]['correlationId'] == '2'
        assert rows[0]['message'] == 'message1'
        assert rows[1]['timestamp'] == '2020-01-01T01:00:03.000Z'
        assert rows[1]['correlationId'] == '2'
        assert rows[1]['message'] == 'message3'

    requests_mock.get(f'{test_url}/api/search/universal/absolute/export',
                      text='''timestamp,correlationId,message
2020-01-01T01:01:04.000Z,3,message4
2020-01-01T01:01:05.000Z,3,message5
    ''')
    retriever.retrieve_logs()
    #  number of files and last retrieved timestamp after second request
    assert len(os.listdir(log_directory)) == 4
    with timestamp_file_path.open('r') as timestamp_file:
        assert timestamp_file.readline() == '2020-01-01T01:01:05.000Z'
    #  file with correlationId 3
    file3 = log_directory / '2020-01-01T01_01_04.000Z_3.csv'
    with file3.open('r') as csv_file_3:
        reader = DictReader(csv_file_3)
        assert reader.fieldnames == ['timestamp', 'correlationId',
                                     'message', 'approach', 'consent']
        rows = list(reader)
        assert rows[0]['timestamp'] == '2020-01-01T01:01:04.000Z'
        assert rows[0]['correlationId'] == '3'
        assert rows[0]['message'] == 'message4'
        assert rows[1]['timestamp'] == '2020-01-01T01:01:05.000Z'
        assert rows[1]['correlationId'] == '3'
        assert rows[1]['message'] == 'message5'
