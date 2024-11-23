import pytest
from patterns import movie_pattern
# Dados de teste


@pytest.mark.parametrize(
    "input_text,expected_matches",
    [
        # Caso válido: filme deve ser capturado
        (
            """#EXTINF:-1 tvg-id="" tvg-name="CARGA EXPLOSIVA 2 (2005)" tvg-logo="http://dns.1888gyn.click:80/images/d8c97292aa032ab8bebd2f3f2a4f3a76.jpg" group-title="FILME | ACÃO E CRIME",CARGA EXPLOSIVA 2 (2005)
http://dns.aipim.info:80/movie/AdautoViseli/g4ue5j5h/320949.mp4
            """,
            [
                {
                    "movie": "CARGA EXPLOSIVA 2 (2005)",
                    "url": "http://dns.aipim.info:80/movie/AdautoViseli/g4ue5j5h/320949.mp4",
                }
            ],
        ),
        # Caso válido: outro filme
        (
            """#EXTINF:-1 tvg-name="Carga Explosiva: O Legado" tvg-logo="http://p6.vc/IIJ" group-title="Filmes | Acao",Carga Explosiva: O Legado
http://cdn22.cc:80/movie/Magalhaesps/101280/57983.mp4

            """,
            [
                {
                    "movie": "Carga Explosiva: O Legado",
                    "url": "http://cdn22.cc:80/movie/Magalhaesps/101280/57983.mp4",
                }
            ],
        ),
        # Caso inválido: canal ao vivo
        (
            """#EXTINF:-1 tvg-id="megapix.br" tvg-name="MEGAPIX FHD H265" tvg-logo="http://dns.1888gyn.click:80/images/f3e7a2148447f01c2b45e5a8f418b783.jpg" group-title="FILMES E SÉRIES",MEGAPIX FHD H265
http://dns.aipim.info:80/AdautoViseli/g4ue5j5h/194195
            """,
            [],  # Nenhum match esperado
        ),
    ],
)
def test_movie_pattern(input_text, expected_matches):
    """
    Testa se a regex captura corretamente filmes e ignora canais ao vivo.
    """
    matches = [
        {"movie": match.group("movie"), "url": match.group("url")}
        for match in movie_pattern.finditer(input_text)
    ]
    assert matches == expected_matches
