from unittest import TestCase
import json


ACCOUNT_DATA = {}

class TestDb(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        global ACCOUNT_DATA

        db.connect()
        with open('fixture/data.json') as f:
            ACCOUNT_DATA = json.load(f)


    def test_create_an_account(self):
        """pass data and add to db"""
        pass


    @classmethod
    def tearDownClass(cls) -> None:
        db.close()
