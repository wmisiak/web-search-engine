import math

from indexer import calculate_idf, calculate_tfidf


def test_calculate_idf():
    document_frequency = {"kot": 2, "pies": 1}
    result = calculate_idf(document_frequency, 2)

    assert math.isclose(result["kot"], 1.0)
    assert math.isclose(result["pies"], math.log(3 / 2) + 1)


def test_calculate_tfidf():
    term_frequency = {"kot": 2, "pies": 1}
    idf_values = {"kot": 1.0, "pies": 2.0}

    result = calculate_tfidf(term_frequency, idf_values)

    assert result["kot"] == round((2 / 3) * 1.0, 8)
    assert result["pies"] == round((1 / 3) * 2.0, 8)


def test_calculate_tfidf_empty_document():
    assert calculate_tfidf({}, {}) == {}