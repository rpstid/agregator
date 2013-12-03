#! /usr/bin/python
'''
Created on 23/06/2013

@author: raul
'''

import BeautifulSoup as BS
from urllib2 import urlopen
from HTMLParser import HTMLParser
from mongo_connector import MongoConnector
import info_valladolid_item_scrapper as item_scrapper

connector = MongoConnector()

def process_rss(rss_url):
    rss = urlopen(rss_url).read()
    soup = BS.BeautifulSoup(rss)
    items = soup.findAll('item')
    jsons = []
    for i, item in enumerate(items):
        print '----------- item', i+1 , '-----------'
        print_rss_item(item)
        item_content = HTMLParser().unescape(item.description.string)
        json = item_scrapper.process_item_content(BS.BeautifulSoup(item_content), HTMLParser().unescape(item.guid.string))
        if json:
            jsons.append(json)
            connector.insert(json)
        #process_item_url(HTMLParser().unescape(item.link.next))
    return jsons
  
def print_rss_item(item): 
    print "rss_title:   ", item.title.string
    #print "link.next:   ", item.link.next -> same as guid
    #print "description: ", item.description.string
    print "rss_pubdate: ", item.pubdate.string
    print "guid.string: ", HTMLParser().unescape(item.guid.string)
    print "rss_creator: ", item.find("dc:creator").string
    print "rss_date:    ", item.find("dc:date").string
    #print "description:\n", HTMLParser().unescape(item.description.string)
    
if __name__ == '__main__':
    #connector.drop_indexes()
    #connector.remove()
    #connector.ensure_indexes()
    print connector.index_information()
    
    rss_url = "http://info.valladolid.es/web/culturayturismo/canalrss/-/journal/rss/10167/RSS-AGENDA"
    process_rss(rss_url)
                
    for json in connector.find():
        print(json)
        #print json._id
        #utils.print_item_dict(json)

        

    
    
    
    