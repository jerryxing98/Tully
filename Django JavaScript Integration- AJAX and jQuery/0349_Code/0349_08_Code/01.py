class EntityForm(django.forms.ModelForm):
    class Meta:
        model = Entity

class LocationForm(django.forms.ModelForm):
    class Meta:
        model = Location
