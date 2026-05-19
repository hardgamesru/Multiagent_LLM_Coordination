def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    word_counts = {}
    for word in words:
        word_counts[word.lower()] = word_counts.get(word.lower(), 0) + 1
    sorted_words = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
    return [word[0] for word in sorted_words[:min(k, len(sorted_words))]]
