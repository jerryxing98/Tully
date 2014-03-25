@ajax_login_required
def ajax_check_login(request):
    output = json.dumps({ u'not_authenticated': False })
    return HttpResponse(output, mimetype = u'application/json')
