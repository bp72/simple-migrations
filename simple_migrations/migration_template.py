import psycopg

from simple_migrations.config import Config


FORWARDS_SQL = ""
BACKWARDS_SQL = ""


def forwards() -> None:
    config = Config()
    with psycopg.connect(config.connection_string) as conn:
        with conn.cursor() as cur:
            cur.execute(FORWARDS_SQL)


def backwards() -> None:
    config = Config()
    with psycopg.connect(config.connection_string) as conn:
        with conn.cursor() as cur:
            cur.execute(BACKWARDS_SQL)
