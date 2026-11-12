from collections import Counter

def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    lowered = [w.lower() for w in words]
    counts = Counter(lowered)
    items = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return [word for word, _ in items[:k]]
