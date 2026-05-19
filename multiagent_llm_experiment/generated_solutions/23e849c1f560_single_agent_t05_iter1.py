def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    
    # Count frequency ignoring case
    counter = Counter(word.lower() for word in words)
    
    # Sort by frequency (descending), then lexicographically 
    sorted_words = sorted(counter.keys(), key=lambda x: (-counter[x], x))
    
    return sorted_words[:k]
