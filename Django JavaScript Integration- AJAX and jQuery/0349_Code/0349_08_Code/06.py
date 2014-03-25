    (ur'^(create/Entity)', views.redirect),
    (ur'^(create/Location)', views.redirect),
    (ur'^manage/Entity/?(\d*)', views.modelform_Entity),
    (ur'^manage/Location/?(\d*)', views.modelform_Location),
