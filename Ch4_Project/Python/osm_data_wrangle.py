#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
osm_data_wrangle -- main program for Chapter 4 project OSM data wrangling

@author:     Jörg Strebel
@contact:    joerg.strebel@bmw.de
'''

import os
import audit_city
import audit_name
import audit_phone_fax
import audit_streetname
import clean_transform_fields
import codecs
import xml.etree.cElementTree as ET
import sys
from collections import defaultdict


from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2017-11-04'
__updated__ = '2017-11-04'

OSMFILENAME = "NEA_District_sample.osm"
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
"""Hack to make it possible to redirect UTF-8 output to a file in the CLI"""

def uc_pretty_print(dictset):
    """Takes a defaultdict(set) and pretty-prints the content"""
    for k in dictset.iterkeys():
        print u"Key: " + k 
        for v in dictset[k]:
            print u"\t" + v 

def audit_process_map(filename):    
    """Process OSM XML file and audit the fields""" 
    dict_street = defaultdict(set)
    dict_phone = defaultdict(set)
    dict_fax = defaultdict(set)
    dict_city = defaultdict(set)
    dict_name = defaultdict(set)
    
    with open(filename, 'r') as xml_file:
        for _, element in ET.iterparse(xml_file):            
            #streets
            dict_street = audit_streetname.audit(dict_street,element) 
            dict_phone = audit_phone_fax.audit_phone(dict_phone, element)
            dict_fax = audit_phone_fax.audit_fax(dict_fax, element)
            dict_city = audit_city.audit(dict_city, element)
            dict_name = audit_name.audit(dict_name, element)
            
            
    print u"Problematic street names: "
    uc_pretty_print(dict_street)
    
    print u"Problematic phone numbers: "
    uc_pretty_print(dict_phone)
    
    print u"Problematic fax numbers: "
    uc_pretty_print(dict_fax)
    
    print u"Problematic city names: "
    uc_pretty_print(dict_city)
    
    print u"Problematic name values in tags: "
    uc_pretty_print(dict_name)

def audit_test():
    """Unit test set for the updated() function""" 
    assert audit_streetname.update(u"Königsstr.") == u"Königsstraße"
    assert audit_phone_fax.update(u"+49-9302-988781") == u"+49 9302-988781" 
    assert audit_city.update(u"Neustadt a.d. Aisch") == u"Neustadt an der Aisch"
    assert audit_city.update(u"Neustadt a.d.Aisch") == u"Neustadt an der Aisch"
    assert audit_city.update(u"Neustadt a. d. Aisch") == u"Neustadt an der Aisch"
    assert audit_name.update(u"FF Ansbach Stadt") == u"Freiwillige Feuerwehr Ansbach Stadt" 
    assert audit_name.update(u"FFW Ansbach Stadt") == u"Freiwillige Feuerwehr Ansbach Stadt"
    assert audit_name.update(u"Freiw. Feuerwehr Ansbach Stadt") == u"Freiwillige Feuerwehr Ansbach Stadt"
        
        
def main(argv=None):
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    #program_version = "v%s" % __version__
    #program_build_date = str(__updated__)
    #program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = u"Start with: python osm_data_wrangle -f <OSM XML source file> [-v]"
 
    try:
        
        # Setup argument parser
        parser = ArgumentParser(description=program_shortdesc, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-f", "--file", dest="filename", action="store", default=OSMFILENAME)
        parser.add_argument("-v", "--validate", dest="bValidate", action="store_true", default=False)
        
        # Process arguments
        args = parser.parse_args()
        hFile = args.filename
        bValFlag = args.bValidate 
        
        # Audit all fields, view their contents        
        audit_process_map(hFile)
        audit_test()
        
        #Clean and transform the fields using the update() function in each module
        clean_transform_fields.process_map(hFile, bValFlag)                                    
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    sys.exit(main())