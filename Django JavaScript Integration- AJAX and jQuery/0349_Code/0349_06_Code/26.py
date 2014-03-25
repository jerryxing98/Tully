        selected_model = get_model(u'directory', model)
        instance = selected_model.objects.get(pk = id)
        setattr(instance, field, value)
        instance.save()
