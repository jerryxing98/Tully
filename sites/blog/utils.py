#coding=utf-8
'''
Created on 2012-1-31

@author: Chine
'''

from datetime import datetime
import re

from django.utils.html import escape

_pagebreak = "<p><!-- pagebreak --></p>"
get_abstract = lambda s: s.split(_pagebreak)[0]

process_comment = lambda content: escape(content).replace('\n', '<br />')

##
# Removes HTML markup from a text string.
#
# @param text The HTML source.
# @return The plain text.  If the HTML source contains non-ASCII
#     entities or character references, this is a Unicode string.

def strip_html(text):
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<":
            return "" # ignore tags
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        elif text[:1] == "&":
            import htmlentitydefs
            entity = htmlentitydefs.entitydefs.get(text[1:-1])
            if entity:
                if entity[:2] == "&#":
                    try:
                        return unichr(int(entity[2:-1]))
                    except ValueError:
                        pass
                else:
                    return unicode(entity, "iso-8859-1")
        return text # leave as is
    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)

def fstr(input, encoding='utf-8'):
    """Force convert """
    import cStringIO, codecs
    s = cStringIO.StringIO()
    w = codecs.getwriter(encoding)(s)
    w.write(input)
    return s.getvalue()

contains_chn_reg = re.compile(u"[\u4e00-\u9fa5]")
def check_is_robot(text):
    if contains_chn_reg.search(text) is None:
        return True
    return False

def get_friend_datestr(dt):
    '''
    dt is instance of datetime.
    '''
    
    diff = datetime.now() - dt
    
    sec_diff = diff.seconds
    days_diff = diff.days
    
    if days_diff < 0:
        return ''
    elif days_diff == 0:
        if sec_diff < 10:
            return '刚刚'
        elif sec_diff < 60:
            return '%d秒前' % sec_diff
        elif sec_diff < 120:
            return '1分钟前'
        elif sec_diff < 3600:
            return '%d分钟前' % (sec_diff / 60)
        elif sec_diff < 7200:
            return '1个小时前'
        else:
            return '%d个小时前' % (sec_diff / 3600)
    elif days_diff == 1:
        return '昨天 %s' % dt.strftime('%H:%M')
    elif days_diff <= 7:
        return '%d天前 %s' % (
            days_diff,
            dt.strftime('%H:%M')
        )
    else:
        return dt.strftime('%Y-%m-%d %H:%M')