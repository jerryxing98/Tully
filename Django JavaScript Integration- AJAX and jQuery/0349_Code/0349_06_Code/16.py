def log_message(message):
    log_file = os.path.join(os.path.dirname(__file__),
      directory.settings.LOGFILE)
    open(log_file, u'a').write(time.asctime() + u': ' + message + u'\n')
