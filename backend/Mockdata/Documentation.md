# Documentation: Process Mining with PM4PY
Further information (https://pm4py.fit.fraunhofer.de/documentation)

## Importing CSV Files

### Prerequisites
- csv file ordered by time
- include at least the columns: correlationId, activity, timestamp

### Convert the CSV into an event log object

1. import the CSV file using pandas
2. converting it to the event log object, dedicated package `objects.conversion.log`
3. CSV-file represents a sequence of events -> need for specification
- `CASE_ID_KEY` & `case:concept:name` which attribute belong to the same case;column defines traces. In our case: _(correlation id)_

- `time:timestamp`
- `case:name` column of the data frame that is the _activity (=message)_

depends on our used variables

(- `CASE_ATTRIBUTE_PREFIX` & `case:` column describes a case-level attribute (attribute does not change during the execution of a process))

`EmbeddedFlowTheory.py`

        from pm4py.objects.log.adapters.pandas import csv_import_adapter
        from pm4py.objects.conversion.log import factory as conversion_factory

        dataframe = csv_import_adapter.import_dataframe_from_path(EmbeddedTheory.csv, sep=";")
        dataframe = dataframe.rename(columns={'correlationId': 'case:concept:name', 'timestamp': 'time:timestamp', 'message': 'concept:name'})
        log = conversion_factory.apply(dataframe)

## Filtering Event Data
- many possibilities to filter the logs
- but may be easier and for the project more relevant to filter the data beforehand

### Filtering on timeframe
- keep events that are contained in specific timeframe
- maybe not relevant, because entries in the log should not be filtered that belong to one Process

### Filter on case performance
- keep only entries with duration that is inside a specific time interval

### Filter on start activities
- a list of start activities has to be specified
- decreasing factor is used
- first activity is kept, afterwards depending on number of occurrences the next activity is included or the process stops
- to find out which are the most frequent starting activities
- for the case that we have several relevant starting activities

### Filter on end activities
- similar to Filter on start activities
- a list of end activities has to be specified
- decreasing factor is used
- for the case that we have several relevant end activities

### Filter on variants
- variant is a set of cases that share the same activities in the same order
- filter on variant to get rid of other log data or to filter out the variant

### Filter on attributes values
- keep cases that contain at least one attribute value within the message (=activity)
- remove cases that contain one given attribute value
- maybe better to do that when fetching data from Graylog

### Filter on numeric attribute values
- keep only cases where the event satisfies a given numerical attribute value


## Process Discovery

### Heuristic Miner
- mines the control-flow perspective of a process
model

- acts on the Directly-Follows Graph (DFG)

- handles noise and finds common constructs (dependency between two activities, AND)
- output is an Heuristics Net (object that contains the activities and relationships) or Petri Net
- outcome as .png or .svg (also .pnml for Petri net possible)

#### Threshold
- __!!!__ `DEPENDENCY_THRESH` Which percentage observed in whole log (default 0.5)  

  - observation if there is a dependency relation between two activities (A & B)

  - what is a good threshold that B truly depends on A?
  - in our case it could be necessary to observe all possible relations as the log will be probably extracted and filtered before the process mining, so the noise will be removed

<br>
  These weren't relevant so far for the mockup results:

- `AND_MEASURE_THRESH` (default 0.65)
- `MIN_ACT_COUNT` minimum number of occurrences of an activity to be considered (default:1)

- `DFG_PRE_CLEANING_NOISE_THRESH` cleaning threshold of the DFG (in order to remove weaker edges, default 0.05)
- `LOOP_LENGTH_TWO_THRESH` thresholds for the loops of length 2

      from pm4py.objects.petri.exporter import exporter as pnml_exporter

      #Heuristics Miner, acts on the Directly-Follows Graph, find common structures, output: Heuristic Net (.png or .svg)

      heu_net = heuristics_miner.apply_heu(log, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.00})
      gviz2 = hn_vis.apply(heu_net, parameters={hn_vis.Variants.PYDOTPLUS.value.Parameters.FORMAT: "png"})
      hn_vis.view(gviz2)

      #Petri Net based on Heuristic Miner (.png, .svg or .pnml)

      net, im, fm = heuristics_miner.apply(log, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.00})
      gviz3 = petri_vis.apply(net, im, fm, parameters={petri_vis.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"})
      petri_vis.view(gviz3)
      pnml_exporter.apply(net, im, "pics/petri_embeddedFlowTheory.pnml", final_marking=fm)

## Directly-Follows Graph
- nodes represent the activities in the logs
- directed edges are presented if there is at least a trace in the log where the source activity is followed by the target activity
- metrics performance and frequency can be included

`EmbeddedFlowTheory.py`

      from pm4py.util import constants

      #Directly-Follows Graph, represent frequency or performance
      parameters = {constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name"}
      variant='frequency'
      dfg = dfg_factory.apply(log, variant=variant, parameters=parameters)
      gviz1 = dfg_vis_factory.apply(dfg, log=log, variant=variant, parameters=parameters)
      dfg_vis_factory.view(gviz1)


## Petri Net Management
- Petri Nets: well-defined semantic
  - process execution starts from the places included the initial marking
  - finishes at the places included in the final marking
  - adds AND-split and AND-join which are two non-observable activities that are added to the process model to execute two parallel activities
  - results in modelling of invisible activities

### Notation
- Places: circles (store information, keep system status)
- Transitions: box (process the information, change system behavior)

### Adding information about Frequency/Performance
Using replay technique: important to include _log=log_

    net, im, fm = heuristics_miner.apply(log, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.00})
    gviz3 = petri_vis.apply(net, im, fm, parameters={petri_vis.Variants.PERFORMANCE.value.Parameters.FORMAT: "svg"}, variant=petri_vis.Variants.PERFORMANCE, log=log)
    petri_vis.view(gviz3)

- `petri_vis.Variants.WO_DECORATION` default
- `petri_vis.Variants.FREQUENCY` frequency information
- `petri_vis.Variants.PERFORMANCE` performance information

## Examples
based on the _Embedded Flow diagram_ below

- Theory: Embededd Flow

  - Presented Embedded Flow transferred into a theoretical log: `EmbeddedTheory.csv`

  - Run embedded example with theoretical data: `EmbeddedFlowTheory.py`

- Reality: Extracted Data out of Graylog

  - Modified log: `EmbeddedGraylog.csv`

  - Run embedded example with real extracted data: `EmbeddedFlowLog.py`

- Run both examples: `Main.py`

## Results

<br>

1. Embedded Flow Diagram  

<br>
    <center><img src="/pics/embedded%20flow%20diagram.jpeg" alt="Embedded Flow Diagram" width="500"/></center>  
</br>

2. Possible Structures of an Embedded Flow: `EmbeddedFlowTheory.py`

    <center><table><tr><td><center>DFG</br></br><img src="/pics/DFG_TestLog_Theory_Embedded.png" alt="/pics/DFG_TestLog_Theory_Embedded.png" height="1300"/></td><td><center>Heuristic Net</br></br>
    <img src="/pics/Heuristic Net_TestLog_Theory_Embedded.png" alt="/pics/Heuristic Net_TestLog_Theory_Embedded.png" height="1300"/></td></tr></table></center>
    <center><table><td><center>Petri Net</br></br><img src="/pics/Petri Net_TestLog_Theory_Embedded.png" alt="/pics/Petri Net_TestLog_Theory_Embedded.png"/></td></table></center>


3. Possible Extracted Log Results of an Embedded Flow: `EmbeddedFlowLog.py`
  <center><table><tr><td><center>DFG</br></br><img src="/pics/DFG_Graylog_Theory_Embedded.png" alt="/pics/DFG_Graylog_Theory_Embedded.png"/></td></tr></table></center>


  <center><table><td><center>Heuristic Net</br></br>
  <img src="/pics/Heuristic Net_Graylog_Theory_Embedded.png" alt="Heuristic Net_Graylog_Theory_Embedded.png"/></td></table></center>

  <center><table><td><center>Petri Net</br></br><img src="/pics/Petri Net_Graylog_Theory_Embedded.svg" alt="/pics/Petri Net_Graylog_Theory_Embedded.svg"/></td></table></center>

4. Observations

    - important how to choose dependency threshold!!
      - very strict because no noise?
      - very low because all relations are important?

      - So far the sample logs had only one correlationId and activities were observed ones

        - DEPENDENCY_THRESH<=0.5 to see all paths

    - Heuristic Net: if the value of messages (=activities) only differ a little bit in the middle of the long message, the results are displayed incorrect (loops emerge)
    - Petri Net as .svg because too many entries for .png
      - As a result the messages need to be clearly distinguishable in the beginning

    - even if the algorithm should consider the timestamp, the log data needs to be ordered by time

    - noise free log or work with thresholds?
      - need to be able to see e.g., where people stopped process

    - frequency and performance aspects can be integrated into DFGs and Petri Nets
