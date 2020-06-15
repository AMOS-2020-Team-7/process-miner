"""
Module used for adding labels to message log entries.
"""
from csv import writer
from csv import reader
from csv import DictReader
from csv import DictWriter


HEADER_OF_NEW_COL = 'label'
BLANK = ' _else_ '

POST = 'Server Response Message'
HTTP = 'Server Request Message'

SEARCHING_ASPSPS = "ASPSPs searching"
ASPSPS_NOT_FOUND = "ASPSP not found"
PROCESSING = "processing"

XS2A = "Xs2aAdapter"
PROFILE = "active profile"
CONSENT = "consent"
SESSION = "session"
TRANSACTION = "transaction"
CHARSET = "charset"
STATUS = "status"
SLACK = "slack"

E_FORMAT = "ERROR_FORMAT"
E_INTERNAL_SERVER = "ERROR_INTERNAL_SERVER"
E_PSU_INVALID = "ERROR_PSU_CREDENTIALS_INVALID"
E_SERVICE_INVALID = "ERROR_SERVICE_INVALID"
W_SERVICE_UNAVAILABLE = "WARNING_SERVICE_UNAVAILABLE"
UNHANDLED_EXCEPTION = "Unhandled exception"


def add_label_column_in_csv(input_file, output_file):
    """ open, read and write the csv file """
    with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:

        dict_reader = DictReader(read_obj)
        field_names = dict_reader.fieldnames

        append_field(field_names)
        dict_writer = DictWriter(write_obj, field_names)
        dict_writer.writeheader()

        for row in dict_reader:
            if "POST" in row['message']:
                add_post(row, dict_reader.line_num)
            elif "PUT" in row['message']:
                add_post(row, dict_reader.line_num)

            elif "TTP/" in row['message']:
                add_http(row, dict_reader.line_num)
            elif "earching for ASPSPs" in row['message']:
                add_aspsps_search(row, dict_reader.line_num)
            elif "earch ASPSPs" in row['message']:
                add_aspsps_search(row, dict_reader.line_num)
            elif "spsp was not found for bankCode" in row['message']:
                add_aspsps_not_found(row, dict_reader.line_num)
            elif "rocessing" in row['message']:
                add_processing(row, dict_reader.line_num)

            elif "s2aAdapter" in row['message']:
                add_xs2a(row, dict_reader.line_num)
            elif "rofiles" in row['message']:
                add_profile(row, dict_reader.line_num)
            elif "onsent" in row['message']:
                add_consent(row, dict_reader.line_num)
            elif "ession" in row['message']:
                add_session(row, dict_reader.line_num)
            elif "ransaction" in row['message']:
                add_transaction(row, dict_reader.line_num)
            elif "harset" in row['message']:
                add_charset(row, dict_reader.line_num)
            elif "tatus" in row['message']:
                add_status(row, dict_reader.line_num)
            elif "lack" in row['message']:
                add_slack(row, dict_reader.line_num)

            elif "FORMAT_ERROR" in row['message']:
                add_error_format(row, dict_reader.line_num)
            elif "INTERNAL_SERVER_ERROR" in row['message']:
                add_error_internal_server(row, dict_reader.line_num)
            elif "PSU_CREDENTIALS_INVALID" in row['message']:
                add_error_psu_credentials_invalid(row, dict_reader.line_num)
            elif "SERVICE_INVALID" in row['message']:
                add_error_service_invalid(row, dict_reader.line_num)
            elif "SERVICE_UNAVAILABLE" in row['message']:
                add_warning_service_unavailable(row, dict_reader.line_num)
            elif "nhandled exception" in row['message']:
                add_unhandeled_exception(row, dict_reader.line_num)

            else:
                add_blank(row, dict_reader.line_num)
            dict_writer.writerow(row)


def append_field(field_names):
    """alternative: field_names.insert(2, header_of_new_col)"""
    field_names.append(HEADER_OF_NEW_COL)
def add_blank(row, line_num):
    """ filling else """
    row.update({HEADER_OF_NEW_COL: BLANK})

def add_post(row, line_num):
    """ searching for key word post """
    row.update({HEADER_OF_NEW_COL: POST})
def add_http(row, line_num):
    """ searching for key word http """
    row.update({HEADER_OF_NEW_COL: HTTP})
def add_aspsps_search(row, line_num):
    """ searching for key word aspsps search """
    row.update({HEADER_OF_NEW_COL: SEARCHING_ASPSPS})
def add_aspsps_not_found(row, line_num):
    """ searching for key word aspsps not found """
    row.update({HEADER_OF_NEW_COL: ASPSPS_NOT_FOUND})
def add_processing(row, line_num):
    """ searching for key word processing """
    row.update({HEADER_OF_NEW_COL: PROCESSING})
def add_xs2a(row, line_num):
    """ searching for key word xs2a """
    row.update({HEADER_OF_NEW_COL: XS2A})
def add_profile(row, line_num):
    """ searching for key word profile """
    row.update({HEADER_OF_NEW_COL: PROFILE})
def add_consent(row, line_num):
    """ searching for key word consent """
    row.update({HEADER_OF_NEW_COL: CONSENT})
def add_session(row, line_num):
    """ searching for key word session """
    row.update({HEADER_OF_NEW_COL: SESSION})
def add_transaction(row, line_num):
    """ searching for key word transaction """
    row.update({HEADER_OF_NEW_COL: TRANSACTION})
def add_charset(row, line_num):
    """ searching for key word charset """
    row.update({HEADER_OF_NEW_COL: CHARSET})
def add_status(row, line_num):
    """ searching for key word status"""
    row.update({HEADER_OF_NEW_COL: STATUS})
def add_slack(row, line_num):
    """ searching for key word slack """
    row.update({HEADER_OF_NEW_COL: SLACK})


def add_error_format(row, line_num):
    """ searching for error format """
    row.update({HEADER_OF_NEW_COL: E_FORMAT})
def add_error_internal_server(row, line_num):
    """ searching for error server """
    row.update({HEADER_OF_NEW_COL: E_INTERNAL_SERVER})
def add_error_psu_credentials_invalid(row, line_num):
    """ searching for error psu """
    row.update({HEADER_OF_NEW_COL: E_PSU_INVALID})
def add_error_service_invalid(row, line_num):
    """ searching for error service """
    row.update({HEADER_OF_NEW_COL: E_SERVICE_INVALID})
def add_warning_service_unavailable(row, line_num):
    """ searching for warning service """
    row.update({HEADER_OF_NEW_COL: W_SERVICE_UNAVAILABLE})
def add_unhandeled_exception(row, line_num):
    """ searching for unhandeled exception  """
    row.update({HEADER_OF_NEW_COL: UNHANDLED_EXCEPTION})

add_label_column_in_csv('graylog-search-result-relative-0.csv',
                        'output_log_label_with_graylog_data.csv')
