class EntityForm(django.forms.ModelForm):
    class Meta:
        model = Entity
        exclude = (u'homepage', u'image')
