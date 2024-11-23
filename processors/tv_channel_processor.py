import re
from media_directory import MediaDirectory
from patterns import channel_pattern
from database import Database


class TVChannelProcessor(MediaDirectory):
    def __init__(self, output_dir):
        super().__init__(output_dir, "tv_channel")
        self.db = Database()  # Inicializa o banco de dados

    def _process_channels(self, text):
        # Encontra os canais no texto usando a regex
        tv_channel_matches = list(channel_pattern.finditer(text))

        if not tv_channel_matches:
            print("Nenhum canal encontrado para processar.")
            return  # Sai do método se não houver correspondências

        # Processar os canais encontrados
        for match in tv_channel_matches:
            channel_data = {
                "channel_name": match.group("channel_name"),
                "tvg_id": match.group("tvg_id"),
                "tvg_logo": match.group("tvg_logo"),
                "group_title": match.group("group_title"),
                "url": match.group("url"),
            }

            # Salva no banco de dados
            self.db.save(channel_data)
            print(f"Canal salvo: {channel_data['channel_name']}")

    def process(self, file_text):
        """
        Processa o texto do arquivo, extraindo canais de TV.
        """
        try:
            self._process_channels(file_text)
        except Exception as e:
            print(f"Erro ao processar canais: {e}")
        finally:
            self.db.close()  # Fecha a conexão com o banco de dados
