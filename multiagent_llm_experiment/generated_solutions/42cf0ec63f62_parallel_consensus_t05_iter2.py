def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    word_count = {}
    for w in words:
        word_count[w.lower()] = word_count.get(w.lower(), 0) + 1
    unique_words = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
    return [w for w, _ in unique_words[:k]]
