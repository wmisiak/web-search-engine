from crawler import crawl
from database import insert_page, page_exists


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
            print(f"Zaindeksowano: {page['title']}")
        else:
            print(f"Pominięto: {page['title']}")

    return indexed


def main():
    start_url = "https://pl.wikipedia.org/wiki/Sztuczna_inteligencja"

    pages = crawl(start_url, max_depth=5, max_pages=100, max_links_per_page=2)
    indexed = index_pages(pages)

    print(f"\nPobrano stron: {len(pages)}")
    print(f"Nowych stron w indeksie: {indexed}")


if __name__ == "__main__":
    main()