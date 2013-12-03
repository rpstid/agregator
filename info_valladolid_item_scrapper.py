'''
Created on 04/07/2013

@author: raul
'''

import BeautifulSoup as BS
from urllib2 import urlopen
from datetime import datetime
import json_dict_utils as utils
import re
import json

root_uri = u"http://info.valladolid.es"

def process_item_url(item_url, title=None, hour=None, location=None):
    print "Processing:", item_url
    item = urlopen(item_url).read()
    itemsoup = BS.BeautifulSoup(item)
    content = itemsoup.find(id="LCDAM_contenido")
    
    if content:
        item_dict = process_item_content(content, item_url)
    else:
        item_dict = {utils.DICT_KEY_EXT_UUID: item_url, \
                     utils.DICT_KEY_INT_UUID: get_int_uuid_more_info(item_url)[0], \
                     utils.DICT_KEY_TITLE: title,\
                     utils.DICT_KEY_STARTTIME: hour,\
                     utils.DICT_KEY_LOCATION: location,\
                     utils.DICT_KEY_MOREINFO: get_int_uuid_more_info(item_url)[1] }
        print "NO LCDAM_contenido DETECTED!!!"
    
    image_list = itemsoup.find("ul", "ad-thumb-list")
    if image_list:
        images = [root_uri+link.get('src') for link in image_list.findAll('img')]
        item_dict[utils.DICT_KEY_IMAGES] = images
    
    redes = itemsoup.find(id="iconosredes")
    if redes:
        iconos = redes.findAll("a")
        for icono in iconos :
            if icono.get('title') != u"Google Translator":
                item_dict[utils.DICT_KEY_MOREINFO][icono.get('title')] = icono.get('href')
                
    izquierda = itemsoup.find("div", "lfr-column", id="izquierda")
    if izquierda:
        izda = itemsoup.find("div", "lfr-column", id="izquierda").find(id="izquierda")
        for li in izda.findAll("li"):
            if li.get('class') == u'direccion':               
                clean(li, 'br')
                clean(li, 'div')
                location2 = ' '.join([ele.strip().replace('\t', '') for ele in li.contents if len(ele.strip()) > 0])
                item_dict[utils.DICT_KEY_LOCATION2] = location2
            elif li.find("div", "topoemail"):
                clean(li, 'div')
                a = li.find('a')
                if a:
                    item_dict[utils.DICT_KEY_MOREINFO]['e-mail'] = a.get('href').strip()
            elif li.find("div", "topotelefono"):
                clean(li, 'div')
                strong = li.find('strong')
                if strong:
                    item_dict[utils.DICT_KEY_MOREINFO]['telefono'] = strong.string.strip()
            elif li.find("div", "topopaginaoficial"):
                clean(li, 'div')
                a = li.find('a')
                if a:
                    item_dict[utils.DICT_KEY_MOREINFO]['web'] = a.get('href').strip()
                    
    centroDescargas = itemsoup.find("div", id="centroDescargas")
    if centroDescargas:
        liDes = centroDescargas.findAll("li")
        links = []
        for li in liDes:
            enlaces = li.findAll('a')
            print enlaces
            if enlaces:
                print enlaces[1]
                link = enlaces[1].get('href').strip()
                text = enlaces[1].string.strip()
                links.append({"title": text, "href": root_uri+link})
        if links:
            item_dict[utils.DICT_KEY_MOREINFO]['descargas'] = links           
      
    print item_dict
    return item_dict

def process_item_content(content, ext_uuid):
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

    clean(content.p, 'br')
    descriptions = [clean_init_end_cr(unicode(desc)) for desc in content.p.contents if len(desc.replace('\n','')) > 0]
    
    item_dict = {utils.DICT_KEY_EXT_UUID: ext_uuid, \
                 utils.DICT_KEY_INT_UUID: get_int_uuid_more_info(ext_uuid)[0], \
                 utils.DICT_KEY_STARTDATE: datehour_ini[0], \
                 utils.DICT_KEY_TITLE: title, utils.DICT_KEY_LOCATION: place, \
                 utils.DICT_KEY_TYPES: ev_types, utils.DICT_KEY_PUBLICS: publics, utils.DICT_KEY_DESCRIPTIONS: descriptions, \
                 utils.DICT_KEY_MOREINFO: get_int_uuid_more_info(ext_uuid)[1] }
    
    if datehour_ini[1]:
        item_dict[utils.DICT_KEY_STARTTIME] = datehour_ini[1]
    if datehour_end[0] != datehour_ini[0]:
        item_dict[utils.DICT_KEY_ENDDATE] = datehour_end[0]
    if datehour_end[1]:
        item_dict[utils.DICT_KEY_ENDTIME] = datehour_end[1]
    
    #utils.print_item_dict(item_dict)
    print item_dict
    return item_dict
    
    #print "datetimeIni: ", datetime_ini
    #print "datetimeEnd: ", datetime_end
    #print contenido.prettify()
    
