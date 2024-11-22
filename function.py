import re

def get_only_letters_and_spaces(sentence: str):
    return re.sub(r'[^a-zA-Z\s]', '', sentence)

def sort_key(item):
    word, frequency = item
    return (-frequency, word)

def get_words_frequency(sentence: str, n: int):
    
    # Check attributes
    if sentence is None:
        raise ValueError("Sentence is empty.")
    if n < 0:
        raise ValueError("n must be a positive integer.")
    if n == 0:
        return []
    
    # Get words frequency
    words = get_only_letters_and_spaces(sentence).split()
    frequencies = {}
    for word in words:
        frequencies[word] = frequencies.get(word, 0) + 1
        
    # Sort words
    sorted_words = sorted(frequencies.items(), key=sort_key)
    return sorted_words[:n]