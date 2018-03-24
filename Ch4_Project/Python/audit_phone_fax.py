#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 04.11.2017

@author: jstrebel
'''

import xml.etree.cElementTree as ET
from collections import defaultdict
import re

missingplus_re = re.compile(r'^49[ -]?[0-9|\(]', re.IGNORECASE | re.UNICODE)
dash_re = re.compile(r'^\+?49-[0-9|\(]', re.IGNORECASE | re.UNICODE)
""" there should not be a dash between the country code and the rest of the number"""

def mapping(unumber):
    ucRet = unumber    
    m = missingplus_re.search(ucRet)
    if m:
        ucRet = u"+"+unumber    
    m = dash_re.search(ucRet)
    if m:        
        ucRet = ucRet.replace(u"-",u" ",1)    
    return ucRet 

 
def audit_number(dictset, unumber):
    m = missingplus_re.search(unumber)
    if m:
        dictset["missing_plus"].add(unumber)
            
    m = dash_re.search(unumber)
    if m:        
        dictset["surplus_dash"].add(unumber)


def audit_phone(dict_phone, etelem):
    """ Receives an element and returns the offending numbers(if any).
    Returns a dictionary with keys:sets""" 
    if etelem.tag == "node":
        for tag in etelem.iter("tag"):            
            if tag.attrib['k'] == u"phone":
                audit_number(dict_phone, tag.attrib['v'])
                
    return dict_phone

def audit_fax(dict_fax, etelem):
    """ Receives an element and returns the offending numbers(if any).
    Returns a dictionary with keys:sets""" 
    if etelem.tag == "node":
        for tag in etelem.iter("tag"):            
            if tag.attrib['k'] == u"fax":
                audit_number(dict_fax, tag.attrib['v'])                
    return dict_fax

def update(name):    
    """Cleaning function, returns a unicode string"""
    strRet = mapping(name)
    return strRet
