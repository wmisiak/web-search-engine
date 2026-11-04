from transforms import calculate_term_frequency, process_text, remove_stop_words, tokenize


def test_tokenize():
    assert tokenize("Sztuczna inteligencja i UCZENIE maszynowe!") == [
        "sztuczna", "inteligencja", "i", "uczenie", "maszynowe"
    ]


def test_remove_stop_words():
    tokens = ["sztuczna", "inteligencja", "i", "uczenie", "maszynowe"]
    assert remove_stop_words(tokens) == ["sztuczna", "inteligencja", "uczenie", "maszynowe"]


def test_calculate_term_frequency():
    tokens = ["kot", "pies", "kot"]
    assert calculate_term_frequency(tokens) == {"kot": 2, "pies": 1}


def test_process_text():
    result = process_text("Kot i pies. Kot!")
    assert result == {"kot": 2, "pies": 1}