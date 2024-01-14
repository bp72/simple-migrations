import psycopg

from simple_migrations.config import simple_migrations_config

FORWARDS_SQL = ""
BACKWARDS_SQL = ""


def forwards() -> None:
    config = simple_migrations_config.get()
    with psycopg.connect(config.connection_string) as conn:
        with conn.cursor() as cur:
            cur.execute(FORWARDS_SQL)


def backwards() -> None:
    config = simple_migrations_config.get()
    with psycopg.connect(config.connection_string) as conn:
        with conn.cursor() as cur:
            cur.execute(BACKWARDS_SQL)
