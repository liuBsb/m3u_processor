#!/usr/bin/env python3
import os
import argparse
from database import Database
from processors.processor_factory import ProcessorFactory
def main():
    # Configuração de argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Processador de arquivos M3U")
    parser.add_argument("m3u_file", type=str, help="Arquivo M3U a ser processado")
    parser.add_argument(
        "-s",
        "--output-dir",
        type=str,
        default=os.getcwd(),
        help="Diretório de saída (padrão: diretório atual)",
    )
    parser.add_argument(
        "-t",
        "--media-types",
        type=str,
        nargs="+",
        default=["series", "movie", "adult", "tv_channel"],
        help="Tipos de mídia a serem processados (ex.: series movie)",
    )

    args = parser.parse_args()

    # Inicializa o banco de dados
    db = Database()
    db.initialize()

    try:
        # Carregar o conteúdo do arquivo M3U
        with open(args.m3u_file, "r") as m3u_file:
            m3u_text = m3u_file.read()

        # Verifica se é uma lista com um ou mais tipos
        if len(args.media_types) == 1:
            processor = ProcessorFactory.create_processor(
                m3u_file=args.m3u_file,
                output_dir=args.output_dir,
                media_type=args.media_types[0],
            )
            processor.process(m3u_text)
        else:
            processors = ProcessorFactory.create_processors(
                m3u_file=args.m3u_file,
                output_dir=args.output_dir,
                media_types=args.media_types,
            )
            for processor in processors:
                processor.process(m3u_text)

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        db.close()

    print("Processo concluído.")


if __name__ == "__main__":
    main()
