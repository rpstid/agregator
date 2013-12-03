'''
Created on 26/06/2013

@author: raul
'''
from pymongo import MongoClient
from pymongo import errors
import json_dict_utils as utils
from HTMLParser import HTMLParser

class MongoConnector:
    
    def __init__(self):
        db = MongoClient().test
        self.collection = db.info_valladolid
        
    def insert(self, json):
        try:
            self.collection.insert(json)
            print "Inserted"
        except errors.OperationFailure as e:
            print "Could not insert:", HTMLParser().unescape(json[utils.DICT_KEY_EXT_UUID])
            print e.code
            #print e.error
        
    def find(self, fecha_ini = None):
        if fecha_ini:
            return self.collection.find({utils.DICT_KEY_STARTDATE: fecha_ini}, fields=utils.JSON_DICT_KEYS)
        else:
            return self.collection.find(fields=utils.JSON_DICT_KEYS)
    
    def remove(self):
        self.collection.remove()
        
    def ensure_indexes(self):
        self.collection.ensure_index('int_uuid.articleId', 300, {'unique': True, 'name': 'int_uuid__index'})
        
    def index_information(self):
        return self.collection.index_information()
    
    def drop_indexes(self):
        self.collection.drop_index("ext_uuid_1")

if __name__ == '__main__':
    connector = MongoConnector()