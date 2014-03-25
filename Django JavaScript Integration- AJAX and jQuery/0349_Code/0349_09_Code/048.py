    first_portion = export[:directory.settings.INITIAL_RESULTS]
    second_portion = export[directory.settings.INITIAL_RESULTS:]
    return render_to_response(u'search_internal.html',
        {
        u'first_portion': first_portion,
        u'second_portion': second_portion,
        u'query': urllib.quote(query),
        })
