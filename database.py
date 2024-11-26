import os
import sqlite3
import subprocess
from sqlite3 import Connection
from utils.config import Config


class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            config = Config()
            db_path = config.get_database_path(environment="development")
        self.db_path = db_path
        self._ensure_directory_exists()
        self.connection: Connection | None = None

    def _ensure_directory_exists(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def connect(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def initialize(self):
        self.connect()
        if self.connection:
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
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            self.connection.commit()

    def save(self, table: str, data: dict):
        """Insere os dados no banco de dados."""
        placeholders = ", ".join(f":{key}" for key in data.keys())
        columns = ", ".join(data.keys())
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        try:
            self.execute(query, data)
        except sqlite3.IntegrityError:
            print(f"Registro já existe: {data['title']}")

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

    def fetchall(self, query: str, params: dict | list | tuple | None = None):
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

    @staticmethod
    def verify_link(url: str) -> bool:
        """Verifica se o link funciona usando ffmpeg."""
        try:
            result = subprocess.run(
                ["ffmpeg", "-i", url, "-t", "00:00:01", "-f", "null", "-"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Erro ao verificar o link: {url} -> {e}")
            return False
