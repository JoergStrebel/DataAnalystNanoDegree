#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 04.11.2017

@author: jstrebel
'''

import xml.etree.cElementTree as ET
from collections import defaultdict
import re

abbrev_pat = r'\sa\.\s?d\.\s?'
abbrev_re = re.compile(abbrev_pat, re.IGNORECASE | re.UNICODE)
""" a.d. should be expanded to "an der" """

def mapping(ucname):
    ucRet = ucname    
    m = abbrev_re.search(ucRet)
    if m:
        ucRet = re.sub(abbrev_pat,u" an der ",ucRet)
        
    return ucRet 

 
def audit_city(dictset, ucname):
    m = abbrev_re.search(ucname)
    if m:
        abbrev_type = m.group()
        dictset[abbrev_type].add(ucname)
                

def audit(dict_city, etelem):
    """ Receives an element and returns the offending numbers(if any).
    Returns a dictionary with keys:sets""" 
    if etelem.tag == "node" or etelem.tag == "way":
        for tag in etelem.iter("tag"):            
            if tag.attrib['k'] == u"addr:city":
                audit_city(dict_city, tag.attrib['v'])
                
    return dict_city


def update(name):    
    """Cleaning function, returns a unicode string"""
    strRet = mapping(name)
    return strRet
