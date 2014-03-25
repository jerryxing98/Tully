    try:
        os.rename(directory.settings.DIRNAME + u'/static/images/profile/' +
          string_id, directory.settings.DIRNAME + u'/static/images/profile/' +
          string_id + '.old')
    except OSError:
        pass
    save_file = open(directory.settings.DIRNAME + u'/static/images/profile/' +
      string_id, u'wb')
    for chunk in file.chunks():
        save_file.write(chunk)
    directory.functions.log_message(u'Image for entity ' + string_id +
      u' changed by ' + request.user.username +u'".')
