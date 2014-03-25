@ajax_login_required
def save(request):
    try:
        html_id = request.POST[u'id']
        dictionary = request.POST
    except:
        html_id = request.GET[u'id']
        dictionary = request.GET
    value = dictionary[u'value']
    if not re.match(ur'^\w+$', html_id):
        raise Exception("Invalid HTML id.")
