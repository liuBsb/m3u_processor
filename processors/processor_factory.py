from processors import *


class ProcessorFactory:
    @staticmethod
    def create_processors(m3u_file=None, output_dir=None, media_types=None):
        """
        Cria uma lista de processadores com base em uma lista de tipos de mídia.
        """
        if not isinstance(media_types, list):
            media_types = [media_types]  # Garante que seja sempre uma lista

        processors = []
        for mt in media_types:
            processors.append(
                ProcessorFactory.create_processor(m3u_file, output_dir, mt)
            )
        return processors

    @staticmethod
    def create_processor(m3u_file=None, output_dir=None, media_type=None):
        """
        Cria um único processador com base no tipo de mídia.
        """
        if not media_type:
            raise ValueError("O tipo de mídia não pode ser None ou vazio.")

        if media_type == "movie":
            return MovieProcessor(output_dir)
        elif media_type == "series":
            return SeriesProcessor(output_dir)
        elif media_type == "adult":
            return AdultProcessor(output_dir)
        elif media_type == "tv_channel":
            return TVChannelProcessor(output_dir)
        else:
            raise ValueError(f"Tipo de mídia '{media_type}' não é suportado.")
