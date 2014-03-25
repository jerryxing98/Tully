        directory.functions.log_message(model + u'.' + field + u'(' + str(id) + 
          u') changed by: ' + request.user.username + u' to: ' + value + u'\n')
        return HttpResponse(escape(value))
