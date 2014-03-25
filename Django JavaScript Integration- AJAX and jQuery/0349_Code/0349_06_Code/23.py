        email = directory.models.EntityEmail(email = value, entity =
          directory.models.Entity.objects.get(pk = model))
        email.save() 
