'''
Created on 29/06/2013

@author: raul
'''

DICT_KEY__ID =          "_id"
DICT_KEY_EXT_UUID =     "ext_uuid"
DICT_KEY_INT_UUID =     "int_uuid"
DICT_KEY_TITLE =        "title"
DICT_KEY_LOCATION =     "location"
DICT_KEY_LOCATION2 =    "location2"
DICT_KEY_STARTDATE =    "startDate"
DICT_KEY_STARTTIME =    "startTime"
DICT_KEY_ENDDATE =      "endDate"
DICT_KEY_ENDTIME =      "endTime"
DICT_KEY_TYPES =        "types"
DICT_KEY_PUBLICS =      "publics"
DICT_KEY_DESCRIPTIONS = "descriptions"
DICT_KEY_MOREINFO =     "moreInfo"
DICT_KEY_IMAGES =       "images"

JSON_DICT_KEYS = [DICT_KEY__ID, DICT_KEY_EXT_UUID, DICT_KEY_INT_UUID, \
                  DICT_KEY_TITLE, DICT_KEY_LOCATION, DICT_KEY_LOCATION2,\
                  DICT_KEY_STARTDATE, DICT_KEY_STARTTIME, \
                  DICT_KEY_ENDDATE, DICT_KEY_ENDTIME, \
                  DICT_KEY_TYPES, DICT_KEY_PUBLICS, DICT_KEY_DESCRIPTIONS, \
                  DICT_KEY_MOREINFO, DICT_KEY_IMAGES]

def print_item_dict(item_dict):
    print "ext_uuid:    ", item_dict[DICT_KEY_EXT_UUID]
    print "title:       ", item_dict[DICT_KEY_TITLE]
    print "place:       ", item_dict[DICT_KEY_LOCATION]
    if item_dict.has_key(DICT_KEY_LOCATION2):    
        print "(2)          ", item_dict[DICT_KEY_LOCATION2]
    if item_dict.has_key(DICT_KEY_STARTDATE):
        print "dateIni:     ", item_dict[DICT_KEY_STARTDATE]
    if item_dict.has_key(DICT_KEY_STARTTIME):
        print "hourIni:     ", item_dict[DICT_KEY_STARTTIME]
    if item_dict.has_key(DICT_KEY_ENDDATE):
        print "dateEnd:     ", item_dict[DICT_KEY_ENDDATE]
    if item_dict.has_key(DICT_KEY_ENDTIME):        
        print "hourEnd:     ", item_dict[DICT_KEY_ENDTIME]
    if item_dict.has_key(DICT_KEY_TYPES):
        print_array(item_dict[DICT_KEY_TYPES], "Tipo de evento")
    if item_dict.has_key(DICT_KEY_PUBLICS):
        print_array(item_dict[DICT_KEY_PUBLICS], "Publico objetivo")
    if item_dict.has_key(DICT_KEY_DESCRIPTIONS):
        print_array(item_dict[DICT_KEY_DESCRIPTIONS], "Descripcion")
    print"--------------------------------------------------------------------------------"

def print_array(array, array_name):
    print array_name, "[", len(array), "]:"
    for i, array_ele in enumerate(array):
        print "\t(", i, ")", array_ele

if __name__ == '__main__':
    pass