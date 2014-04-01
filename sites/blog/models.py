#coding=utf-8

from datetime import datetime
import urllib, hashlib
import re

from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.sitemaps import ping_google
from django.template import Context, loader

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from filebrowser.fields import FileBrowseField

from utils import get_abstract, strip_html, get_friend_datestr
from managers import *
from social_sync import sync
from mail import send_mail

from social.weibo import client as sina_client
from social.txweibo import client as tx_client
from social.renren import client as renren_client
from social.models import SocialItem

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名')
    slug = models.SlugField()
    order = models.IntegerField(blank=True, null=True, verbose_name='顺序')
    
    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ['order',]
        
    def __unicode__(self):
        return self.name
    
    @permalink
    def get_absolute_url(self):
        return ('blog_category', None, {'slug': self.slug})
    
    def save(self):
        if self.order is None:
            cates = Category.objects.all()
            if cates:
                max_order = cates.order_by('-order')[0]
                self.order = max_order.order + 1
            else:
                self.order = 1
            
        super(Category, self).save()
        
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名')
    slug = models.SlugField()
    
    articles = models.ManyToManyField("Article", through="ArticleTag", verbose_name='文章')
    
    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"
        ordering = ['?']
        
    def __unicode__(self):
        return self.name
    
    @permalink
    def get_absolute_url(self):
        return ('blog_tag', None, {'slug': self.slug})
    
class Article(models.Model):
    STATUS_CHOICE = (
        (1, '编辑'),
        (2, '完成'),
        (3, '失效'),
    )
    
    title = models.CharField(max_length=100, verbose_name='标题')
    slug = models.SlugField(max_length=100)
    content = models.TextField(verbose_name='内容')
    status = models.IntegerField(choices=STATUS_CHOICE, default=1, verbose_name='状态')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified = models.DateTimeField(default=datetime.now, verbose_name='修改时间')
    is_always_above = models.BooleanField(default=False, verbose_name='置顶')
    share = models.BooleanField(default=False, verbose_name='分享到社交网络')
    
    clicks = models.IntegerField(default=0, editable=False, verbose_name='点击次数')
    
    category = models.ForeignKey(Category, verbose_name='分类')
    author = models.ForeignKey('BlogUser', verbose_name='作者')
    
    tags = models.ManyToManyField(Tag, through="ArticleTag", verbose_name='标签')
    comments = generic.GenericRelation('Comment')
    shares = generic.GenericRelation(SocialItem)
    
    # Manager
    objects = models.Manager()
    completed_objects = CompletedArticleManager()
    
    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ['-is_always_above', '-created']
        
    def click_once(self):
        self.clicks += 1
        super(Article, self).save()
        
    def __unicode__(self):
        return self.title
    
    @permalink
    def get_absolute_url(self):
        return ('blog_article', None, {'slug': self.slug})
    
    def __getattr__(self, name):
        if name == "abstract":
            return get_abstract(self.content)
        if name == "visible_comments":
            return self.comments.filter(visible=True)
        
        return super(Article, self).__getattr__(name)
    
class ArticleTag(models.Model):
    article = models.ForeignKey(Article)
    tag = models.ForeignKey(Tag)
    
    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = "文章标签"
        
    def __unicode__(self):
        return unicode(self.tag)
    
