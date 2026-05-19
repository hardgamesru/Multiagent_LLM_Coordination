from collections import Counter

def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    
    # Count frequency of each word (case-insensitive)
    counter = Counter(word.lower() for word in words)
    
    # Sort by frequency descending then lexicographically ascending
    sorted_words = sorted(counter.keys(), key=lambda x: (-counter[x], x))
    
    # Return up to k elements or all available unique words
    return sorted_words[:k]
