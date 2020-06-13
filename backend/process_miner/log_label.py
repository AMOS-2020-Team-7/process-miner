from csv import writer
from csv import reader
from csv import DictReader
from csv import DictWriter


header_of_new_col = 'label'
blank = ' _else_ '

post = 'Server Response Message'                               # "POST" or "PUT"
http = 'Server Request Message'                                # 'HTTP/'

searching_aspsps = "ASPSPs searching"                          # 'Searching for ASPSPs' or 'Search ASPSPs'
aspsp_not_found = "ASPSP not found"                            # 'Aspsp was not found for bankCode'
processing = "processing"                                      # 'Processing'

xs2a = "Xs2aAdapter"                                                # 'xs2a'
profile = "active profile"                                          # 'profiles'
consent = "consent"                                                 # 'consent'
session = "session"                                                 # 'session'
transaction = "transaction"                                         # 'transactions'
charset = "charset"                                                 # 'charset'
status = "status"                                                   # 'status'
slack = "slack"                                                     # 'slack'

error_format = "ERROR_FORMAT"                                       # 'FORMAT_ERROR'
error_internal_server = "ERROR_INTERNAL_SERVER"                     # 'INTERNAL_SERVER_ERROR'
error_psu_credentials_invalid = "ERROR_PSU_CREDENTIALS_INVALID"     # 'PSU_CREDENTIALS_INVALID'
error_service_invalid = "ERROR_SERVICE_INVALID"                     # 'SERVICE_INVALID'
warning_service_unavailable = "WARNING_SERVICE_UNAVAILABLE"         # 'SERVICE_UNAVAILABLE'
unhandeled_exception = "Unhandled exception"                        # 'Unhandled exception'



def add_label_column_in_csv(input_file, output_file):                                               #In this function we need to pass an additional callback tansform_column_names, it receives list of column names and we can modify that based on our intent.
    with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:                                             # Open the input_file in read mode and output_file in write mode and yaml file in read mode

        dict_reader = DictReader(read_obj)                      # Create a DictReader object from the input file object
        field_names = dict_reader.fieldnames                    # Get a list of column names from the csv

        append_field(field_names)                               # Call the callback function to modify column name list
        dict_writer = DictWriter(write_obj, field_names)        # Create a DictWriter object from the output file object by passing column / field names
        dict_writer.writeheader()                               # Write the column names in output csv file

        for row in dict_reader:
            if "POST" in row['message']:
                add_post(row, dict_reader.line_num)
            elif "PUT" in row['message']:
                add_post(row, dict_reader.line_num)

            elif "HTTP/" in row['message']:
                add_http(row, dict_reader.line_num)
            elif "Searching for ASPSPs" in row['message']:
                add_aspsps_search(row, dict_reader.line_num)

            elif "Search ASPSPs" in row['message']:
                add_aspsps_search(row, dict_reader.line_num)
            elif "Aspsp was not found for bankCode" in row['message']:
                add_aspsps_not_found(row, dict_reader.line_num)
            elif "Processing" in row['message']:
                add_processing(row, dict_reader.line_num)

            elif "Xs2aAdapter" in row['message']:
                add_xs2a(row, dict_reader.line_num)
            elif "profiles" in row['message']:
                add_profile(row, dict_reader.line_num)
            elif "consent" in row['message']:
                add_consent(row, dict_reader.line_num)
            elif "session" in row['message']:
                add_session(row, dict_reader.line_num)
            elif "transaction" in row['message']:
                add_transaction(row, dict_reader.line_num)
            elif "charset" in row['message']:
                add_charset(row, dict_reader.line_num)
            elif "status" in row['message']:
                add_status(row, dict_reader.line_num)
            elif "slack" in row['message']:
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
            elif "Unhandled exception" in row['message']:
                add_unhandeled_exception(row, dict_reader.line_num)

            else:
                add_blank(row, dict_reader.line_num)
            dict_writer.writerow(row)                           # Write the updated dictionary or row to the output file


def append_field(field_names):
    field_names.append(header_of_new_col)
    #field_names.insert(2, header_of_new_col)
def add_blank(row, line_num):
    row.update({header_of_new_col: blank})

def add_post(row, line_num):
    row.update({header_of_new_col: post})
def add_http(row, line_num):
    row.update({header_of_new_col: http})
def add_aspsps_search(row, line_num):
    row.update({header_of_new_col: searching_aspsps})
def add_aspsps_not_found(row, line_num):
    row.update({header_of_new_col: aspsp_not_found})
def add_processing(row, line_num):
    row.update({header_of_new_col: processing})
def add_xs2a(row, line_num):
    row.update({header_of_new_col: xs2a})
def add_profile(row, line_num):
    row.update({header_of_new_col: profile})
def add_consent(row, line_num):
    row.update({header_of_new_col: consent})
def add_session(row, line_num):
    row.update({header_of_new_col: session})
def add_transaction(row, line_num):
    row.update({header_of_new_col: transaction})
def add_charset(row, line_num):
    row.update({header_of_new_col: charset})
def add_status(row, line_num):
    row.update({header_of_new_col: status})
def add_slack(row, line_num):
    row.update({header_of_new_col: slack})


def add_error_format(row, line_num):
    row.update({header_of_new_col: error_format})
def add_error_internal_server(row, line_num):
    row.update({header_of_new_col: error_internal_server})
def add_error_psu_credentials_invalid(row, line_num):
    row.update({header_of_new_col: error_psu_credentials_invalid})
def add_error_service_invalid(row, line_num):
    row.update({header_of_new_col: error_service_invalid})
def add_warning_service_unavailable(row, line_num):
    row.update({header_of_new_col: warning_service_unavailable})
def add_unhandeled_exception(row, line_num):
    row.update({header_of_new_col: unhandeled_exception})

add_label_column_in_csv('graylog-search-result-relative-0.csv', 'output_log_label_with_graylog_data.csv')