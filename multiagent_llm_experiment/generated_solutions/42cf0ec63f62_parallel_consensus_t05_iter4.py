def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    freq = {}
    for w in words:
        word = w.lower()
        freq[word] = freq.get(word, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return [word for word, _ in sorted_words[:k]]
