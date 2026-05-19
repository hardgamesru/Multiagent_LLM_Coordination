def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    
    # Counting frequencies with lowercase normalization
    counts = Counter(word.lower() for word in words)
    
    # Sort first by frequency descending, then lexicographically ascending
    sorted_words = sorted(counts.keys(), key=lambda w: (-counts[w], w))
    
    return sorted_words[:min(k, len(sorted_words))]
