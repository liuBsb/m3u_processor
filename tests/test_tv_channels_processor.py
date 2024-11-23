# tests/test_main.py
import pytest
from unittest.mock import patch, mock_open
from main import main
import os


@pytest.fixture
def m3u_file_mock():
    return '#EXTINF:-1 tvg-id="channel.br" tvg-name="Test Channel" tvg-logo="logo.png" group-title="group",Test Channel\nhttp://example.com/stream\n'


def test_process_tv_channel(m3u_file_mock):
    # Simulando a leitura do arquivo M3U
    with patch("builtins.open", mock_open(read_data=m3u_file_mock)):
        with patch(
            "sys.argv", ["main.py", "test.m3u", "-t", "tv_channel", "-s", "tests"]
        ):
            main()  # Chama a função main do script principal
        # Verifique se o arquivo M3U foi processado corretamente
        # Aqui você pode adicionar mais verificações específicas, como chamadas ao banco de dados
