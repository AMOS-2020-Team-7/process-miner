import os
import unittest
import MockdataExample
import MockdataLogs

class MockdataTest(unittest.TestCase):
    
    def test_dataimport_Mockdata(self):
        file = os.path.isfile(MockdataExample.datasourceMockdata())
        self.assertTrue(file, "No Mockdata File available")

    def test_dataimport_MockdataLogs(self):
        file = os.path.isfile(MockdataLogs.datasourceMockdata())
        self.assertTrue(file, "No Mockdata Logs available")

if __name__ == '__main__':
    unittest.main()




