    export = []
    for candidate in candidates:
        if candidate[0].image_mimetype:
            image = True
        else:
            image = False
        export.append(
            {
            u'department': name,
            u'description': candidate[0].description,
            u'id': candidate[0].id,
            u'image': image,
            u'name': candidate[0].name,
            u'title': candidate[0].title,
            })
