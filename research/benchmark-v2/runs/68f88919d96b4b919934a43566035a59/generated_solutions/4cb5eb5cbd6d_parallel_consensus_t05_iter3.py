from collections import Counter

def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    lowered = [w.lower() for w in words]
    freq = Counter(lowered)
    sorted_items = sorted(freq.items(), key=lambda item: (-item[1], item[0]))
    return [word for word, _ in sorted_items[:k]]
