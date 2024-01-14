import os
import sys

from simple_migrations.config import simple_migrations_config
import psycopg


def initial_setup() -> int:
    config = simple_migrations_config.get()
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

    if not os.path.exists(config.migrations_dir):
        os.mkdir(config.migrations_dir)
    with open(f"{config.migrations_dir}/__init__.py", "w") as f:
        f.write("\n")

    sys.stdout.write(f"Created {config.migrations_dir} directory\n")
    return 0
