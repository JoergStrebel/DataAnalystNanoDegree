#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Module is based on the classroom quizzes""" 

import xml.etree.cElementTree as ET
from collections import defaultdict
import re

street_type_re = re.compile(r'Str\.$', re.IGNORECASE | re.UNICODE)

mapping = { u"Str.": u"Straße", 
           u"str.": u"straße"}


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == u"addr:street")


def audit(dict_street, etelem):
    """ Receives an element and returns the offending street names (if any).
    Returns a dictionary with keys:sets""" 
    if etelem.tag == "node" or etelem.tag == "way":
        for tag in etelem.iter("tag"):
            if is_street_name(tag):
                audit_street_type(dict_street, tag.attrib['v'])
    return dict_street


def update(name):
    """Cleaning function, that transforms a street name"""
    strRet = name
    for strkey,strval in mapping.iteritems():
        if strkey in name:
            strRet = name.replace(strkey,strval,1)    

    return strRet


