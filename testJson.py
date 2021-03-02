import unittest
from json_convert import *
import json


class testJson(unittest.TestCase):

    def test_export_json(self):
        """ test write_json: export data as json file 
        """
        testDict = {'nrx': 'student', "age": "100"}
        write_json(testDict, 'test_json.json')
        with open('test_json.json') as f:
            file_data = json.load(f)
        self.assertEqual(file_data["nrx"], 'student', "should be student")
        self.assertEqual(file_data["age"], "100", "should be 100")
        self.assertFalse('Bon' in file_data)

    def test_read_json(self):
        """test read from json file to get new data 
        """
        testDict = {'nrx': 'student', "age": "100"}
        json.dump(testDict, open('test_json.json', 'w'))
        file_data = write_data('test_json.json')
        self.assertEqual(file_data["nrx"], 'student', "should be student")
        self.assertEqual(file_data["age"], "100", "should be 100")
        self.assertFalse('Bon' in file_data)

    def test_both(self):
        """test both read and export
        """
        testDict = {'nrx': 'student', "age": "100"}
        write_json(testDict, 'test_json.json')
        file_data = write_data('test_json.json')
        self.assertEqual(file_data["nrx"], 'student', "should be student")
        self.assertEqual(file_data["age"], "100", "should be 100")
        self.assertFalse('Bon' in file_data)


if __name__ == '__main__':
    unittest.main()
