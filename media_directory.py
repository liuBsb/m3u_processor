import os


class MediaDirectory:
    def __init__(self, output_dir, media_type):
        self.output_dir = output_dir
        self.media_type = media_type

        # Criação dos diretórios com base no tipo de mídia
        self.base_dir = self._get_base_directory()
        self._ensure_directory(self.base_dir)

    def _get_base_directory(self):
        """Retorna o diretório base dependendo do tipo de mídia."""
        if self.media_type == "series":
            return os.path.join(self.output_dir, "Series")
        elif self.media_type == "movie":
            return os.path.join(self.output_dir, "Movies")
        elif self.media_type == "adult":
            return os.path.join(self.output_dir, "Others")
        elif self.media_type == "tv_channel":
            return os.path.join(self.output_dir, "TVChannels")
        else:
            raise ValueError(f"Tipo de mídia '{self.media_type}' não suportado.")

    def _ensure_directory(self, directory):
        """Garante que o diretório exista."""
        os.makedirs(directory, exist_ok=True)

    def process(self, text):
        raise NotImplementedError(
            "A subclasse deve implementar o método 'process' para lidar com o texto."
        )
