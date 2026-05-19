def top_k_frequent(words: List[str], k: int) -> List[str]:
    if k <= 0:
        return []
    
    # Count frequency ignoring case by converting to lowercase
    counts = Counter(word.lower() for word in words)
    
    # Sort first by frequency (descending), then by lexicographical order
    sorted_words = sorted(counts.keys(), key=lambda w: (-counts[w], w))
    
    # Return up to k elements or all available unique words
    return sorted_words[:k]
