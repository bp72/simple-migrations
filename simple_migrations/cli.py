import sys
from enum import StrEnum

from simple_migrations.config import configure
from simple_migrations.migrate import generate_migration, migrate
from simple_migrations.initial_setup import initial_setup


class ActionType(StrEnum):
    init = "init"
    generate = "generate"
    migrate = "migrate"


def main(argv: list[str] | None = None) -> int:
    configure()
    argv = argv or sys.argv[1:]
    if not argv:
        # TODO: print help
        return 1
    action = argv[0]
    if action == ActionType.init:
        return initial_setup()
    if action == ActionType.generate:
        return generate_migration()
    if action in ActionType.migrate:
        fake = False
        if "--fake" in argv:
            fake = True
            argv.pop(argv.index("--fake"))
        until = None
        if len(argv) > 1:
            try:
                until = int(argv[1])
            except ValueError:
                sys.stderr.write(f"Invalid version: {argv[1]}, please pass the migration number")
                return 1
        return migrate(until=until, fake=fake)
    else:
        sys.stderr.write("Unknown command\n")
    return 1
