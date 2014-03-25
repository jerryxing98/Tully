    candidates = []
    for candidate in directory.models.Entity.objects.all():
        candidates.append([candidate, 0])
