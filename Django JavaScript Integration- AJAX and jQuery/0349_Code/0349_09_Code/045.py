    for token in tokens:
        new_candidates = []
        for candidate in candidates:
            if directory.functions.score(candidate[0], token) > 0:
                candidate[1] += directory.functions.score(candidate[0], token)
                new_candidates.append(candidate)
        candidates = new_candidates
