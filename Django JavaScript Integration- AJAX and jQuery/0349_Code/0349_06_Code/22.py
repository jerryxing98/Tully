    match = re.match(ur'EntityEmail_new_(\d+)', html_id)
    if match:
        model = int(match.group(1))
