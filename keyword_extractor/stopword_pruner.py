def prune_stopwords_from_results(results, stopwords, mode="remove_if_all_stopwords"):
    def is_all_stopwords(term):
        return all(word.lower() in stopwords for word in term.split())

    def is_any_stopword(term):
        return any(word.lower() in stopwords for word in term.split())

    def remove_stopwords_within(term):
        # Remove stopwords from within a phrase, return cleaned phrase
        return " ".join([w for w in term.split() if w.lower() not in stopwords])

    pruned = {}
    for strategy, items in results.items():
        new_items = []
        for item in items:
            if isinstance(item, str):
                if mode == "remove_if_all_stopwords":
                    if not is_all_stopwords(item):
                        new_items.append(item)
                elif mode == "remove_if_any_stopword":
                    if not is_any_stopword(item):
                        new_items.append(item)
                elif mode == "remove_stopwords_within_phrase":
                    cleaned = remove_stopwords_within(item)
                    if cleaned:  # Only add if something remains
                        new_items.append(cleaned)
            elif isinstance(item, (list, tuple)):
                # For n-grams as tuples/lists
                if mode == "remove_if_all_stopwords":
                    if not all(word.lower() in stopwords for word in item):
                        new_items.append(item)
                elif mode == "remove_if_any_stopword":
                    if not any(word.lower() in stopwords for word in item):
                        new_items.append(item)
                elif mode == "remove_stopwords_within_phrase":
                    cleaned = [w for w in item if w.lower() not in stopwords]
                    if cleaned:
                        new_items.append(tuple(cleaned))
            elif isinstance(item, dict):
                key = 'term' if 'term' in item else 'phrase' if 'phrase' in item else None
                if key:
                    val = item[key]
                    if mode == "remove_if_all_stopwords":
                        if not is_all_stopwords(val):
                            new_items.append(item)
                    elif mode == "remove_if_any_stopword":
                        if not is_any_stopword(val):
                            new_items.append(item)
                    elif mode == "remove_stopwords_within_phrase":
                        cleaned = remove_stopwords_within(val)
                        if cleaned:
                            new_item = item.copy()
                            new_item[key] = cleaned
                            new_items.append(new_item)
                else:
                    new_items.append(item)
            else:
                new_items.append(item)
        pruned[strategy] = new_items
    return pruned