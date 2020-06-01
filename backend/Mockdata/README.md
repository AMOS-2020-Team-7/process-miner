# Mockdata
Sample logs are collected and processed to some mock results.

## Structure
- `Data` Logs collected as CSV

- `pics` Mock results stored as SVG and PNG
- `Simple` simple examples
- `Tests` Unit tests
- `Documentation.md` Documentation on proccess mining, the use of the PM4PY library to get an algorithm understanding

## Examples
- `Main.py` execute `EmbeddedFlowLog.py` and `EmbeddedFlowTheory.py`

- `EmbeddedFlowLog.py` execute an example embedded flow with theoretical data to represent data as Directly-Follows Graph, Heuristic Net, Petri Net
- `EmbeddedFlowTheory.py` execute an example embedded flow with extracted data out of Graylog to represent data as Directly-Follows Graph, Heuristic Net, Petri Net

### Simple Examples
- `ProcessMining.py` execute `MockdataExample.py` and `MockdataLogs.py`

- `MockdataExample.py` execute an simple example with mockdata to represent data as Directly-Follows Graph, Heuristic Net, Petri Net
- `MockdataLogs.py` execute an simple example to represent a mockdata log as Heuristic Net, Petri Net
