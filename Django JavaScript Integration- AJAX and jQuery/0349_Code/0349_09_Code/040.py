def score(entity, keywords):
    result = 0
    if entity.name:
        result += count_tokens(entity.name, keywords) * \
          directory.settings.NAME_WEIGHT
    if entity.description:
        result += count_tokens(entity.description, keywords) * \
          directory.settings.DESCRIPTION_WEIGHT
    if entity.tags:
        for tag in entity.tags.all():
            result += count_tokens(tag.text, keywords) * \
              directory.settings.TAG_WEIGHT
    if entity.title:
        result += count_tokens(entity.title, keywords) * \
          directory.settings.TITLE_WEIGHT
    if entity.department:
        result += count_tokens(entity.department.name, keywords) * \
          directory.settings.DEPARTMENT_WEIGHT
    if entity.location:
        result += count_tokens(entity.location.name, keywords) * \
          directory.settings.LOCATION_WEIGHT
    for status in directory.models.Status.objects.filter(entity = entity.id):
        result += count_tokens(status.text, keywords) * \
          directory.settings.STATUS_WEIGHT
    return result
