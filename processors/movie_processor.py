import re
import subprocess

from database import Database
from patterns import movie_pattern


class MovieProcessor:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.db.initialize()  # Garante que a tabela de filmes exista
        self.movie_count = 0

    def is_url_valid(self, url):
        """Verifica se a URL é válida usando ffprobe."""
        try:
            subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format",
                    "-of",
                    "json",
                    url,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def is_movie_duplicate(self, title, url):
        """Verifica se o filme já foi salvo no banco de dados."""
        query = "SELECT id FROM movies WHERE title = ? OR url = ?"
        results = self.db.fetchall(query, (title, url))
        return len(results) > 0

    def clean_movie_title(self, title):
        """Limpa e formata o título do filme."""
        title = re.sub(r"(/)", "", title)
        title = re.sub(r"\s+", " ", title)
        title = title.title()
        return title.strip()

    def process(self, text):
        """Processa o texto bruto para salvar filmes no banco de dados."""

        movie_matches = movie_pattern.finditer(text)

        for match in movie_matches:
            movie = match.group("movie")
            url = match.group("url")

            # Limpeza e formatação do título do filme
            movie = self.clean_movie_title(movie)

            # Validações
            if not self.is_url_valid(url):
                print(f"Link inválido: {url}")
                continue

            if self.is_movie_duplicate(movie, url):
                print(f"Filme duplicado ignorado: {movie}")
                continue

            # Salvar no banco de dados
            try:
                self.db.save(
                    "movies",
                    {
                        "title": movie,
                        "url": url,
                    },
                )
                self.movie_count += 1
                print(f"Filme salvo: {movie}")
            except Exception as e:
                print(f"Erro ao salvar filme: {movie} -> {e}")

        print(f"Total de filmes processados: {self.movie_count}")
