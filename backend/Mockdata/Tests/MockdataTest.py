import os
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest

import Mockdata.Simple.MockdataExample
import Mockdata.Simple.MockdataLogs
import Mockdata.EmbeddedFlowTheory
import Mockdata.EmbeddedFlowLog


class MockdataTest(unittest.TestCase):

    def test_dataimport_Mockdata(self):
        pathfile = "../Simple/" + Mockdata.Simple.MockdataExample.datasourceMockdata()
        file = os.path.isfile(pathfile)
        self.assertTrue(file, "No Mockdata File for MockdataExample.py available")

    def test_dataimport_MockdataLogs(self):
        pathfile = "../Simple/" + Mockdata.Simple.MockdataLogs.datasourceMockdata()
        file = os.path.isfile(pathfile)
        self.assertTrue(file, "No Mockdata Logs for MockdataLogs.py available")

    def test_dataimport_EmbeddedFlowTheory(self):
        pathfile = "../" + Mockdata.EmbeddedFlowTheory.datasourceMockdata()
        file = os.path.isfile(pathfile)
        self.assertTrue(file, "No Mockdata File for EmbeddedFlowTheory.py available")

    def test_dataimport_EmbeddedFlowLog(self):
        pathfile = "../" + Mockdata.EmbeddedFlowLog.datasourceMockdata()
        file = os.path.isfile(pathfile)
        self.assertTrue(file, "No Mockdata File for EmbeddedFlowLog.py available")



if __name__ == '__main__':
    unittest.main()




