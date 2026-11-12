def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    word_counts = {}
    for w in words:
        word_counts[w.lower()] = word_counts.get(w.lower(), 0) + 1
    freq_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
    return [w for w, _ in freq_words[:k]]