def get_int_uuid_more_info(ext_uuid):
    reg = re.search('.+(groupId)=(\d+)&.+(articleId)=(\d+)', ext_uuid)
    if reg:
        int_uuid = {reg.group(1): reg.group(2), reg.group(3): reg.group(4)}
        more_info = {}
        return [int_uuid, more_info]
    
    reg = re.search('.+(idEvento)=(\d+)&.+(dirMaps)=(.+)&(.+)', ext_uuid)
    if reg:
        int_uuid = {u'articleId': reg.group(2)}
        more_info = {reg.group(3): reg.group(4)}
        return [int_uuid, more_info]

    reg = re.search('.+(idArticulo)=(\d+)&.+(dirMaps)=(.+)', ext_uuid)
    if reg:        
        int_uuid = {u'articleId': reg.group(2)}
        more_info = {reg.group(3): reg.group(4)}    
    else:
        int_uuid = {}
        more_info = {}
    return [int_uuid, more_info]        
    


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
    #for e in li.findAll('br'):
    #    e.extract()
    clean(li, 'br')
    li.contents[0] = li.contents[0].replace(del_str, '')
    return [li_content.replace('\t','').strip() for li_content in li.contents if len(li_content.replace('\t','').strip()) > 0]

def clean(content, tag):
    for tag in content.findAll(tag):
        tag.extract()

def clean_init_end_cr(line):
    if line[0] == '\n':
        line = line[1:]
    if line[-1] == '\n':
        line = line[0:-1]
    return line.strip()

if __name__ == '__main__':
    
    #item_url = "http://info.valladolid.es/web/culturayturismo/que-hacer?p_p_id=AgendaN1N2_WAR_AgendaN1N2&p_p_lifecycle=1&p_p_state=maximized&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=1&_AgendaN1N2_WAR_AgendaN1N2_idEvento=163319&_AgendaN1N2_WAR_AgendaN1N2_dirMaps=C%2F+Olimpo+60%2C47008+00+Espana&_AgendaN1N2_WAR_AgendaN1N2_javax.portlet.action=lanzarEnlaceEvento"
    """
    item_url = "http://info.valladolid.es/web/culturayturismo/detallecm?idArticulo=178018&docDescarga=VisitasVerano2013.pdf&migas=10183&dirMaps=C/%20Acera%20de%20Recoletos%20,47004%2000%20Espana"
    print json.dumps(process_item_url(item_url), indent=4)
    
    item_url = "http://info.valladolid.es/web/culturayturismo/detallecm?idArticulo=171814&docDescarga=NoHayDocDetalle&migas=10183&dirMaps=CMNO%20Viejo%20de%20Simancas%2028,47008%2000%20Espana"
    print json.dumps(process_item_url(item_url), indent=4)
    """   
    item_url = "http://info.valladolid.es/web/culturayturismo/que-hacer?p_p_id=AgendaN1N2_WAR_AgendaN1N2&p_p_lifecycle=1&p_p_state=maximized&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=1&_AgendaN1N2_WAR_AgendaN1N2_idEvento=156035&_AgendaN1N2_WAR_AgendaN1N2_dirMaps=PS+de+Zorrilla+101%2C47007+00+Espana&_AgendaN1N2_WAR_AgendaN1N2_javax.portlet.action=lanzarEnlaceEvento"
    print json.dumps(process_item_url(item_url), indent=4)

    item_url = "http://info.valladolid.es/web/culturayturismo/detallecm?idArticulo=170976&docDescarga=NoHayDocDetalle&migas=10183&dirMaps=CRA%20Renedo%20Km%203,7,47011%2000%20Espana"
    print json.dumps(process_item_url(item_url), indent=4)
    
    item_url = "http://info.valladolid.es/web/culturayturismo/que-hacer?p_p_id=AgendaN1N2_WAR_AgendaN1N2&p_p_lifecycle=1&p_p_state=maximized&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=1&_AgendaN1N2_WAR_AgendaN1N2_idEvento=164801&_AgendaN1N2_WAR_AgendaN1N2_dirMaps=AV+de+Salamanca+59%2C47014+00+Espana&_AgendaN1N2_WAR_AgendaN1N2_javax.portlet.action=lanzarEnlaceEvento"
    print json.dumps(process_item_url(item_url), indent=4)
    
    item_url = "http://info.valladolid.es/web/culturayturismo/detallecm?idArticulo=164801&docDescarga=NoHayDocDetalle&migas=10183&dirMaps=AV%20de%20Salamanca%2059,47014%2000%20Espana"
    print json.dumps(process_item_url(item_url), indent=4)



    