queryset = Entity.objects.filter(description__icontains = u'book').exclude(description__icontains = u'bookworm').order_by(u'name', u'description')
