class EntityForm(django.forms.ModelForm):
    class Meta:
        model = Entity
        fields = (u'active', u'department', u'description', u'image', u'homepage', u'honorifics', u'name', u'post_nominals', u'phone', u'publish_externally', u'reports_to')
