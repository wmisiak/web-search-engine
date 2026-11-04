# Web Search Engine

System składający się z crawlera Wikipedii, indeksera TF-IDF oraz wyszukiwarki wykorzystującej podobieństwo cosinusowe. Dane przechowywane są w PostgreSQL.

## Uruchomienie

Zainstaluj wymagane biblioteki:

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

Uruchom bazę danych:

```bash
docker compose up -d
```

Uruchom crawler i indekser:

```bash
python indexer.py
```

Podaj adres startowego artykułu z polskiej Wikipedii, np.:

```text
Podaj adres startowy Wikipedii: https://pl.wikipedia.org/wiki/Sztuczna_inteligencja
```

## Wyszukiwanie

Uruchom wyszukiwarkę:

```bash
python search.py
```

Wpisz zapytanie, np.:

```text
Wpisz zapytanie: uczenie maszynowe
```

## Testy

```bash
python -m pytest -v
```

## Zatrzymanie

```bash
docker compose down
```