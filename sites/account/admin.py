# __*__ coding:utf-8 __*__

from django.contrib import admin
from models import Profile
'''
class BookmarkAdmin(admin.ModelAdmin):
    pass

    list_display = {'title','link','user','date','description','shared'}
    search_fields = {'title',}

class TagAdmin(admin.ModelAdmin):
    list_display = {'name',}

class LinkAdmin(admin.ModelAdmin):
    list_display = {'url'}
    search_fields = {'url',}
'''
#admin.site.register(Test)



#将Model 在djangoAdmin中注册 （两个条件 1.在model中重写 Admin内部类,Meta内部类 2.编写 ModelManger方法）
#admin.site.register(MyProfile)
#admin.site.register(CaptchaStorage)
#admin.site.register(RegistrationProfile)

