import urllib.robotparser
from collections import deque

import requests
from bs4 import BeautifulSoup
from ratelimit import limits, sleep_and_retry


BASE_URL = "https://pl.wikipedia.org"
WIKI_PREFIX = f"{BASE_URL}/wiki/"
ROBOTS_URL = f"{BASE_URL}/robots.txt"

ROBOT_NAME = "WebSearchEngine"
USER_AGENT = "WebSearchEngine/1.0 (educational university project)"

HEADERS = {
    "User-Agent": USER_AGENT
}


def load_robots_parser() -> urllib.robotparser.RobotFileParser:
    response = requests.get(ROBOTS_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(ROBOTS_URL)
    parser.parse(response.text.splitlines())

    return parser


def can_fetch(url: str, robot_parser: urllib.robotparser.RobotFileParser) -> bool:
    return robot_parser.can_fetch(ROBOT_NAME, url)


def extract_links(soup: BeautifulSoup) -> list[str]:
    content = soup.find("div", id="mw-content-text")

    if content is None:
        return []

    links = []

    for link in content.find_all("a", href=True):
        href = link["href"]

        if not href.startswith(WIKI_PREFIX):
            continue

        article = href[len(WIKI_PREFIX):].split("#")[0].split("?")[0]

        if not article or ":" in article or article.endswith("_(ujednoznacznienie)"):
            continue

        links.append(f"{WIKI_PREFIX}{article}")

    return list(dict.fromkeys(links))


@sleep_and_retry
@limits(calls=1, period=1)
def fetch_page(url: str, robot_parser: urllib.robotparser.RobotFileParser) -> dict:
    if not can_fetch(url, robot_parser):
        raise PermissionError(f"robots.txt zabrania pobrania: {url}")

    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    content_element = soup.find("div", id="mw-content-text")
    title_element = soup.find("h1")

    if content_element is None:
        raise RuntimeError(f"Nie znaleziono treści artykułu: {url}")

    if title_element is None:
        raise RuntimeError(f"Nie znaleziono tytułu artykułu: {url}")

    return {
        "url": url,
        "title": title_element.get_text(strip=True),
        "content": content_element.get_text(" ", strip=True),
        "links": extract_links(soup),
    }


def crawl(start_url: str, max_depth: int = 5, max_pages: int = 100, max_links_per_page: int = 2) -> list[dict]:
    robot_parser = load_robots_parser()

    queue = deque([(start_url, 0)])
    visited = set()
    pages = []

    while queue and len(pages) < max_pages:
        url, depth = queue.popleft()

        if url in visited:
            continue

        visited.add(url)

        try:
            page = fetch_page(url, robot_parser)
        except (requests.RequestException, PermissionError, RuntimeError) as error:
            print(f"Błąd: {url} - {error}")
            continue

        pages.append({
            "url": page["url"],
            "title": page["title"],
            "content": page["content"],
        })

        if depth >= max_depth:
            continue

        added_links = 0

        for link in page["links"]:
            if link in visited:
                continue

            queue.append((link, depth + 1))
            added_links += 1

            if added_links >= max_links_per_page:
                break

    return pages


def main():
    start_url = "https://pl.wikipedia.org/wiki/Sztuczna_inteligencja"

    pages = crawl(start_url, max_depth=5, max_pages=100, max_links_per_page=2)

    print(f"Pobrano stron: {len(pages)}")


if __name__ == "__main__":
    main()