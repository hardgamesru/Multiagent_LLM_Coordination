def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0: 
        return []
    word_count = {w.lower():words.count(w) for w in set(words)}
    return sorted(word_count, key=lambda w: (-word_count[w], w))[:k]
