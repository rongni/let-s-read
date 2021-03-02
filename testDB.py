import ssl
import os
import unittest
import pymongo
import json
from dotenv import load_dotenv
load_dotenv()
db_pw = os.getenv("PW")


class test_db(unittest.TestCase):
    def test_connect(self):
        client = pymongo.MongoClient(
            "mongodb+srv://rni42:"+db_pw +
            "@cluster0.l9fca.mongodb.net/uniteTest?retryWrites=true&w=majority",
            ssl_cert_reqs=ssl.CERT_NONE)

        self.assertTrue(client)
        client.close()

    def test_insert_data(self):
        client = pymongo.MongoClient(
            "mongodb+srv://rni42:"+db_pw +
            "@cluster0.l9fca.mongodb.net/uniteTest?retryWrites=true&w=majority",
            ssl_cert_reqs=ssl.CERT_NONE)
        mydb = client.uniteTest
        info = mydb["info"]
        test_dict = {"name": "nrx", "age": "100"}
        info.insert_one(test_dict)
        self.assertTrue(info.find_one({"age": "100"}))
        self.assertFalse(info.find_one({"age": "20"}))
        many_dict = [{"name": "n", "age": "1"},
                     {"name": "Bob", "age": "2"}]
        info.insert_many(many_dict)
        self.assertTrue(info.find_one({"name": "n"}))
        self.assertFalse(info.find_one({"age": "20"}))


if __name__ == '__main__':
    unittest.main()
