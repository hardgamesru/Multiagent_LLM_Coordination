from collections import Counter

def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    
    # Counting word frequencies with case-insensitive comparison
    freq = Counter(word.lower() for word in words)
    
    # Sorting first by frequency descending, then alphabetically ascending
    sorted_words = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    
    # Extracting only the words (first element of each tuple), limited by k
    result = [word for word, _ in sorted_words[:k]]
    
    return result
