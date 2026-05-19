from collections import Counter

def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    
    freq = Counter(word.lower() for word in words)
    
    sorted_words = sorted(freq.keys(), key=lambda w: (-freq[w], w))
    
    return sorted_words[:k]
