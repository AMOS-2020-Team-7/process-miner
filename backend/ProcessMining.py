import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

if __name__ == "__main__":
    from backend import Mockdata
    from backend import MockdataLogs

    print("\n\Mockdata")
    Mockdata.execute_script()

    print("\n\MockdataLogs")
    MockdataLogs.execute_script()