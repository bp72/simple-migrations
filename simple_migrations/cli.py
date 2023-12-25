import sys
from enum import StrEnum

from simple_migrations.migrate import generate_migration, migrate
from simple_migrations.setup import initial_setup


class ActionType(StrEnum):
    init = "init"
    generate = "generate"
    migrate = "migrate"


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        # TODO: print help
        return 1
    action = argv[0]
    if action == ActionType.init:
        return initial_setup()
    if action == ActionType.generate:
        return generate_migration()
    if action == ActionType.migrate:
        return migrate()
    return 1
