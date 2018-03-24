#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 03.11.2017

@author: jstrebel
'''

import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict
import re
import codecs
import sys

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
OSM_TEST_FILE = "NEA_District.osm"
KEY = "name"
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
"""Hack to make it possible to redirect UTF-8 output to a file"""


def key_type(element, keycounts , keyvalues):    
    if element.tag == "tag":
        sTagKey = element.get("k")         
        keyvalues[sTagKey] += 1
        
        if lower.search(sTagKey)!=None:
            keycounts['lower'] += 1
            return (keyvalues , keycounts)
        elif lower_colon.search(sTagKey)!=None:            
            keycounts['lower_colon'] += 1
            return (keyvalues , keycounts)
        elif problemchars.search(sTagKey)!=None:            
            keycounts['problemchars'] += 1
            return (keyvalues , keycounts)
        else:
            keycounts['other'] += 1
            return (keyvalues , keycounts)
    return (keyvalues , keycounts)

def tag_value(element, strKey):
    """Returns postcode string"""
    strValue =u""    
    if element.tag == "tag":
        sTagKey = element.get("k")
        sTagValue = element.get("v")        
        if sTagKey!=None:
            if sTagKey == strKey:
                strValue = sTagValue                                
    return strValue

def process_map(filename):
    # keycounts = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    # tag_types = defaultdict(int)        
    tkeys = defaultdict(int)        
    dict_tagvalues = defaultdict(int)
    
    with open(filename, 'r') as xml_file:
            for _, element in ET.iterparse(xml_file):
                dict_tagvalues[tag_value(element, KEY)] += 1
                #tkeys , keycounts = key_type(element, keycounts, tkeys)
                #tag_types[element.tag] += 1        
        
    pprint.pprint(KEY+':')
    pprint.pprint(dict_tagvalues)
    for k , v in dict_tagvalues.iteritems():
        print k + u" | " + v
    
    pprint.pprint("Tag Key: \n")
    for (k,v) in tkeys.iteritems():
        print k,v

def test():    
    process_map(OSM_TEST_FILE)
        
if __name__ == '__main__':
    test()
    