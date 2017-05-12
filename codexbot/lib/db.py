import logging
from pymongo import MongoClient


class Db():

    def __init__(self, dbname, host='localhost', port=27017):
        """
        Initialize DB class with host and port.
        :param dbname: Database (DB) name
        :param host: DB host
        :param port: DB port
        """
        try:
            self.client = MongoClient(host, port)
            self.db = self.client[dbname]

        except Exception as e:
            logging.error(e)

    def get(self, name):
        """
        Get collection
        :param name: collection name
        :return: JSON output
        """
        return self.db.get(name)

    def find_one(self, collection, params):
        """
        Find piece of data in collection with search params
        :param collection: collection name
        :param params: JSON search params
        :return: JSON result
        """
        return self.db[collection].find_one(params)

    def find(self, collection, params):
        """
        Find data in collection with search params
        :param collection: collection name
        :param params: JSON search params
        :return: List of JSON results
        """
        return self.db[collection].find(params)

    def insert(self, collection, data):
        """

        :param collection:
        :param data:
        :return:
        """
        return self.db[collection].insert(data)

    def remove(self, collection):
        return self.db[collection].remove()
