#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
blog.163.com to wordpress 搬家工具
copyright yhustc
http://www.yhustc.com
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
from datetime import datetime
import time
from optparse import OptionParser
from string import Template
import pickle
import xml
from xml.sax import saxutils
import json

entries = []
categories = set([])
commentId = 10000
entryId = 10000


def replaceUnicodeNumbers(text):
    rx = re.compile('&#[0-9]+;')
    def one_xlat(match):
        return unichr(int(match.group(0)[2:-1]))
    return rx.sub(one_xlat, text)
        
def fetchEntry(url,datetimePattern = '%Y-%m-%d %H:%M',mode='all'):
    """
    日志结构
        入口
    |-上一篇日志的url
    |-标题
    |-内容
    |-时间日期
    |-分类
    |-评论
        |-作者
        |-内容
        |-时间日期
    """
    logging.debug(u"开始加载日志 %s",url)       
    
    req = urllib2.Request(url)
    req.add_header('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.5) Gecko/20070713 Firefox/2.0.0.5')
    page = urllib2.build_opener().open(req).read()
    soup = BeautifulSoup(page)
    logging.debug(u"成功下载日志网页")
    logging.debug(u"获取日志内容\n---------------\n%s",soup.prettify())
    i={'PrevPermaSerial':'','title':'','content':'','datetime':'','category':'','comments':[]}
    #datetime
    temp = soup.find(attrs={"class":"c09"})
    if temp :
        i['datetime']=temp.string.strip()
        logging.debug(u"提取日期 %s",i['datetime'])
    else :
        logging.warning("无法提取日志发表时间")
        sys.exit(2)
    #content
    temp = soup.find(id=re.compile('blogtext_fks_[0-9]+'))
    if temp :
        i['content']=u''.join(map(CData,temp.contents))
        logging.debug(u"提取内容成功");
    else:
        logging.warning("无法提取内容")
    #title
    temp = soup.find(id=re.compile('blogtitle_fks_[0-9]+'))
    if temp :
       i['title']=replaceUnicodeNumbers(temp.string.strip())
       logging.debug(u"提取标题 %s",i['title'])
    else:
        logging.warning("无法提取标题")
    #category
    temp = soup.find(id=re.compile('aBelongClsfks_[0-9]+'))
    if temp :
       i['category']=replaceUnicodeNumbers(temp.string.strip())
       logging.debug(u"提取分类 %s",i['category'])
       global categories
       categories.add(i['category'])
    else:
        logging.debug(u"没有分类")
    #上一篇日志的ID号是用ajax读取的
    #previous entry link
    match = re.search(r"http://blog\.163\.com/js/static/visitorInfo\.js\?host=(.*?)&mode=.*?blogId=fks_(.*?)&.*?&v=", page, re.DOTALL | re.IGNORECASE | re.MULTILINE)
    blogid = ""
    host = ""
    if match:
        result = match.group()
	host = match.group(1)
	blogid = match.group(2)
        req = urllib2.Request(result)
        req.add_header('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.5) Gecko/20070713 Firefox/2.0.0.5')
        page = urllib2.build_opener().open(req).read()
        logging.debug(u"下载日志相关信息成功，准备提取上一篇日志的ID")
        match = re.search(r"sPrevPermaSerial: '(.*?)',", page, re.DOTALL | re.IGNORECASE | re.MULTILINE)
        if match:
            result = match.group(1)
            if result:
                baseURL = url.split('static/',1)[0]+"static/"        
                logging.debug(u"上一篇日志URL: %s%s/",baseURL,result)
                i['PrevPermaSerial'] = baseURL+result+"/"
    #comments
    try:
        if mode != 'postsOnly' :    
            #评论使用AJAX加载,JSON解码
            comUrl = 'http://ud.blog.163.com/'+host+'/dwr/call/plaincall/BlogBean.getCommentsByBlog.dwr?callCount=1&scriptSessionId=%24{scriptSessionId}07da48ea4b7f4035cf30b314900cd6b6&c0-scriptName=BlogBean&c0-methodName=getCommentsByBlog&c0-id=0&c0-param0=string%3Afks_'
            comUrl += blogid
            comUrl += '&c0-param1=string%3A49787692007425111028704&c0-param2=boolean%3Afalse&c0-param3=boolean%3Afalse&batchId=0'
            req = urllib2.Request(comUrl)
            req.add_header('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.5) Gecko/20070713 Firefox/2.0.0.5')
            page = urllib2.build_opener().open(req).read()
            comSoup = BeautifulSoup(page)
            pretty = comSoup.prettify()
            pretty = pretty.replace("\r","")
            pretty = pretty.replace("\n","")
            pretty = pretty.replace("\t","")
            pretty = pretty.replace("\\r","")
            pretty = pretty.replace("\\n","")
            pretty = pretty.replace("\\t","")
            pretty = pretty.replace("\"","\\\"")#先把引号转译
            pretty = pretty.replace("\\\\\"","\"")#真正要用到的引号会变成\\"
            for match in re.finditer(r"gPermaComs.push\({id:(.*?)}", pretty):
		comStr = match.group(1)
		p = re.compile(',(\w+):')
		comStr = p.sub(r',"\1":',comStr)
		comStr = '{"id":'+comStr+'}'
		comObj = json.read(comStr)
		comment = {'email':'','author':'','comment':'','datetime':'','url':''} #make sure every key is in
		comment['email']=comObj['publisherEmail']
		comment['author']=comObj['publisherNickname']
		comment['comment']=u'<![CDATA['+comObj['content']+']]>'
		comment['datetime']=time.strftime(datetimePattern,time.localtime(float(comObj['publishTime'])/1000))
		comment['url']=comObj['publisherUrl']
		i['comments'].append(comment)
            logging.debug(u'为本篇日志提取 %d 条评论'
                      ,len(i['comments']))
    except:
        logging.debug(u"===============提取评论出错,堆栈信息================")
        for index in comObj:
		logging.debug("%s %s",index,comObj[index])
        logging.debug(u"======================================================================")
        logging.error("HTML解析出错。可能是因为blog.163.com升级造成HTML格式发生变化。请将LOG文件发送给hn_yh@163.com")
    finally:
	return i

