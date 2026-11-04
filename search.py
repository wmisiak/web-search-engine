import math
from collections import Counter

from database import get_pages
from transforms import remove_stop_words, tokenize


def cosine_similarity(query_vector: dict[str, float], document_vector: dict[str, float]) -> float:
    common_terms = query_vector.keys() & document_vector.keys()

    dot_product = sum(query_vector[token] * document_vector[token] for token in common_terms)
    query_norm = math.sqrt(sum(weight ** 2 for weight in query_vector.values()))
    document_norm = math.sqrt(sum(weight ** 2 for weight in document_vector.values()))

    if query_norm == 0 or document_norm == 0:
        return 0.0

    return dot_product / (query_norm * document_norm)


def calculate_document_frequency(pages: list[dict]) -> dict[str, int]:
    document_frequency = Counter()

    for page in pages:
        document_vector = page["index_structure"] or {}
        document_frequency.update(document_vector.keys())

    return dict(document_frequency)


def create_query_vector(query: str, document_frequency: dict[str, int], number_of_documents: int) -> dict[str, float]:
    tokens = remove_stop_words(tokenize(query))

    if not tokens:
        return {}

    frequencies = Counter(tokens)
    total_terms = sum(frequencies.values())
    query_vector = {}

    for token, frequency in frequencies.items():
        if token not in document_frequency:
            continue

        tf = frequency / total_terms
        idf = math.log((number_of_documents + 1) / (document_frequency[token] + 1)) + 1
        query_vector[token] = tf * idf

    return query_vector


def search(query: str, limit: int = 10) -> list[dict]:
    pages = get_pages()

    if not pages:
        return []

    document_frequency = calculate_document_frequency(pages)
    query_vector = create_query_vector(query, document_frequency, len(pages))

    if not query_vector:
        return []

    results = []

    for page in pages:
        document_vector = page["index_structure"] or {}
        score = cosine_similarity(query_vector, document_vector)

        if score > 0:
            results.append({
                "title": page["title"],
                "url": page["url"],
                "score": score,
            })

    results.sort(key=lambda result: result["score"], reverse=True)

    return results[:limit]


def main():
    query = input("Wpisz zapytanie: ")
    results = search(query)

    if not results:
        print("Brak wyników.")
        return

    print("\nWyniki wyszukiwania:")

    for index, result in enumerate(results, start=1):
        print(f"\n{index}. {result['title']}")
        print(result["url"])
        print(f"Podobieństwo: {result['score']:.4f}")


if __name__ == "__main__":
    main()