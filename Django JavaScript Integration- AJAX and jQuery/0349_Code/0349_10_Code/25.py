def format_timestamp(timestamp):
    localtime = timestamp.timetuple()
    result = unicode(int(time.strftime(u'%I', localtime)))
    result += time.strftime(u':%M %p, %A %B ', localtime)
    result += unicode(int(time.strftime(u'%d', localtime)))
    result += time.strftime(u', %Y')
    return result
