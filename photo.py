# encoding: utf-8
"""
Created on Sun Mar 13 09:25:47 2016

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

PRE = 'https://www.zhihu.com'

class zhihu:    
    def __make_dir(self, folder):
        self.urlpath_save = folder + '/'+self.urlpath        
        # 创建images文件夹
        if not os.path.exists(folder):
            os.mkdir(folder)
        # 创建问题子目录
        if not os.path.exists(self.urlpath_save):
            os.mkdir(self.urlpath_save)       
    
    def __init__(self, url):
        # 记录问题地址
        self.url = url
        # 短地址
        self.urlpath = os.path.basename(url)
        # html文件
        self.url_content = urllib2.urlopen(url).read()
    
    def config_get_ans(self):
        # 回答数目
        self.answers_num = re.findall('h3 data-num="(.*?)"', self.url_content)
        # 创建图像文件夹
        self.__make_dir('images')    
        
    def config_get_profile(self):
        # 获取用户回答总页数
        self.page_num = self.get_profile_anspage_num()
        # 创建用户文件夹
        self.__make_dir('profile')
        # 处理函数
        self.get_profile_ans_page()
    
    def get_profile_ans_page(self):
        # 打开页面
        if self.page_num == 0:
            content = urllib2.urlopen(self.url+'/answers').read()
            self.get_profile_praise_page_ans(content)
        else:
            for i in range(self.page_num):
                print 'Praise page # ', i
                content = urllib2.urlopen(self.url+'/answers?from=profile_answer_card&page='+str(i+1)).read()
                self.get_profile_praise_page_ans(content)
    
    def get_profile_praise_page_ans(self, content):
        # 解析出该页的所有回答 link
        question_list = re.findall('<a class="question_link" href="(.*)">', content)
        # 对每个回答进行保存照片
        for p in question_list:
            comment = urllib2.urlopen(PRE+p).read()
            # get imagelist        
            imagelist = re.findall('<img src="(.*?)" data-rawwidth=', comment)
            true_imglist = []
            # including some wrong path
            for i in imagelist:
                base = os.path.basename(i)
                if base.find('_b.') != -1:
                    true_imglist.append(i)
            
            count = 0
            for i in true_imglist:
                try:
                  img_data = urllib2.urlopen(i).read()
                  file_name = os.path.basename(urlparse.urlsplit(i)[2])
                  output = open(self.urlpath_save+'/'+file_name, 'wb')
                  output.write(img_data)
                  output.close()
                  count = count + 1
                  print "Downloading num of ", count
                except:
                  pass
            
    # 获取用户回答总页数
    def get_profile_anspage_num(self):
        # 获取回答页信息
        url_ans_content = urllib2.urlopen(self.url+'/answers').read()
        # self.save_html(url_ans_content)
        res = re.findall('\?page=(.*)"', url_ans_content)
        if len(res) == 0:
            return 0
        else:
            return int(max(res))
    
    def save_html(self, content):
        fp = open('log.txt','w')
        fp.write(content)
        fp.close()
    
    # 保存网页html代码
    def save_ans_list(self):
        fp = open(self.urlpath+'.txt','w')
        # 写入html文件
        # fp.write(self.url_content)
        for i in range(len(self.ans_list[0])):
            p = str(self.ans_list[0][i])+'   '+str(self.ans_list[1][i])+'   '+str(self.ans_list[2][i])+'\n'
            fp.write(p)
        fp.close()
        
    # 获取回答赞数排行列表
    def get_answer_authors(self):
        answers_authors = re.findall('>(.*)</a><span title=|<span class="name">(.*)</span><span|<span class="name">(.*)</span', self.url_content)
        answers_agree = re.findall('<span class="count">(.*)</span>', self.url_content)
        self.ans_list = [[],[],[]]
        # 添加用户(包括匿名用户和知乎用户)
        for i in answers_authors:
            for c in i:
                if c != '':
                    k = c
            self.ans_list[0].append(k)
        
        for i in range(len(self.ans_list[0])):
            # 添加赞数
            self.ans_list[1].append(answers_agree[i])
            # 添加答主个人网址
            srch = 'href="(.*)">' + self.ans_list[0][i] + '</a><span title='
            ans_find = re.findall(srch, self.url_content)
            self.ans_list[2].append(ans_find)
            # 输出列表信息
            # print self.ans_list[0][i], self.ans_list[1][i], self.ans_list[2][i]
    
    # 抓取某个问题的图谱
    def get_ques_photo(self):
        page_size = 50
        offset = 0
        limits = int(self.answers_num[0])
        min_size = 100 # 100kb 避免贴图
        
        time_start = time.time()
        #爬取内容
        count = 0
        while offset < limits:
            print "Processing...", offset
            
            post_url = "http://www.zhihu.com/node/QuestionAnswerListV2"
            params = json.dumps({
              'url_token': int(self.urlpath),
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
              'Referer': self.url
            }
            
            response = requests.post(post_url,data=data,headers = header)
            answer_list = response.json()['msg']
            img_urls = re.findall('img .*?src="(.*?_b.*?)"',''.join(answer_list))
            
            for img_url in img_urls:
                #img_url = img_urls[0]
                try:
                  img_data = urllib2.urlopen(img_url).read()
                  if len(img_data) > min_size*1024:
                      file_name = os.path.basename(urlparse.urlsplit(img_url)[2])
                      output = open(self.urlpath_save+'/'+file_name, 'wb')
                      output.write(img_data)
                      output.close()
                      count = count + 1
                      print "Downloading num of ", count
                except:
                  pass
            
            offset += page_size
            
        time_end = time.time()
        print "Total crawling time is " + str(time_end - time_start) + 's.'
                


def get_comment_pic():
    post_photo = zhihu('https://www.zhihu.com/question/22025486')
    post_photo.config_get_ans()
    post_photo.get_answer_authors()
    post_photo.get_ques_photo()
    post_photo.save_ans_list()

def get_profile_pic():
    post_profile = zhihu('https://www.zhihu.com/people/lin-mo-40-68')
    post_profile.config_get_profile()
    
get_comment_pic()