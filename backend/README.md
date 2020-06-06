# Process Miner Frontend

## Retrieving of logs

### Configuration

The log retriever has to be configured using a YAML file named `process_miner_config.yaml` which should reside at the top level of the `backend` directory.

The file contains the following sections and entries:

* `global`
    * `log_directory` - Target directory for the retrieved logs (may be an absolute or relative path)
* `log_retriever`
    * `url` - URL of the Graylog instance logs should be retrieved from
    * `api_token` - Access Token used for authentication to the Graylog instance (see [Creating and using Access Token](https://docs.graylog.org/en/3.3/pages/configuration/rest_api.html#creating-and-using-access-token))

### Setup and running the code

For setting up the environment only `make` and `pip` are required. Although this guide assumes that `make` is available in your development environment you can also run the respective commands from the included makefile by hand. The project makes use of `pipenv` for dependency management.

To set up the development environment use

`make setup-dev-env`

To determine if changes to the code pass the checks in the CI pipeline use

`make check`

To actually run the flask app use

`make run`

To do all of the above issuing only one command use

`make`

To run the `process_miner` packages main (eg. for testing purposes) use

`make run-main`

### Functional overview

The retrieving of logs is done by the class `LogRetriever` implemented in `log_retriever.py`. After configuring the class the retrieval process is started by calling the method `retrieve_logs`.

Before retrieving any logs the `LogRetriever` will check the target directory for the existence of the file `last_included_timestamp` which indicates that the directory has already been used and contains log entries up to the time specified by the timestamp found in the file. During repeated log retrieval to the same target directory all log entries up to that timestamp will not be retrieved again.

Currently the retrieved values for each log entry are `timestamp`, `correlationId` and `message`. The retrieved log entries will be grouped by their `correlationId` and stored in separate files in the CSV format. The files will be named using the timestamp of the first contained log entry and the `correlationId` (eg. `2020-05-21T16_01_09.038Z_FD59B377DFE72EDE64C95C94C98182E4.csv`).