#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
hi.baidu.com to wordpress 搬家工具
copyright yhustc
http://www.yhustc.com


Modified by jianjun
tonynju.iteye.com
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
    |-标题
    |-时间日期
    |-内容
    |-分类
    |-上一篇日志的url
    |-评论
        |-作者
        |-时间日期
        |-内容
    """
    logging.debug(u"开始加载日志 %s",url)       
    
    req = urllib2.Request(url)
    req.add_header('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.5) Gecko/20070713 Firefox/2.0.0.5')
    page = urllib2.build_opener().open(req).read()
    soup = BeautifulSoup(page)
    logging.debug(u"成功下载日志网页")
    logging.debug(u"获取日志内容\n---------------\n%s",soup.prettify())
    i={'PrevPermaSerial':'','title':'','content':'','datetime':'','category':'','comments':[]}
    #title
    temp = soup.findAll(attrs={"class":"tit"})[1]
    if temp :
       i['title']=replaceUnicodeNumbers(temp.string.strip())
       logging.debug(u"提取标题 %s",i['title'])
    else:
        logging.warning("无法提取标题")
    #datetime
    temp = soup.find(attrs={"class":"date"})
    if temp :
        i['datetime']=temp.string.strip()
        logging.debug(u"提取日期 %s",i['datetime'])
    else :
        logging.warning("无法提取日志发表时间")
        sys.exit(2)
    #content
    temp = soup.find(id='blog_text')
    if temp :
        i['content']=u''.join(map(CData,temp.contents))
        logging.debug(u"提取内容成功");
    else:
        logging.warning("无法提取内容")
    #category,选项div里面的第一个a标签就是分类
    temp = soup.find(attrs={"class":"opt"}).findAll('a')[0]
    if temp :
       category = replaceUnicodeNumbers(temp.string.strip())
       i['category'] = category.replace(u'类别：','')
       logging.debug(u"提取分类 %s",i['category'])
       global categories
       categories.add(i['category'])
    else:
        logging.debug(u"没有分类")
    #上一篇日志的ID号是用ajax读取的
    #previous entry link
    match = re.search(r"var pre = \[(.*?),.*?,.*?,'(.*?)'\]", page, re.DOTALL | re.IGNORECASE | re.MULTILINE)
    if match:
        if match.group(1)=="true":
            result = url.split('com/',1)[0]+'com'+match.group(2) 
            logging.debug(u"上一篇日志URL: %s",result)
            i['PrevPermaSerial'] = result
    #comments
    try:
        if mode != 'postsOnly' :
            #暂时只能下载一页评论
            temp = soup.find(id="in_comment")  #comment div
            if temp :
		cmTables = temp.findAll(attrs={"class":"item"})
		for cmTable in cmTables:
		    comment = {'email':'','author':'','comment':'','datetime':'','url':''} #make sure every key is in
		    userAndUrl = cmTable.find(attrs={"class":"user"}).contents[1]
		    match = re.search(r'writecmt\(.*?,.*?,"(.*?)","(.*?)".*?\);', userAndUrl.string, re.DOTALL | re.IGNORECASE | re.MULTILINE)
		    if match:
			comment['author'] = match.group(1)
			emailOrUrl = match.group(2)
			if re.match(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", emailOrUrl, re.DOTALL | re.IGNORECASE | re.MULTILINE):
			    comment['email'] = emailOrUrl
			else:
			    comment['url'] = emailOrUrl
		    comment['comment']=u''.join(map(CData,cmTable.find(attrs={"class":"desc"}).contents))
		    comment['datetime']=cmTable.find(attrs={"class":"date"}).contents[0].string.strip()
		    i['comments'].append(comment)
            logging.debug(u'为此日志共提取 %d 条评论'
                      ,len(i['comments']))
        return i
    except:
        logging.debug(u"===============提取评论出错 堆栈信息================")
        logging.debug(u"-- cmTable")
        logging.debug(cmTable.prettify())        
        logging.debug(u"-- userAndUrl")
        logging.debug(userAndUrl.prettify())
        #logging.debug(soup.prettify())        
        logging.debug(u"======================================================================")
        logging.error("HTML解析出错。可能是因为blog.163.com升级造成HTML格式发生变化。请将LOG文件发送给hn_yh@163.com")
    finally:
	return i

def find1stPermalink(srcURL):
    logging.info(u"准备连接BLOG %s",srcURL)
    page = urllib2.urlopen(srcURL)
    logging.info(u"连接成功,查找第一篇日志的入口")
    soup = BeautifulSoup(page)
    morediv = soup.find(attrs={"class":"more"})
    if morediv :
        linkNode = morediv.a
    if linkNode :
        linkNodeHref = srcURL.split('com/',1)[0]+'com'+linkNode["href"]
        logging.info("提取到第一篇日志的入口URL %s",linkNodeHref)
        return linkNodeHref;
    else :
        logging.error("无法提取日志入口")
        return False

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
    <wp:wxr_version>1.0</wp:wxr_version>
""") #need blogTitle, nowTime, blogURL
    catT = Template(u'''<wp:category><wp:cat_name><![CDATA[${category}]]></wp:cat_name></wp:category>\n''')
    catStr = u''
    for cat in categories:
        catStr+=catT.substitute(category=cat)
    dic['blogTitle'] = saxutils.escape(dic['blogTitle'])
    f.write(t.substitute(dic))
    f.write(catStr)

