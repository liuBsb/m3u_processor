import re
import os
from media_directory import MediaDirectory
from patterns import adult_pattern


class AdultProcessor(MediaDirectory):
    def __init__(self, output_dir):
        super().__init__(output_dir, "adult")

    def process(self, text):
        adult_matches = adult_pattern.finditer(text)
        for match in adult_matches:
            # Extrair informações do conteúdo
            adult_name = match.group("adult_name")

            # Limpeza do nome
            adult_name = self.clean_adult_name(adult_name)

            # Substituir os espaços internos por pontos, ignorando espaços no início e no final
            adult_name = re.sub(r"(?<=\S)\s+(?=\S)", ".", adult_name).strip()

            url = match.group("url")

            # Extrair o nome do site e data nos formatos "YY MM DD" ou "YYYY.MM.DD"
            date_match = re.search(
                r"\b(\d{2})\s(\d{2})\s(\d{2})\b|\b(\d{4})\.(\d{2})\.(\d{2})\b",
                adult_name,
            )

            if date_match:
                # Extrair o nome do site antes da data, mantendo todas as palavras antes dela
                site = adult_name[: date_match.start()].strip()
            else:
                site = "UnknownSite"

            # Construir o nome do arquivo no formato especificado
            file_name = f"{adult_name}.strm"

            # Definir o diretório para o site e garantir que ele exista
            site_dir = os.path.join(self.base_dir, site)
            os.makedirs(site_dir, exist_ok=True)
            strm_file = os.path.join(site_dir, file_name)

            # Criar o arquivo apenas se ainda não existir
            if not os.path.exists(strm_file):
                with open(strm_file, "w") as f:
                    f.write(url)
                print(f"Criado: {strm_file}")
            else:
                print(f"Ignorado (já existe): {strm_file}")

    def clean_adult_name(self, adult_name):
        """
        Limpa o nome do conteúdo adulto, removendo palavras específicas e símbolos indesejados.

        :param adult_name: Nome original do conteúdo adulto.
        :return: Nome limpo do conteúdo.
        """
        # Remover "XXX", "Adulto", colchetes e outros símbolos específicos do nome principal
        adult_name = re.sub(
            r"\b(XXX|Adulto|:|/|\[|\])\b|\[.*?\]",
            "",
            adult_name,
            flags=re.IGNORECASE,
        ).strip()

        # Adicionar sufixo ".XXX"
        adult_name = f"{adult_name}.XXX"

        return adult_name
