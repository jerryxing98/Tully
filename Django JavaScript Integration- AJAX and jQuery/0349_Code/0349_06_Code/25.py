    else:
        match = re.match(ur'^(.*?)_(.*)_(\d+)$', html_id)
        model = match.group(1)[0].upper() + match.group(1)[1:].lower()
        field = match.group(2).lower()
        id = int(match.group(3))