def exportHead(f,dic,categories=[]):
    t = Template(u"""<?xml version="1.0" encoding="UTF-8"?>
<!--
    This is a WordPress eXtended RSS file generated by Live Space Mover as an export of 
    your blog. It contains information about your blog's posts, comments, and 
    categories. You may use this file to transfer that content from one site to 
    another. This file is not intended to serve as a complete backup of your 
    blog.
    
    To import this information into a WordPress blog follow these steps:
    
    1.    Log into that blog as an administrator.
    2.    Go to Manage > Import in the blog's admin.
    3.    Choose "WordPress" from the list of importers.
    4.    Upload this file using the form provided on that page.
    5.    You will first be asked to map the authors in this export file to users 
        on the blog. For each author, you may choose to map an existing user on 
        the blog or to create a new user.
    6.    WordPress will then import each of the posts, comments, and categories 
        contained in this file onto your blog.
-->

<!-- generator="Live Space Mover 1.0" created="${nowTime}"-->
<rss version="2.0"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.0/"
>

<channel>
    <title>${blogTitle}</title>
    <link>${blogURL}</link>
    <description></description>
    <pubDate>Tue, 30 Nov 1999 00:00:00 +0000</pubDate>
    <generator>163 Blog Mover 1.0</generator>
    <language>en</language>
""") #need blogTitle, nowTime, blogURL
    catT = Template(u'''<wp:category><wp:cat_name><![CDATA[${category}]]></wp:cat_name></wp:category>\n''')
    catStr = u''
    for cat in categories:
        catStr+=catT.substitute(category=cat)
    dic['blogTitle'] = saxutils.escape(dic['blogTitle'])
    f.write(t.substitute(dic))
    f.write(catStr)
    
def exportEntry(f,entry,user):
    commentT = Template(u"""<wp:comment>
<wp:comment_id>${commentId}</wp:comment_id>
<wp:comment_author>${commentAuthor}</wp:comment_author>
<wp:comment_author_email>${commentEmail}</wp:comment_author_email>
<wp:comment_author_url>${commentURL}</wp:comment_author_url>
<wp:comment_author_IP></wp:comment_author_IP>
<wp:comment_date>${commentDate}</wp:comment_date>
<wp:comment_date_gmt>0000-00-00 00:00:00</wp:comment_date_gmt>
<wp:comment_content>${commentContent}</wp:comment_content>
<wp:comment_approved>1</wp:comment_approved>
<wp:comment_type></wp:comment_type>
<wp:comment_parent>0</wp:comment_parent>
</wp:comment>""") #need commentId, commentAuthor, commentEmail, commentURL,commentDate,commentContent
    itemT = Template(u"""<item>
<title>${entryTitle}</title>
<link>${entryURL}</link>
<pubDate>Tue, 30 Nov 1999 00:00:00 +0000</pubDate>
<dc:creator>${entryAuthor}</dc:creator>

        <category><![CDATA[${category}]]></category>

<guid isPermaLink="false"></guid>
<description></description>
<content:encoded><![CDATA[${entryContent}]]></content:encoded>
<wp:post_id>${entryId}</wp:post_id>
<wp:post_date>${postDate}</wp:post_date>
<wp:post_date_gmt>0000-00-00 00:00:00</wp:post_date_gmt>
<wp:comment_status>open</wp:comment_status>
<wp:ping_status>open</wp:ping_status>
<wp:post_name>${entryTitle}</wp:post_name>
<wp:status>publish</wp:status>
<wp:post_parent>0</wp:post_parent>
<wp:menu_order>0</wp:menu_order>
<wp:post_type>post</wp:post_type>
${comments}
</item>
""") #need entryTitle, entryURL, entryAuthor, category, entryContent, entryId, postDate
    global entryId
    global commentId
    commentsStr = u""
    #logging.debug(entry)
    for comment in entry['comments']:
        commentsStr+=commentT.substitute(commentId = commentId,
            commentAuthor = saxutils.escape(comment['author']),
            commentEmail = saxutils.escape(comment['email']),
            commentURL = comment['url'],
            commentDate=comment['datetime'],
            commentContent=comment['comment'])
        commentId-=1
        #logging.debug(comment['comment'])
    #logging.debug(entry['category'])
    itemStr = itemT.substitute(entryTitle=saxutils.escape(entry['title']),
        entryURL='',entryAuthor=user, category=entry['category'],entryContent=entry['content'],entryId=entryId,postDate=entry['datetime'],comments=commentsStr)
    entryId-=1
    #logging.debug(itemStr)
    f.write(itemStr)
    
