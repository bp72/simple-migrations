from simple_migrations.config import Config
import psycopg


def initial_setup(

) -> None:
    config = Config()
    with psycopg.connect(config.connection_string) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS simple_migrations (
                    id bigint PRIMARY KEY,
                    name text,
                    created_at timestamptz
                )
            """)
