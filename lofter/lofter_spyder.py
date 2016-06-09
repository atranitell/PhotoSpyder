# -*- coding: utf-8 -*-
"""
Created on Sun Jun 05 11:31:37 2016

@author: jk
"""

import urllib2
import urlparse
import re
import os
import thread

def start(url):
    res = re.findall('http://(.*?).lofter', url)
    if not os.path.exists(res[0]):
        os.mkdir(res[0])
    name = res[0] + '/'
    get_root_website(url, name)
    
def get_root_website(url, name):
    flag = True
    base_url = url
    previous = []
    while flag:
        url_content = urllib2.urlopen(url).read()
        process(url_content, name)
        res = re.findall('href="\?page=(.*?)">', url_content)
        previous.append(url)
        if len(res) != 0:
            if len(res) == 2:
                url = base_url + '?page=' + res[1]
            else:
                url = base_url + '?page=' + res[0]
            if url in previous:
                break
        else:
            break
        print url
        
def process(url_content, name):
    img_urls = re.findall('<img src="(.*)">', url_content)
    if len(img_urls) == 0:
        img_urls = re.findall('<img src="(.*)" />', url_content)
    count = 0
    for img_url in img_urls:
        try:
          img_data = urllib2.urlopen(img_url).read()
          file_name = os.path.basename(urlparse.urlsplit(img_url)[2])
          output = open(name + '/' + file_name, 'wb')
          output.write(img_data)
          output.close()
          count = count + 1
          print "Downloading num of ", count
        except:
          pass
    

def multi(url_lists):
    for url in url_lists:
        start(url)
        
url_list = []
url_list.append('http://crashzpy.lofter.com/')
url_list.append('http://taoyuaner.lofter.com/')
url_list.append('http://sea350991.lofter.com/')
url_list.append('http://ryogieeeeeee.lofter.com/')
url_list.append('http://nnmnnm.lofter.com/')
url_list.append('http://kyuyomi1101.lofter.com/')
url_list.append('http://naomimiao.lofter.com/')
url_list.append('http://rachelaaaa.lofter.com/')
url_list.append('http://houhuahua.lofter.com/')
url_list.append('http://carmen-wjm.lofter.com/')
start('http://mnnno.lofter.com/')
#multi(url_list)