# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:24:37 2016

@author: jk
"""

import urlparse
import os
import urllib2
import re
import requests
import json
import time
from utils import tools

#==============================================================================
#   person information
#==============================================================================
class zhihu_profile:
    __url = '' # person website
    __url_ans = '' # answer website
    __path_pic = '' # a path to root for saving pictures
    __i_name = '' # nickname
    __i_name_id = '' # userid
    __i_gender = '' # female
    __i_location = '' # living in
    __i_occupy = '' # major in
    __num_agree = 0 # agree number
    __num_thank = 0 # thanks number
    __num_ans = 0 # answer number
    __num_qus = 0 # question number
    __num_ans_page = 0 # answer page number
    __zhihu_url = 'https://www.zhihu.com'
    __i_dict = {}
    
#==============================================================================
#   initailize user website
#   @ url : https://www.zhihu.com/people/qiao-josua (like this)
#==============================================================================
    def __init__(self, url):
        # constuctor basic info
        self.__url = url
        self.__i_name_id = os.path.basename(url)
        self.__get_basic_info()
    
    def __get_basic_info(self):
        url_content = urllib2.urlopen(self.__url).read()
        # praise the nickname
        res = re.findall('<span class="name">(.*?)</span>', url_content)
        self.__i_name = res[0]
        # praise the gender
        res = re.findall('<i class="icon icon-profile-(.*?)"></i></span>', url_content)
        self.__i_gender = res[0]
        # praise location
        res = re.findall('<span class="location item" title="(.*?)">', url_content)
        self.__i_location = res[0]
        # praise occupy
        res = re.findall('<span class="business item" title="(.*?)">', url_content)
        self.__i_occupy = res[0]
        # agree number
        res = re.findall('<strong>(.*?)</strong>赞同</span>', url_content)
        self.__num_agree = res[0]
        # thanks number
        res = re.findall('<strong>(.*?)</strong>感谢</span>', url_content)
        self.__num_thank = res[0]
        # answer number
        res = re.findall('回答\n<span class="num">(.*?)</span>', url_content)
        self.__num_ans = res[0]
        # question number
        res = re.findall('提问\n<span class="num">(.*?)</span>', url_content)
        self.__num_qus = res[0]
        # answer page number
        self.__num_ans_page = self.__get_anspage_num()
        # cluster
        self.__i_dict = {'nickname':self.__i_name, 'gender':self.__i_gender, 'location':self.__i_location, \
                       'occupy':self.__i_occupy, 'agree num':self.__num_agree, 'thanks num':self.__num_thank, \
                       'answer num':self.__num_ans, 'question num':self.__num_qus, 'answer page num':self.__num_ans_page}

#==============================================================================
#   print user basic information to screen           
#==============================================================================
    def print_info(self, save=False, filename=''):
        print 'person website: ', self.__url
        print 'nickname: ', self.__i_name
        print 'user id: ', self.__i_name_id
        print 'gender: ', self.__i_gender
        print 'location: ', self.__i_location
        print 'occupy: ', self.__i_occupy
        print 'agree number: ', self.__num_agree
        print 'thanks number: ', self.__num_thank
        print 'answer number: ', self.__num_ans
        print 'question number: ', self.__num_qus
        print 'answer page: ', self.__num_ans_page, '\n'
        # save to log
        if save == True:
            if filename == '' : filename = self.__i_name_id
            fp = open( filename + '.txt', 'w')
            for i in self.__i_dict.keys():
                info = i + ': ' + str(self.__i_dict[i]) + '\n'
                fp.write(info)
            fp.close()

#==============================================================================
#   acquire answers page number in order to get post    
#==============================================================================
    # acquire the amount number of user answers page
    def __get_anspage_num(self):
        url_content = urllib2.urlopen(self.__url+'/answers').read()
        res = re.findall('\?page=(.*)"', url_content)
        if len(res) == 0: return 0
        else: return int(max(res))

#==============================================================================
#   get one comment picture
#   @ step1: praise each pages answer
#   @ step2: open answer and download pic
#==============================================================================
    def get_all_comments_pic(self):
        self.__pic_count = 0
        # constructor folder
        self.__path_pic = tools.make_dir('profile', self.__i_name_id)
        # acquire each pages answer
        print '\nReady to Download Pictures'
        if self.__num_ans_page == 0:
            content = urllib2.urlopen(self.__url + '/answers').read()
            self.__get_one_comments_pic(content)
        else:
            for i in range(self.__num_ans_page):
                print 'Praise page # ', i
                content = urllib2.urlopen(self.__url+'/answers?from=profile_answer_card&page='+str(i+1)).read()
                self.__get_one_comments_pic(content)
    
    def __get_one_comments_pic(self, content):
        question_list = re.findall('<a class="question_link" href="(.*)">', content)
        for pic_name in question_list:
            comment = urllib2.urlopen(self.__zhihu_url + pic_name).read()     
            imagelist = re.findall('<img src="(.*?)" data-rawwidth=', comment)
            true_imglist = []
            for i in imagelist:
                base = os.path.basename(i)
                if base.find('_b.') != -1:
                    true_imglist.append(i)
            
            for i in true_imglist:
                try:
                  img_data = urllib2.urlopen(i).read()
                  file_name = os.path.basename(urlparse.urlsplit(i)[2])
                  output = open(self.__path_pic+'/'+file_name, 'wb')
                  output.write(img_data)
                  output.close()
                  self.__pic_count = self.__pic_count + 1
                  print "Downloading num of ", self.__pic_count
                except:
                  pass

#==============================================================================
#   @ function1: catch all pictures in comments of each question
#   @ function2: acquire the answer_name_list in this question
#==============================================================================
class zhihu_comments:
    __url = '' # question url
    __q_id = '' # question id
    __ans_num = '' # answer number
    __path_pic = '' # to save picture
    
    def __init__(self, url):
        # constuctor basic info
        self.__url = url
        self.__q_id = os.path.basename(url)
        self.__path_pic = tools.make_dir('comments', self.__q_id)
        self.__url_content = urllib2.urlopen(url).read()
        self.__ans_num = re.findall('h3 data-num="(.*?)"', self.__url_content)

#==============================================================================
#   function1 catch all pictures in comments of each question
#==============================================================================
    def get_ques_photo(self):
        page_size = 50
        offset = 0
        limits = int(self.__ans_num[0])
        min_size = 100 # 100kb avoid to small picture        
        time_start = time.time()
        count = 0

        while offset < limits:
            print "Processing...", offset
            post_url = "http://www.zhihu.com/node/QuestionAnswerListV2"
            params = json.dumps({
              'url_token': int(self.__q_id),
              'pagesize': page_size,
              'offset': offset
            })
            data = {
              '_xsrf': '',
              'method': 'next',
              'params': params
            }
            header = {
              'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
              'Host': "www.zhihu.com",
              'Referer': self.__url
            }            
            response = requests.post(post_url, data=data, headers = header)
            answer_list = response.json()['msg']
            img_urls = re.findall('img .*?src="(.*?_b.*?)"', ''.join(answer_list))            

            for img_url in img_urls:
                try:
                  img_data = urllib2.urlopen(img_url).read()
                  if len(img_data) > min_size*1024:
                      file_name = os.path.basename(urlparse.urlsplit(img_url)[2])
                      output = open(self.__path_pic + '/' + file_name, 'wb')
                      output.write(img_data)
                      output.close()
                      count = count + 1
                      print "Downloading num of ", count
                except:
                  pass            
              
            offset += page_size            
        time_end = time.time()
        print "Total crawling time is " + str(time_end - time_start) + 's.'

#==============================================================================
#   function2 get all authors of one question
#==============================================================================
    # 获取回答赞数排行列表
    def get_answer_authors(self):
        ans_authors = re.findall('>(.*?)</a><span title=|<span class="name">(.*?)</span><span|<span class="name">(.*?)</span>\n</div>', self.__url_content)
        ans_agree = re.findall('<span class="count">(.*)</span>', self.__url_content)
        # 
        ans_list = [[],[],[]]
        for i in ans_authors:
            for c in i:
                if c != '':
                    k = c
            ans_list[0].append(k)
        
        for i in range(len(ans_list[0])):
            ans_list[1].append(ans_agree[i])
            srch = 'href="(.*)">' + ans_list[0][i] + '</a><span title='
            ans_find = re.findall(srch, self.__url_content)
            ans_list[2].append(ans_find)
            # 输出列表信息
            print ans_list[0][i], ans_list[1][i], ans_list[2][i]
#==============================================================================
#  examples
#==============================================================================
p = zhihu_profile('https://www.zhihu.com/people/qiao-josua')
#p.get_all_comments_pic()
#p.print_info(True)
#p.get_all_comments_pic()    

#q = zhihu_comments('https://www.zhihu.com/question/29298363')
#q.get_ques_photo()
#q.get_answer_authors()
    