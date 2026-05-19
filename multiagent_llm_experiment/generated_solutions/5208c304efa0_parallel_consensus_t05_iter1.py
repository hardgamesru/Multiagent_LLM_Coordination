from collections import Counter

def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    
    # Counting frequencies case insensitively
    freq = Counter(word.lower() for word in words)
    
    # Sorting by (-frequency, lowercase_word), ensuring stable sorting
    sorted_words = sorted(freq.keys(), key=lambda w: (-freq[w], w))
    
    # Return up to k elements but no more than available unique words
    return sorted_words[:min(k, len(sorted_words))]
