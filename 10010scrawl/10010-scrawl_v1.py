#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
cnblogs to jerryminds.info 搬家工具
copyright jerryxing98
jerryminds.info


"""

__VERSION__="1.0"

import sys
import os
import codecs
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup,Tag,CData
import re
import logging
from datetime import datetime,timedelta
import time
from optparse import OptionParser
from string import Template
import pickle
import xml
from xml.sax import saxutils
import json
import xlrd,xlwt
file_excel = xlwt.Workbook()
table = file_excel.add_sheet('10010',cell_overwrite_ok=True)

#data = xlrd.open_workbook('10010_number.xls')
#table = data.sheets()[0]
table.write(0,0,u'电话号码')
table.write(0,1,u'号码预存话费')
table.write(0,2,u'号码备注')
table.write(0,3,u'号码等级')
table.write(0,4,u'号码所在城市')
table.write(0,5,u'是否靓号')

def add_recs(arr,row):
    row=row+1
    '''
    根据输入文件，向excel中添加记录
    '''
    table.write(row,0,arr['NumID'])
    table.write(row,1,arr['NumPreFee'])
    table.write(row,2,arr['NumMemo'])
    table.write(row,3,arr['NumLevel'])
    table.write(row,4,arr['City'])
    table.write(row,5,arr['NiceRuleTag'])
    
def add_rec(recs):
    if test_exist(recs):
        print('Exist!')
    sql_seq='''select count(*) from blog_article'''
    cu.execute(sql_seq)
    seq=cu.fetchall()[0][0]
    id=seq+1
    category_id=get_category(recs)
    arg_list =[id,recs['title'],id,recs['content'],recs['datetime'],recs['datetime'],category_id] 
    sql_cmd = u'''insert into blog_article (id,title,slug,content,status,created
    ,modified,is_always_above,share,clicks,category_id,author_id) values (?,?,?,?,2,?,strftime('%%Y-%%m-%%d %%H:%%M:%%S',?),0,100,1000,?,1)''' 
    print sql_cmd
    cu.execute(sql_cmd,arg_list)
    cx.commit()



def replaceUnicodeNumbers(text):
    rx = re.compile('&#[0-9]+;')
    def one_xlat(match):
        return unichr(int(match.group(0)[2:-1]))
    return rx.sub(one_xlat, text)


  
def post(url, data):  
    req = urllib2.Request(url)
    req.add_header('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.5) Gecko/20070713 Firefox/2.0.0.5')
    data = urllib.urlencode(data)  
    #enable cookie  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
    response = opener.open(req, data)  
    return response.read() 


def get(url,data=None):
    if data:
        print data
        data = urllib.urlencode(data)
        url= '%s?%s' % (url,data)
        print url
        req = urllib2.Request(url)
    else:
        req = urllib2.Request(url)
    req.add_header('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.5) Gecko/20070713 Firefox/2.0.0.5')
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    page = opener.open(req).read()
    return page
    


def fetchEntry(url):
    """
    号码结构
        入口
    |-城市
    |-号码
    |-预存话费
    """
    logging.debug(u"开始加载日志 %s",url)
    page = get(url)
    soup = BeautifulSoup(page)
    logging.debug(u"成功下载日志网页")
    logging.debug(u"获取日志内容\n---------------\n%s",soup.prettify())
    arr={'NumID':'','NumPreFee':'','NumMemo':'','NumLevel':'','City':'','NiceRuleTag':''}
    #title
    temp = soup.prettify()
    if temp :
       temp=replaceUnicodeNumbers(temp.strip())
    else:
        logging.warning("无法提取数据")
    j_temp=json.loads(temp)
    logging.debug(u"\n%s\n",j_temp['moreNumArray'])
    try:
        j_arr=j_temp['moreNumArray']
        for i in range(len(j_arr)):
            if i%6==0: 
                arr['NumID']=j_arr[i]
            elif i%6==1: 
                arr['NumPreFee']=j_arr[i]
            elif i%6==2: 
                arr['NumMemo']=j_arr[i]
            elif i%6==3: 
                arr['NumLevel']=j_arr[i]
            elif i%6==4: 
                arr['City']=j_arr[i]
            elif i%6==5: 
                arr['NiceRuleTag']=j_arr[i]
                logging.debug(u"\n%s\n",arr)
                add_recs(arr,i/6+1)

    except:
        logging.debug(u"===============提取数据出错 堆栈信息================")
        #logging.debug(u"\n%s\n",j_temp)
        logging.debug(u"======================================================================")

def find1stPermalink(srcURL):
    logging.info(u"准备连接10010 %s",srcURL)
    page = urllib2.urlopen(srcURL)
    logging.info(u"连接成功,查找第一页的入口")
    soup = BeautifulSoup(page)
    morediv = soup.find(attrs={"class":"more"})
    if morediv :
        linkNode = morediv.a
    if linkNode :
        linkNodeHref = srcURL.split('com/',1)[0]+'com'+linkNode["href"]
        logging.info("提取到第一页数据URL %s",linkNodeHref)
        return linkNodeHref;
    else :
        logging.error("无法提取数据")
        return False


if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG,
                    format='LINE %(lineno)-4d  %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='cnblogs-mover.log',
                    filemode='w');
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    try:
        fetchEntry('http://num.10010.com/NumApp/chseNumList/serchNums?province=11&cityCode=110&sortType=numAsc')
        file_excel.save('10010_demo.xls')
    except:
        logging.exception(u"未知错误")
        raise

    
