import math
from collections import Counter

from crawler import crawl
from database import get_pages, insert_page, page_exists, update_index_structure
from transforms import process_text


def index_page(page: dict) -> bool:
    if page_exists(page["url"]):
        return False

    insert_page(page["url"], page["title"], page["content"])
    return True


def index_pages(pages: list[dict]) -> int:
    indexed = 0

    for page in pages:
        if index_page(page):
            indexed += 1

    return indexed


def calculate_document_frequency(pages: list[dict]) -> dict[str, int]:
    document_frequency = Counter()

    for page in pages:
        term_frequency = process_text(page["content"])
        document_frequency.update(term_frequency.keys())

    return dict(document_frequency)


def calculate_idf(document_frequency: dict[str, int], number_of_documents: int) -> dict[str, float]:
    return {
        token: math.log((number_of_documents + 1) / (frequency + 1)) + 1
        for token, frequency in document_frequency.items()
    }


def calculate_tfidf(term_frequency: dict[str, int], idf_values: dict[str, float]) -> dict[str, float]:
    total_terms = sum(term_frequency.values())

    if total_terms == 0:
        return {}

    return {
        token: round((frequency / total_terms) * idf_values[token], 8)
        for token, frequency in term_frequency.items()
    }


def build_index() -> None:
    pages = get_pages()

    if not pages:
        print("Brak stron do zaindeksowania.")
        return

    document_frequency = calculate_document_frequency(pages)
    idf_values = calculate_idf(document_frequency, len(pages))

    for page in pages:
        term_frequency = process_text(page["content"])
        tfidf = calculate_tfidf(term_frequency, idf_values)
        update_index_structure(page["id"], tfidf)

    print(f"Zbudowano indeks TF-IDF dla {len(pages)} stron.")


def main():
    start_url = input("Podaj adres startowy Wikipedii: ").strip()

    if not start_url.startswith("https://pl.wikipedia.org/wiki/"):
        print("Podaj poprawny adres artykułu z polskiej Wikipedii.")
        return

    pages = crawl(start_url, max_depth=5, max_pages=100, max_links_per_page=2)
    indexed = index_pages(pages)

    print(f"Pobrano stron: {len(pages)}")
    print(f"Nowych stron w indeksie: {indexed}")

    build_index()

if __name__ == "__main__":
    main()