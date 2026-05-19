from collections import Counter

def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    
    # Count frequencies using Counter with lowercased words
    freq = Counter(word.lower() for word in words)
    
    # Sort based on frequency descending, then alphabetically 
    sorted_words = sorted(freq.keys(), key=lambda x: (-freq[x], x))
    
    # Limit result to min(k, total_unique_words)
    return sorted_words[:min(k, len(sorted_words))]