class Comment(MPTTModel):
    username = models.CharField(max_length=50, verbose_name='用户名')
    email_address = models.EmailField(verbose_name='邮箱地址')
    site = models.URLField(verify_exists=False, blank=True, verbose_name='站点')
    avatar = models.URLField(blank=True, null=True, verbose_name='头像')
    content = models.TextField(verbose_name='内容')
    post_date = models.DateTimeField(editable=False, default=datetime.now, verbose_name='评论时间')
    visible = models.BooleanField(default=True, verbose_name='是否可见')
    ip = models.IPAddressField(null=True, blank=True, verbose_name='IP地址')
    
    # mptt
    reply_to_comment = models.ForeignKey("self", blank=True, null=True, related_name="children")
    
    # contenttypes
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    comment_obj = generic.GenericForeignKey('content_type', 'object_id')
    
    shares = generic.GenericRelation(SocialItem)
    
    # Managers
    objects = TreeManager()
    to_article_objects = CommentToArticleManager()
    to_blog_user_objects = CommentToBlogUserManager()
    visible_objects = CommentsVisibleManager()
    
    class Meta:
        ordering = ['-post_date']
        verbose_name = '评论'
        verbose_name_plural = '评论'
        
    class MPTTMeta:
        parent_attr = 'reply_to_comment'
        
    def __getattr__(self, name):
        if name == "friend_datestr":
            return get_friend_datestr(self.post_date)
        # avatar
        avatar_reg = re.compile("^avatar_([0-9]+)$")
        if avatar_reg.match(name):
            if self.avatar.startswith('http://www.gravatar.com/'):
                size = avatar_reg.match(name).groups()[0]
                return self.avatar.split('?')[0] + "?s=" + str(size) + "&d=404"
            else:
                return self.avatar
        if name == "is_author":
            return self.email_address == settings.ADMINS[0][1]
        return super(Comment, self).__getattr__(name)
    
    def __unicode__(self):
        return self.content
    
class BlogUser(models.Model):
    small_avatar = FileBrowseField(max_length=40, verbose_name='头像（42×42）')
    info = models.TextField(verbose_name='用户信息')
    # 微博相关
    weibo_access_token = models.CharField(max_length=40, verbose_name='微博access token', blank=True, null=True)
    weibo_access_token_expires = models.BigIntegerField(blank=True, null=True, verbose_name="微博access token过期时间")
    weibo_uid = models.BigIntegerField(blank=True, null=True, verbose_name="微博uid")
    
    user = models.OneToOneField(User)
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        
    def __unicode__(self):
        return self.user.username
    
    def __getattr__(self, name):
        if name == "abstract":
            return get_abstract(self.info)
        
        return super(BlogUser, self).__getattr__(name)
    
class Link(models.Model):
    name = models.CharField(max_length=50, verbose_name='链接名')
    site = models.URLField(verify_exists=False,verbose_name='链接地址')
    
    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'
        
    def __unicode__(self):
        return self.name
    
class BlackList(models.Model):
    ip_address = models.IPAddressField(verbose_name='IP地址')
    
    class Meta:
        verbose_name = '黑名单'
        verbose_name_plural = '黑名单'
        
    def __unicode__(self):
        return self.ip_address
    
class Subscriber(models.Model):
    username = models.CharField(max_length=50, verbose_name="订阅用户")
    email_address = models.EmailField(verbose_name="邮箱地址")
    subscribe_time = models.DateTimeField(auto_now_add=True, verbose_name='订阅时间')
    enabled = models.BooleanField(default=True, verbose_name='是否开启')
    
    # Manager
    objects = models.Manager()
    enabled_objects = EnabledSubscriberManager()
    
    class Meta:
        verbose_name = '订阅用户'
        verbose_name_plural = '订阅用户'
        
    def __unicode__(self):
        return self.username

class ArticleSubscriber(models.Model):
    article = models.ForeignKey(Article)
    subscriber = models.ForeignKey(Subscriber)
    
    class Meta:
        verbose_name = "文章订阅信息"
        verbose_name_plural = "文章订阅信息"
        
    def __unicode__(self):
        return unicode(self.article)

'''
Signals
'''   
@receiver(post_save, sender=Article, dispatch_uid="sina")
def send_weibo(sender, instance, **kwargs):
    article = instance
    blog_user = BlogUser.objects.get(user__username=settings.ADMINS[0][0])
    #sina_client.set_access_token(blog_user.weibo_access_token, blog_user.weibo_access_token_expires)
    
    if settings.ENABLE_WEIBO_ACCOUNT:
        sync(sina_client, article, 1)
    
