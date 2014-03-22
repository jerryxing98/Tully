# -*- coding: UTF-8 -*-
from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
from django.conf import settings

from userena.utils import generate_sha1
from attachments.models import Attachment
from easy_thumbnails.fields import ThumbnailerImageField
from taggit.managers import TaggableManager
from django.template import Template, Context
from  django.template.loader  import  get_template 

STATUS_CHOICES = (('draft', u'草稿'), 
    ('pub', u'发布'),
    ('del', u'删除')
)




MTYPE_CHOICES = (
    (1,'HTML'),
    (2,'IMAGE'),
    (3,'TEXT'),
    (4,'VIDEO'),
    (5,'AUDIO'),
)
SHARED_CHOICES = (
    (1,'YES'),
    (2,'NO'),
)

url_help = """
Not a formal URL field. This accepts a string which will have string formatting operations performed on it. Valid key 
mappings for the string formatting includes:
<ul>
  <li><strong>%(url)s</strong> Url to be provided to social bookmarking service</li>
  <li><strong>%(title)s</strong> Title of object being submitted to social bookmarking service</li>  
  <li><strong>%(description)s</strong> Summary or description of the object being submitted</li>    
</ul>
"""

image_help = """
Bookmark image icon stored in media/social_bookmarking/img folder. Stored there so easier to install with fixtures."
"""

js_help = """
Javascript placed here will be inserted in the page in a <script></script> body. Lines will be stripped so make sure that 
you end your lines of code correctly.
"""

_pagebreak = "<p><!-- pagebreak --></p>"
get_abstract = lambda s: s.split(_pagebreak)[0]

def upload_to_image(instance, filename):
    #salt, hash = generate_sha1(instance.id)
    extension = filename.split('.')[-1].lower()
    hash = filename.split('.')[-2]
    return '%(path)s%(hash)s.%(extension)s' % {'path': 'screen_500/',
                                               'hash': hash,
                                               'extension': extension}


def upload_to_thumbnail(instance, filename):
    #103,143
    #salt, hash = generate_sha1(instance.id)
    hash = filename.split('.')[-2]
    extension='jpg_103'
    return '%(path)s%(hash)s.%(extension)s' % {'path': 'thumbnail_103/',
                                               'hash': hash,
                                               'extension': extension}

class Link(models.Model):
    url =  models.URLField(
        blank=False, 
        max_length=255,
        unique=True,
        help_text=url_help
    )
    image = ThumbnailerImageField(help_text=image_help, 
                                  max_length=255, 
                                  blank=False,
                                  upload_to = upload_to_image)



    def __str__(self):
        #定义对象的字符串表示
        return self.url

    ''' 定义内部管理类，使其能被django 的后台管理  '''
    '''
    class Admin:
        pass
    '''

    ''' 指定该数据模型的一些元数据 '''
    class Meta:
        '''  '''
        verbose_name_plural = '链接信息'


    def get_image_url(self):
        if self.image:
            return self.image.url
        return getattr(settings, 'TL_COVER_URL', None)




class BookmarkManager(models.Manager):
    def get_all_bookmarks(self):
        return Bookmark.objects.filter(status='pub')
    def get_hot_bookmarks(self):
        return self.get_all_bookmarks().order_by('-num_views')
    def get_last_bookmarks(self):
        return self.get_all_bookmarks().order_by('-updated_on')
    def get_random_bookmarks(self):
        return self.get_all_bookmarks().order_by('-rec_on')
    def get_recommend_bookmarks(self):
        return self.get_all_bookmarks().order_by('?')
    def get_tag_bookmarks(self):
        return self.get_all_bookmarks().filter(tags__name__in=[tag_name]).order_by('-updated_on')

    '''
    get 
    '''
    def get_first_bookmark_ids_for_link(self):
        sql=' select b.id ' \
            ' from bookmark_bookmark b,(select link_id,min(date) md ' \
            ' from bookmark_bookmark' \
            ' where shared=1 group by link_id) bb ' \
            ' where b.link_id = bb.link_id and date=bb.md';
        #print sql
        cursor = connection.cursor()
        cursor.execute(sql)
        result_list=[row[0] for row in cursor.fetchall()]
        #print result_list
        return result_list

class Bookmark(models.Model):
    title           = models.CharField(max_length=255, blank=False)
    status = models.CharField(u"发布状态", max_length=16, default='draft', choices=STATUS_CHOICES)
    description     = models.CharField(max_length=255, blank=True, help_text="Because some things want it")
    js              = models.TextField(help_text=js_help, blank=True)
    mtype           = models.IntegerField(choices=MTYPE_CHOICES,default=1)
    shared          = models.IntegerField(choices=SHARED_CHOICES,default=1)
    thumbnail       = ThumbnailerImageField(max_length=255,blank=True,upload_to=upload_to_thumbnail)

    num_views = models.IntegerField(u'浏览次数', default=0)
    num_replies = models.PositiveSmallIntegerField(u'回复数', default=0)

    link = models.ForeignKey(Link)
    rec = models.BooleanField(u'推荐', default=False)
    rec_on = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    tags = TaggableManager(blank=True)

    focus_date = models.CharField(u'初始日期', max_length=30, null=True, blank=True)
    objects = BookmarkManager()

    def __getattribute__(self, name):
        if name == "abstract":
            c = Context({'bm':self}) 
            t = get_template('bookmark/feeds/bookmark_feed.html') 
            html=t.render(c)
            return get_abstract(html)
        '''
        if name == "visible_comments":
            return self.comments.filter(visible=True)
        '''
        return super(Bookmark, self).__getattribute__(name)


    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return unicode(self.title)

    def __unicode__(self):
        return self.title


    def update_updated_on(self, commit=True):
        self.updated_on = datetime.now()
        if commit:
            self.save()



    def update_num_replies(self, commit=True):
        self.num_replies = self.bkcomment_set.count()
        if commit:
            self.save()

    def get_cover_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return getattr(settings, 'TL_COVER_URL', None)

    @models.permalink
    def get_absolute_url(self):
        return ('bookmark_detail', (self.pk, ))



class BKComment(models.Model):
    bookmark = models.ForeignKey(Bookmark)
    content = models.TextField()

    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(u'创建日期', auto_now_add=True)

    def __unicode__(self):
        return "%s-%s" % (self.bookmark.title, self.content[:20])
