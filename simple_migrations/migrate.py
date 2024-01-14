import os
import sys
from datetime import datetime, timezone
from importlib import import_module

import psycopg

from simple_migrations.config import simple_migrations_config

FILE_DIR = os.path.dirname(__file__)


def generate_migration() -> int:
    config = simple_migrations_config.get()
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


def migrate(until: int | None, fake: bool) -> int:
    config = simple_migrations_config.get()
    migrations_map = {}
    for file_name in os.listdir(config.migrations_dir):
        migration_id = _get_migration_id_from_name(file_name)
        if migration_id is None:
            continue
        if migration_id in migrations_map:
            sys.stderr.write(f"Duplicated migrations were found, migrations can't be applied: {migrations_map[migration_id]}, {file_name}")
            return 1

        migrations_map[migration_id] = file_name

    sys.stdout.write(f"Collected {len(migrations_map)} migrations\n")
    last_migration_id = _get_last_migration_id()
    if last_migration_id is None:
        sys.stdout.write(f"No applied migrations were found\n")
    else:
        sys.stdout.write(f"Last applied migration is #{last_migration_id}\n")

    if until is not None and until < last_migration_id:
        command = "backwards"
        log_action = "Rolling back"
        migrations_to_apply = (
            (m_id, m) for m_id, m in migrations_map.items()
            if m_id <= last_migration_id and m_id > until
        )
        migrations_to_apply = sorted(migrations_to_apply, key=lambda x: -x[0])
    else:
        command = "forwards"
        log_action = "Applying"
        migrations_to_apply = (
            (m_id, m) for m_id, m in migrations_map.items()
            if m_id > last_migration_id and (until is None or m_id <= until)
        )
        migrations_to_apply = sorted(migrations_to_apply, key=lambda x: x[0])
    if not migrations_to_apply:
        sys.stdout.write("Nothing to migrate\n")
        return 0

    log_action = f"Fake {log_action.lower()}" if fake else log_action
    for m_id, migration in migrations_to_apply:
        sys.stdout.write(f"{log_action} {migration}... ")
        if not fake:
            migration_obj = import_module(f"{config.migrations_dir}.{migration[:-3]}")
            method = getattr(migration_obj, command)
            method()
        if command == "forwards":
            _insert_migration(m_id=m_id, name=migration)
        else:
            _delete_migration(m_id=m_id)
        sys.stdout.write("OK\n")
    return 0


def _get_last_migration_id() -> int:
    config = simple_migrations_config.get()
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
    return last_migration[0]


def _format_migration_id(migration_id: int) -> str:
    formatted_id = str(migration_id)
    return "0" * (6 - len(formatted_id)) + formatted_id


def _get_migration_id_from_name(name: str) -> int | None:
    try:
        return int(name[:6])
    except ValueError:
        return None


def _insert_migration(m_id: int, name: str) -> None:
    created_at = datetime.now(timezone.utc)
    config = simple_migrations_config.get()
    with psycopg.connect(config.connection_string) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO simple_migrations (id, name, created_at)
                VALUES (%s, %s, %s)
            """, (m_id, name, created_at))


def _delete_migration(m_id: int) -> None:
    config = simple_migrations_config.get()
    with psycopg.connect(config.connection_string) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM simple_migrations WHERE id = %s
            """, (m_id, ))
