import os
import pytest
from database import Database


@pytest.fixture
def test_db():
    """Configura um banco de dados temporário para testes."""
    test_db_path = os.path.join(os.getcwd(), "test_media.db")
    db = Database(test_db_path)
    db.initialize()
    yield db
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


def test_initialize(test_db):
    """Teste de inicialização do banco de dados."""
    assert os.path.exists(test_db.db_path)


def test_save_and_fetch(test_db):
    """Teste de inserção e recuperação de dados."""
    channel_data = {
        "channel_name": "Channel 1",
        "tvg_id": "12345",
        "tvg_logo": "http://example.com/logo.png",
        "group_title": "News",
        "url": "http://example.com/stream",
    }
    test_db.save(channel_data)
    results = test_db.fetchall("SELECT * FROM tv_channels")
    assert len(results) == 1
    assert results[0][1] == "Channel 1"
