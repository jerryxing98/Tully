def ajax_permission_required(permission):
    def outer_wrap(view_function):
        def wrap(request, *arguments, **keywords):
            if request.user.has_perm(permission):
                return view_function(request, *arguments, **keywords)
            output = json.dumps({ u'not_permitted': True })
            return HttpResponse(output, mimetype = u'application/json')
        return wrap
    return outer_wrap
