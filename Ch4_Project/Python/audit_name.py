#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 04.11.2017

@author: jstrebel
'''

import xml.etree.cElementTree as ET
from collections import defaultdict
import re

ffw_pat = r'^(FF\s|FFW\s|Freiw\.\s*Feuerwehr)\s*'

ffw_re = re.compile(ffw_pat, re.IGNORECASE | re.UNICODE)
""" a.d. should be expanded to "an der" """

def mapping(ucname):
    ucRet = ucname    
    m = ffw_re.search(ucRet)
    if m:
        ucRet = re.sub(ffw_pat,u"Freiwillige Feuerwehr ",ucRet)
        
    return ucRet 

 
def audit_name(dictset, ucname):
    m = ffw_re.search(ucname)
    if m:
        ffw_type = m.group()
        dictset[ffw_type].add(ucname)
                

def audit(dict_name, etelem):
    """ Receives an element and returns the offending numbers(if any).
    Returns a dictionary with keys:sets""" 
    if etelem.tag == "node" or etelem.tag == "way":
        for tag in etelem.iter("tag"):            
            if tag.attrib['k'] == u"name":
                audit_name(dict_name, tag.attrib['v'])
                
    return dict_name


def update(name):    
    """Cleaning function, returns a unicode string"""
    strRet = mapping(name)
    return strRet
