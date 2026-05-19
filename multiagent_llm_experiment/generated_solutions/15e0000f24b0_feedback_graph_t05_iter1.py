from collections import Counter

def top_k_frequent(words: list[str], k: int) -> list[str]:
    if k <= 0:
        return []
    
    # Counting occurrences of each word regardless of case
    counts = Counter(word.lower() for word in words)
    
    # Get the k most common elements based on count; if same count, sort alphabetically
    result = [word for word, _ in sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:k]]
    
    return result
