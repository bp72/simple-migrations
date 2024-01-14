import os.path
from configparser import ConfigParser
from contextvars import ContextVar
from dataclasses import dataclass


@dataclass
class Config:
    database_host: str
    database_port: str
    database_name: str
    database_user: str
    database_password: str
    migrations_dir: str

    @property
    def connection_string(self) -> str:
        return (
            f"postgresql://"
            f"{self.database_user}:{self.database_password}@"
            f"{self.database_host}:{self.database_port}/"
            f"{self.database_name}"
        )


simple_migrations_config = ContextVar("simple_migrations_config")


def configure() -> None:
    config_path = "simple_migrations.ini"
    if not os.path.exists(config_path):
        raise ValueError("Simple migrations: config file doesn't exist")

    config = ConfigParser()
    config.read(config_path)

    simple_migrations_config.set(
        Config(
            database_host=config["simple-migrations"]["database_host"],
            database_port=config["simple-migrations"]["database_port"],
            database_name=config["simple-migrations"]["database_name"],
            database_user=config["simple-migrations"]["database_user"],
            database_password=config["simple-migrations"]["database_password"],
            migrations_dir=config["simple-migrations"]["migrations_dir"],
        ),
    )
