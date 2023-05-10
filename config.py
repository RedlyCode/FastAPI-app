from dataclasses import dataclass

from sqlalchemy import URL


@dataclass
class DatabaseConfig:
    host: str  # Database server host. Local example: 127.0.0.1 or localhost
    user: str  # Database user
    password: str  # Database user password
    database: str  # Database name
    port: int = 5432  # Database port. Default value: 5432

    def construct_sqlalchemy_url(self) -> URL:
        return URL.create(
            drivername='postgresql+asyncpg',  # Using the asyncpg driver
            username=self.user,
            password=self.password,
            database=self.database,
            host=self.host,
            port=self.port
        )
