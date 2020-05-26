# Process Miner Frontend

## Retrieving of logs

### Configuration

The log retriever has to be configured using the `log_retriever` section of the config file `process_miner_config.py`.

* `url` - URL of the Graylog instance logs should be retrieved from
* `api_token` - Access Token used for authentication to the Graylog instance (see [Creating and using Access Token](https://docs.graylog.org/en/3.3/pages/configuration/rest_api.html#creating-and-using-access-token))
* `target_dir` - Target directory for the retrieved logs. May be an absolute or relative path.

### Functional overview

The retrieving of logs is done by the class LogRetriever implemented in `log_retriever.py`. After configuring the class the retrieval process is started by calling the method `retrieve_logs`.

Before retrieving any logs the LogRetriever will check the target directory for the existence of the file `last_included_timestamp` which indicates that the directory has already been used and contains log entries up to the time specified by the timestamp found in the file. During repeated log retrieval to the same target directory all log entries up to that timestamp will not be retrieved again.

Currently the retrieved values for each log entry are `timestamp`, `correlationId` and `message`. The retrieved log entries will be grouped by their `correlationId` and stored in separate files in the CSV format. The files will be named using the timestamp of the first contained log entry and the `correlationId` (eg. `2020-05-21T16:01:09.038Z_FD59B377DFE72EDE64C95C94C98182E4.csv`).