

class Config:

    def __init__(
            self,
            database_host: str = "localhost",
            database_port: str = "5432",
            database_name: str = "simple",
            database_user: str = "simple",
            database_password: str = "simple",
    ) -> None:
        self.database_host = database_host
        self.database_port = database_port
        self.database_name = database_name
        self.database_user = database_user
        self.database_password = database_password

    @property
    def connection_string(self) -> str:
        return (
            f"postgresql://"
            f"{self.database_user}:{self.database_password}@"
            f"{self.database_host}:{self.database_port}/"
            f"{self.database_name}"
        )
