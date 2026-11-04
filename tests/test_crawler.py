from bs4 import BeautifulSoup

from crawler import BASE_URL, extract_links


def test_extract_links():
    html = f"""
    <div id="mw-content-text">
        <a href="{BASE_URL}/wiki/Uczenie_maszynowe">Uczenie maszynowe</a>
        <a href="{BASE_URL}/wiki/Sieć_neuronowa">Sieć neuronowa</a>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")
    links = extract_links(soup)

    assert links == [
        f"{BASE_URL}/wiki/Uczenie_maszynowe",
        f"{BASE_URL}/wiki/Sieć_neuronowa",
    ]


def test_extract_links_removes_duplicates():
    html = f"""
    <div id="mw-content-text">
        <a href="{BASE_URL}/wiki/Uczenie_maszynowe">Link 1</a>
        <a href="{BASE_URL}/wiki/Uczenie_maszynowe">Link 2</a>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")
    links = extract_links(soup)

    assert links == [f"{BASE_URL}/wiki/Uczenie_maszynowe"]


def test_extract_links_ignores_other_domains():
    html = f"""
    <div id="mw-content-text">
        <a href="https://example.com/wiki/Test">Inna strona</a>
        <a href="{BASE_URL}/wiki/Sztuczna_inteligencja">Wikipedia</a>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")
    links = extract_links(soup)

    assert links == [f"{BASE_URL}/wiki/Sztuczna_inteligencja"]


def test_extract_links_ignores_namespaces():
    html = f"""
    <div id="mw-content-text">
        <a href="{BASE_URL}/wiki/Kategoria:Informatyka">Kategoria</a>
        <a href="{BASE_URL}/wiki/Plik:Example.jpg">Plik</a>
        <a href="{BASE_URL}/wiki/Algorytm">Algorytm</a>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")
    links = extract_links(soup)

    assert links == [f"{BASE_URL}/wiki/Algorytm"]


def test_extract_links_removes_fragment_and_query():
    html = f"""
    <div id="mw-content-text">
        <a href="{BASE_URL}/wiki/Algorytm#Historia">Historia</a>
        <a href="{BASE_URL}/wiki/Uczenie_maszynowe?test=1">Uczenie maszynowe</a>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")
    links = extract_links(soup)

    assert links == [
        f"{BASE_URL}/wiki/Algorytm",
        f"{BASE_URL}/wiki/Uczenie_maszynowe",
    ]


def test_extract_links_ignores_disambiguation():
    html = f"""
    <div id="mw-content-text">
        <a href="{BASE_URL}/wiki/Sztuczna_inteligencja_(ujednoznacznienie)">Ujednoznacznienie</a>
        <a href="{BASE_URL}/wiki/Sztuczna_inteligencja">Sztuczna inteligencja</a>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")
    links = extract_links(soup)

    assert links == [f"{BASE_URL}/wiki/Sztuczna_inteligencja"]


def test_extract_links_without_content():
    soup = BeautifulSoup("<html><body></body></html>", "html.parser")

    assert extract_links(soup) == []