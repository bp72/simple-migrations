import os
import sys

import psycopg

from simple_migrations.config import Config


FILE_DIR = os.path.dirname(__file__)


def generate_migration() -> int:
    config = Config()
    next_migration_id = _format_migration_id(_get_last_migration_id() + 1)
    conflicting_file_name = next(
        (
            file_name for file_name in os.listdir(config.migrations_dir)
            if file_name.startswith(next_migration_id)
        ),
        None,
    )
    if conflicting_file_name:
        sys.stderr.write(f"There is an unapplied migration with conflicting name: {conflicting_file_name}")
        return 1

    with open(f"{FILE_DIR}/migration_template.py", "r") as template:
        template_code = template.read()

    new_migration_name = f"{config.migrations_dir}/{next_migration_id}_migration.py"
    with open(new_migration_name, "w") as f:
        f.write(template_code)
    return 0


def _get_last_migration_id() -> int:
    config = Config()
    with psycopg.connect(config.connection_string) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id FROM simple_migrations
                ORDER BY id DESC
                LIMIT 1
            """)
            last_migration = cur.fetchone()
    if last_migration is None:
        return 0
    return last_migration["id"]


def _format_migration_id(migration_id: int) -> str:
    formatted_id = str(migration_id)
    return "0" * (6 - len(formatted_id)) + formatted_id