def exportFoot(f):
    f.write("""
</channel>
</rss>
""")
    f.close()
    
def main():
    #main procedure begin
    parser = OptionParser()
    parser.add_option("-f","--startfrom",action="store", type="string",dest="startfromURL",help="a permalink in source msn/live space address for starting with, if this is specified, srcURL will be ignored.")    
    parser.add_option("-x","--proxy",action="store",type="string",dest="proxy",help="http proxy server, only for connecting live space.I don't know how to add proxy for metaWeblog yet. So this option is probably not useful...")
    parser.add_option("-t","--datetimepattern",action="store",dest="datetimepattern",default="%Y-%m-%d %H:%M",help="The datetime pattern of livespace, default to be %Y-%m-%d %H:%M. Check http://docs.python.org/lib/module-time.html for time formatting codes. Make sure to quote the value in command line.")
    parser.add_option("-l","--limit",action="store",type="int",dest="limit",help="limit number of transfered posts, you can use this option to test")
    parser.add_option("-m","--mode",action="store",type="string",dest="mode",default="all",help="Working mode, 'all' or 'commentsOnly'. Default is 'all'. Set it to 'commentsOnly' if you have used earlier version of this script to move posts. Set it to 'postsOnly' if you can't upload the comments-post page to your dest WordPress blog so can't move comments")
    parser.add_option("-a","--maxDstEntryID",action="store",type="int",default='100',dest="maxDstEntryID",help="Use this parameter to specify the MAX post id of your destination blog")    
    parser.add_option("-u","--userName",action="store",type="string",default='yourusername',dest="user",help="Blog author")    
    (options, args) = parser.parse_args()
    #export all options variables
    for i in dir(options):
        exec i+" = options."+i
    #add proxy
    if proxy:
        proxy_handler = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        logging.info(u"设置代理 %s",proxy)
    #connect src blog and find first permal link
    if startfromURL :
        permalink = startfromURL
        logging.info(u"入口地址 %s",startfromURL)
    else:
        logging.error("错误,必须指定第一条日志的入口URL")
        sys.exit(2)
    #main loop, retrieve every blog entry and post to dest blog
    count = 0
    cacheFile = open('entries.cache','w')
    try:
        while permalink:
            i=fetchEntry(permalink,datetimepattern,mode)   
            entries.append(i)
            pickle.dump(i,cacheFile)
            logging.debug(u"-----------------------")
            if 'PrevPermaSerial' in i :
                    permalink = i['PrevPermaSerial']
            else :
                    break
            count+=1
            if limit and count >= limit : break
    finally:
        cacheFile.close()
    #get blog info and export header
    blogInfoDic = {}
    if startfromURL:
        blogInfoDic['blogURL'] = startfromURL.split('blog/',1)[0]
    else:
        logging.error("错误,参数中应该传入日志入口URL")
        sys.exit(2)
    logging.info(u'日志URL: %s',blogInfoDic['blogURL'])
    blogInfoDic['nowTime']=datetime.now().strftime('%Y-%m-%d %H:%M')
    page = urllib2.urlopen(blogInfoDic['blogURL'])
    soup = BeautifulSoup(page)
    blogInfoDic['blogTitle']=soup.find(attrs={"class":"fs01"}).string.strip()
    logging.debug(u'日志标题: %s',blogInfoDic['blogTitle'])
    exportFileName = '163blog_'+datetime.now().strftime('%m%d%Y-%H%M')+'.xml'
    f = codecs.open(exportFileName,'w','utf-8')
    if f:
        logging.info(u'导出XML文件: %s',exportFileName)
    else:
        logging.error("无法打开可写的导出文件: %s",exportFileName)
        sys.exit(2)
    exportHead(f,blogInfoDic,categories)
    logging.debug(u'导出文件头部')
    #export entries
    for entry in entries:
        exportEntry(f,entry,user)
    #export Foot
    exportFoot(f)
    logging.debug(u'导出文件尾部')
    #Delete cache file
    os.remove('entries.cache')
    logging.info(u"删除缓存文件")
    logging.info(u"%s 日志搬家成功",blogInfoDic['blogURL'])

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG,
                    format='LINE %(lineno)-4d  %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='163-blog-mover.log',
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
        main()
    except:
        logging.exception("未知错误")
        raise

    