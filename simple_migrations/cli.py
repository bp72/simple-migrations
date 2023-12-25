import sys
from enum import StrEnum

from simple_migrations.setup import initial_setup


class ActionType(StrEnum):
    init = "init"


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        # TODO: print help
        return 1
    action = argv[0]
    if action == ActionType.init:
        initial_setup()
        return 0
    return 1
