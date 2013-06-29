#! /usr/bin/python
'''
Created on 23/06/2013

@author: raul
'''

import BeautifulSoup as BS
from urllib2 import urlopen
from HTMLParser import HTMLParser
from datetime import datetime
from mongo_connector import MongoConnector

def process_rss(rss_url, connector):
    rss = urlopen(rss_url).read()
    soup = BS.BeautifulSoup(rss)
    items = soup.findAll('item')
    for i, item in enumerate(items):
        print '----------- item', i+1 , '-----------'
        print_rss_item(item)
        item_content = HTMLParser().unescape(item.description.string)
        json = process_item_content(BS.BeautifulSoup(item_content))
        
        connector.insert(json)
        #process_item_url(HTMLParser().unescape(item.link.next))
  
def print_rss_item(item): 
    print "rss_title:   ", item.title.string
    #print "link.next:   ", item.link.next -> same as guid
    #print "description: ", item.description.string
    print "rss_pubdate: ", item.pubdate.string
    print "guid.string: ", HTMLParser().unescape(item.guid.string)
    print "rss_creator: ", item.find("dc:creator").string
    print "rss_date:    ", item.find("dc:date").string
    #print "description:\n", HTMLParser().unescape(item.description.string)
    
"""    
def process_item_url(item_url):
    item = urlopen(item_url).read()
    itemsoup = BS.BeautifulSoup(item)
    content = itemsoup.find(id="LCDAM_contenido")
    process_item_content(content)
"""
    
def process_item_content(content):
    
    title = content.h1.string
    place = content.ul.li.h3.string if content.ul.li.h3 is not None else None
    
    date_ini_str = content.find("li", "FechaInicio").string.replace("Fecha de inicio: ","").strip()
    datetime_ini = get_datetime(date_ini_str)
    datehour_ini = get_date_hour(datetime_ini)
    
    date_fin_str = content.find("li", "FechaFin").string.replace("Fecha de fin:  ","").strip()
    datetime_end = get_datetime(date_fin_str)
    datehour_end = get_date_hour(datetime_end)
    
    ev_types = get_content(content, "Tipo", "Tipo de evento:")
    publics = get_content(content, "Publico", "Publico objetivo:") 
    descriptions = [unicode(desc) for desc in content.p.contents]

    
    item_dict = {"startDate": datehour_ini[0], "title": title, "location": place, \
                 "types": ev_types, "publics": publics, "descriptions": descriptions}
    
    if datehour_ini[1]:
        item_dict["startTime"] = datehour_ini[1]
    if datehour_end[0] != datehour_ini[0]:
        item_dict["endDate"] = datehour_end[0]
    if datehour_end[1]:
        item_dict["endTime"] = datehour_end[1]
    
    #print_item_dict(item_dict)
    return item_dict
    
    #print "datetimeIni: ", datetime_ini
    #print "datetimeEnd: ", datetime_end
    #print contenido.prettify()
    
def print_item_dict(item_dict):
    print
    print "title:       ", item_dict["title"]
    print "place:       ", item_dict["location"]
    print "dateIni:     ", item_dict["startDate"]
    if item_dict.has_key("startTime"):    
        print "hourIni:     ", item_dict["startTime"]
    if item_dict.has_key("endDate"):
        print "dateEnd:     ", item_dict["endDate"]
    if item_dict.has_key("endTime"):        
        print "hourEnd:     ", item_dict["endTime"]
    print_array(item_dict["types"], "Tipo de evento")
    print_array(item_dict["publics"], "Publico objetivo")
    #print_array(item_dict["descriptions"], "Descripcion")
    
def print_array(array, array_name):
    print array_name, "[", len(array), "]:"
    for i, array_ele in enumerate(array):
        print "\t(", i, ")", array_ele

def get_datetime(date_str):
    has_time = False
    if len(date_str) > 10:
        date_time = datetime.strptime(date_str, '%d/%m/%Y    %H:%M')
        has_time = True
    else:
        date_time = datetime.strptime(date_str, '%d/%m/%Y')
    return (date_time, has_time)

def get_date_hour(datetime):
    hour = datetime[0].strftime('%H:%M') if datetime[1] else None
    return (datetime[0].strftime('%Y-%m-%d'), hour) 

def get_content(content, li_name, del_str):
    li = content.find("li", li_name)
    for e in li.findAll('br'):
        e.extract()
    li.contents[0] = li.contents[0].replace(del_str, "")
    return [li_content.replace('\t','').strip() for li_content in li.contents if not li_content.strip() == u'']

if __name__ == '__main__':
    rss_url = "http://info.valladolid.es/web/culturayturismo/canalrss/-/journal/rss/10167/RSS-AGENDA?doAsGroupId=10167&refererPlid=13213"
    
    connector = MongoConnector()
    connector.remove()
    process_rss(rss_url, connector)
    results = connector.find()
    for json in results:
        print(json)
        #print json._id
        print_item_dict(json)

        

    
    
    
    