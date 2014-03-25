    for entry in result:
        score = 0
        for word in split_query:
            if re.match(ur'(?ui)\b' + word + ur'\b'):
                score += 1
        entry[u'score'] = score
    def compare(a, b):
        if cmp(a[u'score'], b[u'score']) == 0:
            return cmp(a[u'name'], b[u'name'])
        else:
            return -cmp(a[u'score'], b[u'score'])
    results.sort(compare)
