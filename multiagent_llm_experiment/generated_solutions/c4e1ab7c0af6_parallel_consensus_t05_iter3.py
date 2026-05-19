def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    
    # Counting frequencies while normalizing case
    freq = Counter(word.lower() for word in words)
    
    # Sort first by negative count (descending), then alphabetically 
    sorted_words = sorted(freq.keys(), key=lambda w: (-freq[w], w))
    
    return sorted_words[:min(k, len(sorted_words))]
