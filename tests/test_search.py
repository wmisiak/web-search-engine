import math

from search import cosine_similarity, create_query_vector


def test_cosine_similarity_identical_vectors():
    vector = {"kot": 0.5, "pies": 0.5}

    assert math.isclose(cosine_similarity(vector, vector), 1.0)


def test_cosine_similarity_no_common_terms():
    query = {"kot": 1.0}
    document = {"pies": 1.0}

    assert cosine_similarity(query, document) == 0.0


def test_cosine_similarity_empty_vector():
    assert cosine_similarity({}, {"kot": 1.0}) == 0.0


def test_create_query_vector_stop_words_only():
    document_frequency = {"uczenie": 2}

    result = create_query_vector("i oraz na w", document_frequency, 5)

    assert result == {}


def test_create_query_vector_unknown_word():
    document_frequency = {"uczenie": 2}

    result = create_query_vector("xyzabcqwerty", document_frequency, 5)

    assert result == {}