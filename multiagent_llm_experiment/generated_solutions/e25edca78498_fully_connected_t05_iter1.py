def top_k_frequent(words: List[str], k: int) -> List[str]:
    if k <= 0:
        return []
    
    # Count frequency while ignoring case
    freq = Counter(word.lower() for word in words)
    
    # Sort by frequency descending, then lexicographically ascending
    sorted_words = sorted(freq.keys(), key=lambda x: (-freq[x], x))
    
    return sorted_words[:min(k, len(sorted_words))]
