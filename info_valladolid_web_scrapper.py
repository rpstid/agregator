#! /usr/bin/python
'''
Created on 23/06/2013

@author: raul
'''

import BeautifulSoup as BS
from urllib2 import urlopen
from HTMLParser import HTMLParser
from mongo_connector import MongoConnector
#import json_dict_utils as utils
import info_valladolid_item_scrapper as item_scrapper

connector = MongoConnector()

def process_url(url):
    html = urlopen(url).read()
    soup = BS.BeautifulSoup(html)
    accordion2 = soup.find('div', id='Accordion2')
    #print accordion2.prettify()
    
    litems = accordion2.findAll('li')
    items=[]
    for li in litems:
        a = li.find('a')
        link = HTMLParser().unescape(a['href'])
        titulo = a.string
        hora = li.find("div", "hora").string
        lugar = li.find("span", "lugarevento").string 
        print "--------------------------------------------------------------------------------"
        item = item_scrapper.process_item_url(link, titulo, hora, lugar)
        if item:
            items.append(item)
            connector.insert(item)
        else:
            print "NOT INSERTED!!!"
    return items

if __name__ == '__main__':
    url = "http://info.valladolid.es/web/culturayturismo/que-hacer"
    
    #connector.remove()
    process_url(url)
    
    """    
    for json in connector.find():
        print(json)
        #print json._id
        utils.print_item_dict(json)
    """


        

    
    
    