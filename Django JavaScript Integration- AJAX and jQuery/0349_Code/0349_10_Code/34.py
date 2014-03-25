def create_user(request):
    if settings.SHOULD_ALLOW_USERS_TO_CREATE_ACCOUNTS:
        username = request.REQUEST[u'new_username']
        email = request.REQUEST[u'new_email']
        password = request.REQUEST[u'new_password']
        if username and email and password:
            user = User.objects.create_user(username, email, password)
            user.save()
    return HttpResponse(u'')
