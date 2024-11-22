import pytest
from function import get_words_frequency

def test_word_frequency():
    sentence = "bar baz foo foo zblah zblah zblah baz toto bar"
    assert get_words_frequency(sentence, 3) == [("zblah", 3), ("bar", 2), ("baz", 2)]
    assert get_words_frequency(sentence, 2) == [("zblah", 3), ("bar", 2)]

def test_word_frequency_multiple_spaces_and_punctuation():
    sentence = "bar baz foo  foo, zblah zblah. zblah baz : toto bar"
    assert get_words_frequency(sentence, 3) == [("zblah", 3), ("bar", 2), ("baz", 2)]
    
def test_word_frequency_in_alphabetical_order():
    sentence = "z y x w v u t s r q p o n m l k j i h g f e d c b a"
    assert get_words_frequency(sentence, 5) == [("a", 1), ("b", 1), ("c", 1), ("d", 1), ("e", 1)]
    
def test_word_frequency_case_sensitive():
    assert get_words_frequency("foo Foo", 2) == [("Foo", 1), ("foo", 1)]
    
def test_word_frequency_less_words_than_asked():
    assert get_words_frequency("foo", 2) == [("foo", 1)]
    
def test_word_frequency_zero():
    assert get_words_frequency("foo", 0) == []

def test_word_frequency_empty():
    assert get_words_frequency("", 3) == []
    
def test_word_frequency_only_spaces():
    assert get_words_frequency("   ", 3) == []

def test_word_frequency_no_sentence():
    with pytest.raises(ValueError, match="Sentence is empty."):
        get_words_frequency(None, 3)
    
def test_word_frequency_negative():
    with pytest.raises(ValueError, match="n must be a positive integer."):
        get_words_frequency("foo", -1)