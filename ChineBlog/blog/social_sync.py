#coding=utf-8
'''
Created on 2012-2-15

@author: Chine
'''

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from ChineBlog.social.weibo import client as sina_client
from ChineBlog.social.models import SocialItem
from utils import strip_html

MAX_WORDS = 140

def get_sync_content(article, client, social_type):
    # Title
    title = article.title
    title_count = sina_client.count_words(title)
    
    # Short url
    url = '%s%s' % (settings.SITE, article.get_absolute_url())
    if hasattr(client, 'get_short_url'):
        short_url = client.get_short_url(url)
    else:
        short_url = url
    short_url_count = sina_client.count_words(short_url)
    
    # Base content
    base = u"发表了文章《》 - ... "
    base_count = sina_client.count_words(base)
    
    rest_count = MAX_WORDS - title_count - short_url_count - base_count
    
    rest_content = ''
    for word in iter(strip_html(article.content)):
        rest_count -= sina_client.count_words(word)
        threshold = 0 if not social_type==2 else 3
        if rest_count < threshold:
            break
        rest_content += word
        
    content = u"发表了文章《%s》 - %s... %s" % (title, rest_content, short_url)
    return content
        
def sync(client, article, social_type):
    if article.status == 2 \
        and article.share \
        and article.shares.filter(type=social_type).count() == 0:
        
        share_id = client.update_status(get_sync_content(article, client, social_type))
        
        content_type = ContentType.objects.get(model='article')
        share = SocialItem(share_id=share_id, content_type=content_type, type=social_type, object_id=article.id)
        share.save()