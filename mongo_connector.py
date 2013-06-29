'''
Created on 26/06/2013

@author: raul
'''
from pymongo import MongoClient

class MongoConnector:
    
    def __init__(self):
        db = MongoClient().test
        self.collection = db.info_valladolid
        
    def insert(self, json):
        self.collection.insert(json)
        
    def find(self):
        return self.collection.find(fields=["_id", "title", "location", "startDate", "startTime", "endDate", "endTime", "types", "publics"])
    
    def remove(self):
        self.collection.remove()

if __name__ == '__main__':
    connector = MongoConnector()