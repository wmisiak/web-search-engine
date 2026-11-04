import re
from collections import Counter


STOP_WORDS = {
    "a", "aby", "ale", "albo", "bo", "by", "być", "co", "czy", "dla",
    "do", "i", "ich", "jak", "jest", "już", "który", "na", "nie", "o",
    "od", "oraz", "po", "przez", "się", "są", "tak", "to", "w", "we",
    "z", "za", "ze", "że"
}


def tokenize(text: str) -> list[str]:
    return re.findall(r"\b[\wąćęłńóśźż]+\b", text.lower())


def remove_stop_words(tokens: list[str]) -> list[str]:
    return [token for token in tokens if token not in STOP_WORDS and len(token) > 1]


def calculate_term_frequency(tokens: list[str]) -> dict[str, int]:
    return dict(Counter(tokens))


def process_text(text: str) -> dict[str, int]:
    tokens = tokenize(text)
    tokens = remove_stop_words(tokens)
    return calculate_term_frequency(tokens)