# Example Process Miner

## Configuration

The example process miner uses the following configuration file entries in `process_miner_config.yaml`

* `global`
    * `log_directory` - Target directory for the retrieved logs (may be an absolute or relative path)

## Common Paths for all Approaches


The graphs are stored in the directory `common_path`

Naming conditions:
{visualization type}_{approach type}_{with or without errors}.{output_format}

### Visualization Type
`visualization type`:
- `heuristicnet`: Heuristic Net

- `dfg`: Directly-Follows-Graph

### Approach Type
Results are available for the `approach type` that needs to be chosen in `__main__.py`:
- `all` All approaches combined

- `embedded` Embedded approach

- `redirect` Redirect approach

- `not available` Entries without available approach type

### With or Without error_sca_status_405
Choose in `__main__.py` if you want to filter or if you want to include the logs where an error occured.

### Output format
Use one of the formats that are supported by PyDotPlus that provides a Python Interface to Graphviz’s Dot:
- bmp
- canon
- cmap, cmapx, cmapx_np
- dot
- emf, emfplus
- eps
- fig
- gd, gd2
- gif
- gv
- imap, imap_np, ismap
- jpe jpeg jpg
- metafile
- pdf
- pic
- plain, plain-ext
- png
- pov
- ps, ps2
- svg svgz
- tif tiff
- tk
- vml, vmlz, vrml
- wbmp
- xdot, xdot1.2, xdot1.4

further details and explanation can be looked up here: https://graphviz.org/doc/info/output.html

#### Output Formats to Consider

`plain`, `plain-ext`:
- https://graphviz.org/doc/info/output.html#d:plain-ext
- contains four types of statements
  - graph: _scale width height_
  - node: _node x y witdht height label style shape color fillcolor_
  - edge: _tail head n x1 y1 ... xn yn [label xl yl] style color_
  - stop

`dot`, `xdot`:
- https://graphviz.org/doc/info/output.html#d:dot
- contains information about nodes and their labels
