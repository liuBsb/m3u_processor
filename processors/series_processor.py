import os
from media_directory import MediaDirectory
from patterns import series_pattern


class SeriesProcessor(MediaDirectory):
    def __init__(self, output_dir):
        super().__init__(output_dir, "series")

    def process(self, text):
        series_matches = series_pattern.finditer(text)
        for match in series_matches:
            serie = match.group("serie").replace(":", "").replace("/", "-")
            season = match.group("season")
            episode = match.group("episode")
            url = match.group("url")
            season_dir = os.path.join(self.base_dir, serie, f"Season {season}")
            os.makedirs(season_dir, exist_ok=True)
            strm_file = os.path.join(season_dir, f"{serie} S{season}E{episode}.strm")
            if not os.path.exists(strm_file):
                with open(strm_file, "w") as f:
                    f.write(url)
                print(f"Criado: {strm_file}")
            else:
                print(f"Ignorado (já existe): {strm_file}")
