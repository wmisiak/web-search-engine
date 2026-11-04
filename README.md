# Web Search Engine

System składający się z crawlera Wikipedii, indeksera TF-IDF oraz wyszukiwarki wykorzystującej podobieństwo cosinusowe. Dane przechowywane są w PostgreSQL.

## Instalacja

Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

Utwórz plik `.env`:

```env
DB_HOST=localhost
DB_PORT=5434
DB_NAME=web_search_db
DB_USER=a_user
DB_PASSWORD=pass123
```

## Baza danych

Uruchom PostgreSQL w Dockerze:

```bash
docker compose up -d
```

Sprawdź, czy kontener działa:

```bash
docker ps
```

## Indeksowanie

Uruchom crawler i zbuduj indeks:

```bash
python indexer.py
```

Program pobierze strony z Wikipedii, zapisze nowe strony w PostgreSQL i zbuduje dla nich indeks TF-IDF.

## Wyszukiwanie

Uruchom:

```bash
python search.py
```

Następnie wpisz zapytanie, np.:

```text
Wpisz zapytanie: uczenie maszynowe
```

Program zwróci posortowaną listę najbardziej podobnych stron wraz z adresami URL.

## Testy

Uruchom:

```bash
python -m pytest -v
```

## Zatrzymanie bazy

```bash
docker compose down
```