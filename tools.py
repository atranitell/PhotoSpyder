# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:44:32 2016

@author: jk
"""

import urlparse
import os
import urllib2
import re
import requests
import os
import json
import time

#==============================================================================
#   create a sub folder
#   root - folder - subfolder
#   @ folder: folder name
#   @ return: a folder relative path to root
#==============================================================================
def make_dir(folder, subfolder):
    _path = folder + '/' + subfolder      
    # create folder
    if not os.path.exists(folder):
        os.mkdir(folder)
    # create sub folder
    if not os.path.exists(_path):
        os.mkdir(_path)
    # return subfolder path to root
    return _path
    
#==============================================================================
#   save html code to log.txt in root path
#==============================================================================
def save_html(content):
    fp = open('log.txt','w')
    fp.write(content)
    fp.close()