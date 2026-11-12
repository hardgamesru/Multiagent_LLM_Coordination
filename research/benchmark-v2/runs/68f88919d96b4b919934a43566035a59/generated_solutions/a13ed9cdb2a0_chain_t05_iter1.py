def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    from collections import Counter
    counts = Counter(w.lower() for w in words)
    items = list(counts.items())
    items.sort(key=lambda x: (-x[1], x[0]))
    return [w for w, _ in items[:k]]
