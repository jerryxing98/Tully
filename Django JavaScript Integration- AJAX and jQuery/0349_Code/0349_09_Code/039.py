        tokens = re.split(ur'(?u)[^-\w]', raw)
    except TypeError:
        tokens = raw
    while u'' in tokens:
        tokens.remove(u'')
    try:
        matches = re.split(ur'(?u)[^-\w]', query)
    except TypeError:
        tokens = query
    while u'' in matches:
        matches.remove(u'')
    for token in tokens:
        for match in matches:
            if token.lower() == match.lower():
                result += 1
    return result
