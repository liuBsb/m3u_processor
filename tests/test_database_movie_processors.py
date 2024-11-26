import os

import pytest
from database import Database
from processors.movie_processor import MovieProcessor
from utils.config import Config

m3u_text = """
    #EXTINF:-1 tvg-id="" tvg-name="Terrifier: O Início (2013)" tvg-logo="http://dns.1888gyn.click:80/images/544cec6e59af6cde779382c0d870c79a.jpg" group-title="FILME | Terror",Terrifier: O Início (2013)
    http://dns.aipim.info:80/movie/AdautoViseli/g4ue5j5h/336099.mp4
    #EXTINF:-1 tvg-id="" tvg-name="Mazzaropi - Chico Fumaça (1956)" tvg-logo="http://dns.1888gyn.click:80/images/4abc3dffd78581933d108e012ddf4e3c.jpg" group-title="FILME | CLASSÍCOS",Mazzaropi - Chico Fumaça (1956)
    http://dns.aipim.info:80/movie/AdautoViseli/g4ue5j5h/138236.mp4
    #EXTINF:-1 tvg-id="" tvg-name="Chofer de Praça (1959)" tvg-logo="https://image.tmdb.org/t/p/w600_and_h900_bestv2/7yyVIQO8DTpp5XgfDfueE1OtMV2.jpg" group-title="FILME | CLASSÍCOS",Chofer de Praça (1959)
    http://dns.aipim.info:80/movie/AdautoViseli/g4ue5j5h/138237.mp4
    #EXTINF:-1 tvg-id="" tvg-name="chofer de praça (1959)" tvg-logo="https://image.tmdb.org/t/p/w600_and_h900_bestv2/7yyVIQO8DTpp5XgfDfueE1OtMV2.jpg" group-title="FILME | CLASSÍCOS",Chofer de Praça (1959)
    http://dns.aipim.info:80/movie/AdautoViseli/g4ue5j5h/138237.mp4
"""


@pytest.fixture(scope="session")
def test_db():
    """Configura um banco de dados temporário para testes e o mantém até o final da sessão."""
    config = Config()
    test_db_path = config.get_database_path("test")
    if os.path.exists(test_db_path):  # Limpa resíduos de testes anteriores
        os.remove(test_db_path)
    db = Database(test_db_path)
    db.initialize()
    yield db


@pytest.fixture
def movie_processor(test_db):
    """Cria uma instância do MovieProcessor usando o banco de dados de teste."""
    return MovieProcessor(test_db.db_path)


def test_initialize(test_db):
    """Teste de inicialização do banco de dados."""
    assert os.path.exists(test_db.db_path)


def test_process_valid_movies(mocker, movie_processor, test_db):
    """Teste de processamento de filmes válidos."""
    # Mockar o método is_url_valid
    mocker.patch(
        "processors.movie_processor.MovieProcessor.is_url_valid", return_value=True
    )

    movie_processor.process(m3u_text)
    results = test_db.fetchall("SELECT * FROM movies")
    assert len(results) == 3
    assert results[0][1] == "Terrifier: O Início (2013)"
    assert (
        results[0][2]
        == "http://dns.aipim.info:80/movie/AdautoViseli/g4ue5j5h/336099.mp4"
    )


def test_process_duplicate_movies(mocker, movie_processor, test_db):
    """Teste de detecção de filmes duplicados."""
    # Mockar o método is_url_valid
    mocker.patch(
        "processors.movie_processor.MovieProcessor.is_url_valid", return_value=True
    )
    movie_processor.process(m3u_text)
    results = test_db.fetchall("SELECT * FROM movies")
    # Apenas um registro deve ser salvo
    assert len(results) == 2


def test_process_multiple_movies(mocker, movie_processor, test_db):
    """Teste de processamento de múltiplos filmes."""
    mocker.patch("processors.movie_processor.MovieProcessor.is_url_valid")
    m3u_text = """
    """
    movie_processor.process(m3u_text)
    results = test_db.fetchall("SELECT * FROM movies")
    assert len(results) == 2
    assert results[0][1] == "Mazzaropi  Chico Fumaça (1956)"
    assert results[1][1] == "Chofer de Praça (1959)"


def test_process_invalid_movies(mocker, movie_processor, test_db):
    """Teste de processamento de filmes inválidos."""
    # Mockar o método is_url_valid
    mocker.patch(
        "processors.movie_processor.MovieProcessor.is_url_valid", return_value=True
    )
    sample_text = """
    #EXTINF:-1,Filme Inválido
    http://example.com/invalid_stream.mp4
    """
    movie_processor.process(sample_text)
    results = test_db.fetchall("SELECT * FROM movies")
    # Nenhum filme inválido deve ser salvo
    assert len(results) == 0


def test_database_insert_movies(test_db):
    """Teste inserir dados na tabela movies"""

    movie_data = {
        "title": "Mazzaropi  Chico Fumaça (1956)",
        "url": "http://example.com/video.mp4",
    }

    # Insere os dados no banco de dados
    test_db.save("movies", movie_data)

    # Consulta os registros inseridos
    results = test_db.fetchall(
        "SELECT * FROM movies WHERE title = ?", (movie_data["title"],)
    )

    # Verifica se o filme foi inserido corretamente
    assert len(results) == 1
    assert results[0][1] == "Mazzaropi  Chico Fumaça (1956)"
    assert results[0][2] == "http://example.com/video.mp4"


def test_clean_movie_title(movie_processor):
    """Teste de limpeza e formatação de títulos."""
    raw_title = "Filme TESTE: versão /4K"
    cleaned_title = movie_processor.clean_movie_title(raw_title)
    assert cleaned_title == "Filme Teste: Versão 4K"
