def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    
    # Counting frequencies with case normalization
    freq = Counter(word.lower() for word in words)
    
    # Sorting based on (-frequency, word), so higher frequency comes first 
    # but within same frequency, lower alphabetic value comes first
    sorted_words = sorted(freq.keys(), key=lambda w: (-freq[w], w))
    
    # Truncate to at most k elements
    return sorted_words[:min(k, len(sorted_words))]
