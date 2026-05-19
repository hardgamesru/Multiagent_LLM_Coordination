def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    
    # Count frequencies while normalizing case
    freq = Counter(word.lower() for word in words)
    
    # Sort first by decreasing frequency then by increasing lexical order
    sorted_items = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    
    # Extract just the words from the sorted items up to k elements
    result = [item[0] for item in sorted_items[:min(k, len(sorted_items))]]
    
    return result
