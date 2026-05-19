def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    
    # Counting frequencies with case-insensitive comparison
    freq = Counter(word.lower() for word in words)
    
    # Sort first by decreasing frequency then by increasing alphabetical order
    sorted_words = sorted(freq.keys(), key=lambda x: (-freq[x], x))
    
    # Return at most 'k' elements but no more than available unique words
    return sorted_words[:min(k, len(sorted_words))]
