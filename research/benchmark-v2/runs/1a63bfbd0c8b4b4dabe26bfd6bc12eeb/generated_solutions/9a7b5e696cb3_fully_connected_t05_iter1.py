def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    freq = {}
    for w in words:
        w_lower = w.lower()
        freq[w_lower] = freq.get(w_lower, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return [w for w, _ in sorted_words[:min(k, len(freq))]]
