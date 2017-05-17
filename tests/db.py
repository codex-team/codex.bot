import unittest

from codexbot.lib.db import Db
from tests.base import BaseTest


class DatabaseTest(BaseTest, unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(BaseTest, self).__init__(*args, **kwargs)
        self.db_name = 'test_db'
        self.collection_name = 'test_collection'

    def setUp(self):
        self.db = Db(self.db_name)
        self.db.insert(self.collection_name, {'id': 'test_id'})

    def testDatabaseInit(self):
        result = list(self.db.find(self.collection_name, {'id': 'test_id'}))
        self.assertNotEquals(len(result), 0)

    def tearDown(self):
        self.db.remove(self.collection_name)
