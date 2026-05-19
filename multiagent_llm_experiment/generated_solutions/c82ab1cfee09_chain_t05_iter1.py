def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    counts = {}
    for word in words:
        normalized = word.lower()
        counts[normalized] = counts.get(normalized, 0) + 1
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [word for word, _ in ordered[:k]]
