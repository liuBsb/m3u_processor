import os
import sqlite3
from sqlite3 import Connection  # Para tipagem


class Database:
    DEFAULT_DB_PATH = os.path.join(
        os.path.expanduser("~"), ".m3u_processor", "media.db"
    )

    def __init__(self, db_path: str | None = None):
        self.db_path: str = db_path or self.DEFAULT_DB_PATH
        self._ensure_directory_exists()
        self.connection: Connection | None = None  # Anotação explícita de tipo

    def _ensure_directory_exists(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def connect(self):
        """Estabelece a conexão com o banco de dados."""
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def initialize(self):
        """Cria as tabelas necessárias no banco de dados."""
        self.connect()
        if self.connection:  # Garantindo que a conexão não é None
            cursor = self.connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tv_channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_name TEXT NOT NULL,
                    tvg_id TEXT,
                    tvg_logo TEXT,
                    group_title TEXT,
                    url TEXT NOT NULL
                )
            """
            )
            self.connection.commit()

    def save(self, channel_data: dict):
        """Salva os dados do canal no banco de dados."""
        self.connect()
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                INSERT INTO tv_channels (channel_name, tvg_id, tvg_logo, group_title, url)
                VALUES (:channel_name, :tvg_id, :tvg_logo, :group_title, :url)
                """,
                channel_data,
            )
            self.connection.commit()

    def execute(self, query: str, params: dict | list | None = None):
        """Executa uma consulta no banco de dados."""
        self.connect()
        if self.connection:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        raise RuntimeError("A conexão com o banco de dados não foi estabelecida.")

    def fetchall(self, query: str, params: dict | list | None = None):
        """Executa uma consulta e retorna todos os resultados."""
        self.connect()
        if self.connection:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        raise RuntimeError("A conexão com o banco de dados não foi estabelecida.")
