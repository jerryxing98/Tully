@ajax_login_required
def save(request):
    session = request.session.session_key
    username = request.user.username
    try:
        html_id = request.POST[u'id']
        dictionary = request.POST
    except:
        html_id = request.GET[u'id']
        dictionary = request.GET
    value = dictionary[u'value']
    if not re.match(ur'^\w+$', html_id):
        raise Exception("Invalid HTML id.")
    match = re.match(ur'Status_new_(\d+)', html_id)
    if match:
        status = directory.models.Status(entity =
          directory.models.Entity.objects.get(id = int(match.group(1))),
          text = value)
        status.save()
        directory.functions.log_message(u'Status for Entity ' +
          str(match.group(1)) + u' added by: ' + request.user.username +
          u', value: ' + value + u'\n')
