    (ur'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    (ur'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (ur'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (ur'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
