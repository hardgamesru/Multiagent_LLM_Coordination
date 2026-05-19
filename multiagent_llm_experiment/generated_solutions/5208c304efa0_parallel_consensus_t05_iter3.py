from collections import Counter

def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    
    # Counting frequencies while normalizing to lowercase
    freq = Counter(word.lower() for word in words)
    
    # Sorting by (-frequency, word), where frequency negation ensures descending order 
    sorted_freq = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    
    # Select up to k items; ensure we don't exceed available unique words
    result = [word for word, _ in sorted_freq[:min(k, len(sorted_freq))]]
    
    return result