def parseAndSetEntryDatetime(entry):
    datestr = entry['datetime']   #2011年02月03日 星期四  06:38 P.M.
    datestr = re.sub(r'(\d\d\d\d).*(\d\d).*(\d\d).*(\d\d:\d\d)\s(\w)\.M\.', r'\1-\2-\3 \4 \5M', datestr)
    if datestr[-2:] == 'PM':
        gmt8Time = datetime.strptime(datestr, '%Y-%m-%d %I:%M %p')
    else:
        gmt8Time = datetime.strptime(datestr, '%Y-%m-%d %H:%M %p')
    origPostTime = gmt8Time - timedelta(hours=8)
    entry['pubDate'] = origPostTime.strftime('%a, %d %b %Y %H:%M:00 +0000')
    entry['postDate'] = gmt8Time.strftime('%Y-%m-%d %H:%M:00') #2011-04-08 23:49:20       GMT+8
    entry['postDateGMT'] = origPostTime.strftime('%Y-%m-%d %H:%M:00')


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
<pubDate>${pubDate}</pubDate>
<dc:creator>${entryAuthor}</dc:creator>

        <category><![CDATA[${category}]]></category>

<guid isPermaLink="false"></guid>
<description></description>
<content:encoded><![CDATA[${entryContent}]]></content:encoded>
<wp:post_id>${entryId}</wp:post_id>
<wp:post_date>${postDate}</wp:post_date>
<wp:post_date_gmt>${postDateGMT}</wp:post_date_gmt>
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
    parseAndSetEntryDatetime(entry)   #parse and set time
    itemStr = itemT.substitute(entryTitle=saxutils.escape(entry['title']),
        entryURL='',entryAuthor=user, category=entry['category'],entryContent=entry['content'],entryId=entryId,postDate=entry['postDate'],postDateGMT=entry['postDateGMT'],pubDate=entry['pubDate'],comments=commentsStr)
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
    parser.add_option("-s","--source",action="store", type="string",dest="srcURL",help="source msn/live space address")
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
    elif srcURL:
        permalink = find1stPermalink(srcURL)
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
    if srcURL:
        blogInfoDic['blogURL']=srcURL
    elif startfromURL:
        blogInfoDic['blogURL'] = startfromURL.split('blog/',1)[0]
    else:
        logging.error("错误,参数中应该传入日志入口URL")
        sys.exit(2)
    logging.info(u'日志URL: %s',blogInfoDic['blogURL'])
    blogInfoDic['nowTime']=datetime.now().strftime('%Y-%m-%d %H:%M')
    page = urllib2.urlopen(blogInfoDic['blogURL'])
    soup = BeautifulSoup(page)
    blogInfoDic['blogTitle']=soup.find(attrs={"class":"titlink"}).string.strip()
    logging.debug(u'日志标题: %s',blogInfoDic['blogTitle'])
    exportFileName = 'hibaidu_'+datetime.now().strftime('%m%d%Y-%H%M')+'.xml'
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
                    filename='hi-baidu-mover.log',
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

    
