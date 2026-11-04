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


def create_query_vector(query: str) -> dict[str, float]:
    tokens = tokenize(query)
    tokens = remove_stop_words(tokens)

    if not tokens:
        return {}

    frequencies = Counter(tokens)
    total_terms = sum(frequencies.values())

    return {
        token: frequency / total_terms
        for token, frequency in frequencies.items()
    }


def search(query: str, limit: int = 10) -> list[dict]:
    query_vector = create_query_vector(query)

    if not query_vector:
        return []

    results = []

    for page in get_pages():
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