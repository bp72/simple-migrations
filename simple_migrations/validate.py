import os
import sys

import psycopg

from simple_migrations.config import Config


def validate_migrations() -> bool:
    config = Config()
    with psycopg.connect(config.connection_string) as conn:
        with conn.cursor() as cur:
            applied_migrations = cur.fetchall("""
                SELECT name FROM simple_migrations
                ORDER BY created_at
            """)

    sys.stdout.write(f"Collected {len(applied_migrations)} applied migrations from the database")

    file_migrations = os.listdir(config.migrations_dir)
    