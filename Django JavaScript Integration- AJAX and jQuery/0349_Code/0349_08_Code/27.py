class EntityForm(django.forms.ModelForm):
    class Meta:
        model = Entity
        fields = (u'name', u'honorifics', u'post_nominals', u'description', u'homepage', u'phone', u'department', u'reports_to', u'active', u'publish_externally')
