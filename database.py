import json
import os

import psycopg
from dotenv import load_dotenv


load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


def page_exists(url: str) -> bool:
    with psycopg.connect(**DB_CONFIG) as conn:
        result = conn.execute(
            "SELECT 1 FROM pages WHERE url = %s",
            (url,),
        ).fetchone()

    return result is not None


def insert_page(url: str, title: str, content: str) -> None:
    with psycopg.connect(**DB_CONFIG) as conn:
        conn.execute(
            """
            INSERT INTO pages (url, title, content)
            VALUES (%s, %s, %s)
            ON CONFLICT (url) DO NOTHING
            """,
            (url, title, content),
        )


def get_pages() -> list[dict]:
    with psycopg.connect(**DB_CONFIG) as conn:
        rows = conn.execute(
            "SELECT id, url, title, content, index_structure FROM pages"
        ).fetchall()

    return [
        {
            "id": row[0],
            "url": row[1],
            "title": row[2],
            "content": row[3],
            "index_structure": row[4],
        }
        for row in rows
    ]


def update_index_structure(page_id: int, index_structure: dict[str, float]) -> None:
    with psycopg.connect(**DB_CONFIG) as conn:
        conn.execute(
            "UPDATE pages SET index_structure = %s WHERE id = %s",
            (json.dumps(index_structure), page_id),
        )