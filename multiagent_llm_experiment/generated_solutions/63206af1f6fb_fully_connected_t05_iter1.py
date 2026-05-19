def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    word_counts = {}
    for w in words:
        word_counts[w.lower()] = word_counts.get(w.lower(), 0) + 1
    freq_word_list = [(count, word) for word, count in word_counts.items()]
    freq_word_list.sort(key=lambda x: (-x[0], x[1]))
    return [word for count, word in freq_word_list[:k]]
