from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from timeline import views
from timeline import eventviews as eviews

urlpatterns = patterns('',
    url(r'^$', views.index, name='timeline_idx'),
    #timeline hot list
    url(r'^hot/$', views.hot, name='timeline_hot'),
    #timeline recommend list
    url(r'^recommend/$', views.recommend, name='timeline_recommend'),
    #timeline last list
    url(r'^last/$', views.last, name='timeline_last'),
    #timeline random list
    url(r'^random/$', views.random, name='timeline_random'),
    #timeline all tags list
    url(r'^tags/$', views.tags, name='timeline_tags'),
    #timeline tagname list
    url(r'^tag/(?P<tag_name>[^/]+)/$', views.tag, name='timeline_tag'),
    
    url(r'^t/(?P<pk>\d+)/fs/$', views.full_screen, name='timeline_full_screen'),
    url(r'^t/(?P<pk>\d+)/e/$', views.embed, name='timeline_embed'),
    

    #timeline_detail
    url(r'^t/(?P<pk>\d+)/$', views.detail, name='timeline_detail'),
    #
    url(r'^t/(?P<pk>\d+)/edit/$', views.edit, name='timeline_edit'),
    url(r'^t/(?P<pk>\d+)/edit/collaboration/$', views.edit_collaboration, name='timeline_edit_collaboration'),
    url(r'^t/(?P<pk>\d+)/add_collaborator_/$', views.add_collaborator_, name='timeline_add_collaborator_'),
    url(r'^t/(?P<pk>\d+)/remove_collaborator_/$', views.remove_collaborator_, name='timeline_remove_collaborator_'),
    url(r'^t/(?P<pk>\d+)/delete/$', views.delete, name='timeline_delete'),
    url(r'^t/(?P<pk>\d+)/postcomment_/$', views.postcomment_, name='timeline_postcomment_'),
    url(r'^t/(?P<pk>\d+)/events/json_/$', views.events_json_, name='timeline_events_json_'),
    url(r'^t/(?P<pk>\d+)/events/sjson_/$', views.events_sjson_, name='timeline_events_sjson_'),
    url(r'^t/(?P<pk>\d+)/attachs/$', views.attachs, name='timeline_attachs'),
    url(r'^t/(?P<pk>\d+)/attach/upload/$', views.attach_upload, name='timeline_attach_upload'),
    url(r'^t/(?P<pk>\d+)/attachs_/$', views.attachs_, name='timeline_attachs_'),
    url(r'^t/(?P<pk>\d+)/attach/upload_/$', views.attach_upload_, name='timeline_attach_upload_'),
    url(r'^t/(?P<pk>\d+)/attach/delete_/$', views.attach_delete_, name='timeline_attach_delete_'),
    url(r'^t/(?P<pk>\d+)/attach/change_descn_/$', views.attach_change_descn_, name='timeline_attach_change_descn_'),
    url(r'^t/$', TemplateView.as_view(template_name='base_site.html')),
    url(r'^t/new/$', views.new, name='timeline_new'),
    url(r'^t/(?P<pk>\d+)/addevent_/$', views.addevent_, name='timeline_addevent_'),
    
    #timeline all events
    url(r'^t/(?P<pk>\d+)/events/$', views.events, name='timeline_events'),
)

urlpatterns += patterns('',
    url(r'^event/delete_/$', eviews.delete_, name='event_delete_'),
    url(r'^event/json_/$', eviews.json_, name='event_json_'),
    url(r'^event/edit_/$', eviews.edit_, name='event_edit_'),
)
