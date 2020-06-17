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
* `filters`
    * `filter_expressions` - Array of Regular Expressions that can be used to remove log entries that do not serve any purpose for the process mining

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

The retrieving of logs is done by the class `LogRetriever` implemented in the module `log_retriever`. After configuring the class the retrieval process is started by calling the method `retrieve_logs`.

Before retrieving any logs the `LogRetriever` will check the target directory for the existence of the file `last_included_timestamp` which indicates that the directory has already been used and contains log entries up to the time specified by the timestamp found in the file. During repeated log retrieval to the same target directory all log entries up to that timestamp will not be retrieved again.

Currently the retrieved values for each log entry are `timestamp`, `correlationId` and `message`. The retrieved log entries will be grouped by their `correlationId` and stored in separate files in the CSV format. The files will be named using the timestamp of the first contained log entry and the `correlationId` (eg. `2020-05-21T16_01_09.038Z_FD59B377DFE72EDE64C95C94C98182E4.csv`).

#### Filtering

The retrieved log entries will be filtered before being processed further. This is done by the class `LogFilter` implemented in the module `log_filter`. During this process all log entries missing either of the fields `timestamp`, `correlationId` or `message` will be removed. Additionally all entries with a `message` that matches any of the regular expressions supplied in the configuration file via `filter_expressions` will also be removed. By default the following expressions will be used:
* `^Searching for ASPSPs:` - duplicate entries that seem to occur asynchronously after retrieving bank information
* `^UTF-8 charset will be used for response body parsing$` - entries that provide information about how responses are processed without being a step of their own

=======
#### Tagging

To aid the process mining the class `LogTagger` from the module `log_tagger` extracts information from the processed log entries fields. This is done by trying to match a pattern on the source field of each log entry and inserting a fixed value into a target field if the pattern was matched successfully. The source field, the used patterns and the inserted values can be configured in the `tags` section of the configuration file. For each subsection of `tags` an additional column named after the subsection is added to the output CSV files. An example configuration may look like this:

    tags:
      fieldname:                  # name of the field the tag gets written to
        source: 'source'          # field that gets matched to determine the tag value
        tag_all: false            # whether only the matching entry or all related entries should be tagged
        default_value: 'default'  # default value that is used if no matching value was found
        mappings:                 # mapping of tag values to their respective keyword(s)
          'value1':               # value that is inserted if one of its patterns matched
            - 'pattern11'
            - 'pattern12'
          'value2':               # another pattern
            - 'pattern21'
      'another fieldname':
        .....

Even if none of the patterns matched each tags field will be present in the output files. For concrete usage examples see `docs/example_process_miner_config.yaml`.

=======
## Common Paths for all Approaches
The graphs are stored in the directory `common_path` as Scalable Vector Graphics.

Naming conditions:
{visualization type}_{approach type}.svg

`visualization type`:
- `heuristicnet`: Heuristic Net

- `dfg`: Directly-Follows-Graph

Results are available for the `approach type`:
- `all` All approaches combined

- `embedded` Embedded approach

- `redirect` Redirect approach

- `not available` Entries without available approach type
