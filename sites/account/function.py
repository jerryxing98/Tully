from django.http import HttpResponse

import json

def ajax_login_required(view_function):
    def wrap(request, *arguments, **keywords):
        if request.user.is_authenticated():
            return view_function(request, *arguments, **keywords)
        output = json.dumps({ 'not_authenticated': True })
        return HttpResponse(output, mimetype = 'application/json')
    wrap.__doc__ = view_function.__doc__
    wrap.__dict__ = view_function.__dict__
    return wrap
