import os
import sys

from simple_migrations.config import Config
import psycopg


def initial_setup(

) -> int:
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

    sys.stdout.write("Created simple_migrations table\n")

    if os.path.exists(config.migrations_dir) and os.listdir(config.migrations_dir):
        sys.stderr.write(f"{config.migrations_dir} directory exists and not empty")
        return 1

    os.mkdir(config.migrations_dir)
    sys.stdout.write(f"Created {config.migrations_dir} directory\n")
    return 0
