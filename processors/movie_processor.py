import re
import os
from media_directory import MediaDirectory
from patterns import movie_pattern


class MovieProcessor(MediaDirectory):
    def __init__(self, output_dir):
        super().__init__(output_dir, "movie")

    def process(self, text):
        movie_matches = movie_pattern.finditer(text)
        movie_count = 0
        for match in movie_matches:
            movie = match.group("movie").strip()
            movie = re.sub(r"(:|/|-)", "", movie)
            movie = re.sub(r"(\D)4K", r"\1 4K", movie)
            movie = re.sub(r"\s+", " ", movie)
            url = match.group("url")
            movie_dir = os.path.join(self.base_dir, movie)
            os.makedirs(movie_dir, exist_ok=True)
            strm_file = os.path.join(movie_dir, f"{movie}.strm")

            movie_count += 1
            if os.path.exists(strm_file):
                with open(strm_file, "r") as f:
                    old_url = f.read().strip()  # Lê o link anterior
                print(f"Substituindo link anterior: {old_url}")
            else:
                old_url = None
            with open(strm_file, "w") as f:
                f.write(url)

            if old_url:
                print(f"Link do arquivo '{
                      strm_file}' atualizado para: '{url}'")
            else:
                print(f"Criado arquivo '{strm_file}' com link: {url}")
        print(f"Total de filmes processados: {movie_count}")
