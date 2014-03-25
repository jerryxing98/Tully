@ajax_login_required
def save(request):
    try:
        html_id = request.POST[u'id']
        value = request.POST[u'value']
    except:
        html_id = request.GET[u'id']
        value = request.GET[u'value']
    if not re.match(ur'^\w+$', html_id):
        raise Exception(u'Invalid HTML id.')
