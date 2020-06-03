# Documentation: log data provided by graylog
Select and export data from graylog for process mining. [Further information: Graylog Documentation](https://mydocs-edmundoa.readthedocs.io/en/docs/index.html)

## Log export
* In graylog the data type (_fields_) can be selected before exporting the .csv file. [_how-to_](https://mydocs-edmundoa.readthedocs.io/en/docs/pages/queries.html#export-results-as-csv)

##### For process mining it is necessary to have at least the three information:
* case id --> _correlation_id_
* activity --> _message_
* timestamp --> _timestamp_

![necessary information for process mining](/Users/larslempenauer/Amos/ProcessMining/process-miner/backend/graylog/graylogDataStructure.png)

Every further information is optional.

##### timestamp
Saved as _yyyy-mm-dd hh-mm-ss_

##### correlation_id
key attribute to match all activities to the right event. Saved as _string_

##### message / full_message
Contains the information about the type of activity. If the original message is needed, use full_message [_see_](https://mydocs-edmundoa.readthedocs.io/en/docs/pages/queries.html#export-results-as-csv). Saved as _string_


## CSV file format
Graylog exports .csv files, the table is stored as a list. All fields of each record are in one line, separated by comma. Note: the .csv format is not standardized. 

##### order of the *relevant* data in the .csv file exported from graylog:
1. timestamp
2. correlationId
3. _full_message_
4. message

(notice: timestamp is always in the file, even if the field is not selected before exporting)

##### order of *all* the data in the .csv file exported from graylog:

1. **timestamp**
2. "source"
3. "adapterId"
4. "alert"
5. "application"
6. "aspspId"
7. "consentModel"
8. **"correlationId"**
9. "environment"
10. "event_definition_id"
11. "event_definition_type"
12. "fields"
13. **"full_message"**
14. "gl2_message_id"
15. "gl2_processing_timestamp"
16. "gl2_receive_timestamp"
17. "gl2_remote_ip"
18. "gl2_remote_port"
19. "gl2_source_input"
20. "gl2_source_node"
21. "iban"
22. "id"
23. "key"
24. "key_tuple"
25. "level"
26. "logger_name"
27. **"message"**
28. "operation"
29. "origin_context"
30. "priority"
31. "some_env_var"
32. "some_info"
33. "source_streams"
34. "streams"
35. "thread_name"
36. "timerange_end"
37. "timerange_start"
38. "timestamp_processing"
39. "triggered_jobs"
40. "user_id"