@receiver(post_save, sender=Article, dispatch_uid="tx")
def send_tx_weibo(sender, instance, **kwargs):
    article = instance
    
    if settings.ENABLE_QQWEIBO_ACCOUNT:
        sync(tx_client, article, 2)
    
@receiver(post_save, sender=Article, dispatch_uid="renren")
def renren_share(sender, instance, **kwargs):
    article = instance
    
    if settings.ENABLE_RENREN_ACCOUNT \
        and article.status == 2 \
        and article.share \
        and article.shares.filter(type=3).count() == 0:
        
        content = u'翻墙乐趣的博客发表了文章《%s》 - %s' % (article.title,
                                              strip_html(article.content[:100]+"..."))
        content = content.encode('utf-8')

        renren_share = renren_client('share.share',
                            url='%s%s' % (settings.SITE, article.get_absolute_url()),
                            comment=content,
                            type=6)
        
        if 'error_code' in renren_share and renren_share['error_code'] != 0:
            return
        
        share_id = renren_share['id'] # 6 in renren api means this is a url
        content_type = ContentType.objects.get(model='article')
        share = SocialItem(share_id=share_id, content_type=content_type, type=3, object_id=article.id)
        share.save()
    
@receiver(post_save, sender=Article, dispatch_uid="ping_google")
def ping_google(sender, instance, **kwargs):
    article = instance
    
    if not settings.DEBUG and article.status == 2:
        try:
            ping_google()
        except:
            pass
        
'''
Signals
'''   
@receiver(post_save, sender=Article, dispatch_uid="subscriber")
def send_subscribers_email(sender, instance, **kwargs):
    article = instance
    
    if settings.ENABLE_EMAIL:
        subject = u'您订阅的【残阳似血的博客】上的文章有了更新'
        from_email = settings.EMAIL_HOST_USER
        t = loader.get_template("blog/coolblue/subscriberemail.html")
        
        for subscriber in Subscriber.enabled_objects.all():
            if ArticleSubscriber.objects.filter(article=article, subscriber=subscriber).count() == 0:
                article_subscriber = ArticleSubscriber(article=article, subscriber=subscriber)
                article_subscriber.save()
                
                to_email = [subscriber.email_address, ]
                
                c = Context({
                    'article': article,
                    'subscriber': subscriber,
                    'parameter': urllib.urlencode({
                                   'email': to_email[0],
                                   'hv': hashlib.md5("%s%s"%(to_email[0], str(subscriber.subscribe_time))).hexdigest()
                                   }),
                    'site': settings.SITE
                })
                html = t.render(c)
                plain_text = strip_html(html)
                send_mail(subject, plain_text, from_email, to_email, html=html)
            
        
@receiver(post_save, sender=Comment, dispatch_uid="send_email")
def send_email(sender, instance, **kwargs):
    comment = instance
    
    if settings.ENABLE_EMAIL and comment.visible == True:
        t = loader.get_template("blog/coolblue/email.html")
        type = 0 if comment.content_type.model == 'article' else 1
        
        c = Context({
            'type': type,
            'comment': comment,
            'site': settings.SITE
        })
        
        html = t.render(c)
        plain_text = strip_html(html)
        
        subject = ''
        to_email = ''
        if not comment.reply_to_comment:
            to_email = [settings.ADMINS[0][1], ]
            if type == 0:
                subject = u'【残阳似血的博客】上的文章刚刚被%s评论了' % comment.username
            else:
                subject = u'【残阳似血的博客】刚刚收到%s的留言' % comment.username
        else:
            to_email = [comment.reply_to_comment.email_address, ]
            if type == 0:
                subject = u'您在【残阳似血的博客】上的评论刚刚被%s回复了' % comment.username
            else:
                subject = u'您在【残阳似血的博客】上的留言刚刚被%s回复了' % comment.username
        
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, plain_text, from_email, to_email, html=html)