# Aplicativo de Processamento de Arquivos M3U

Este é um aplicativo modular para processar arquivos `.m3u`, permitindo a organização de conteúdos como canais de TV, filmes, séries e conteúdos adultos.  
O projeto nasceu da necessidade de extrair e organizar conteúdos distribuídos em listas `.m3u` para uso com **Emby/Jellyfin**.

## Funcionalidades

- **Processamento Modular**: Diferentes tipos de conteúdo são gerenciados por processadores dedicados (canais de TV, filmes, séries e adultos).
- **Geração de Arquivos `.strm`**: Cria e atualiza arquivos `.strm` para cada item de VOD, permitindo fácil integração com servidores de mídia.
- **Gerenciamento de Links**: Atualiza links obsoletos armazenados nos diretórios existentes.
- **Banco de Dados SQLite**: Armazena metadados de mídia em um banco de dados SQLite, permitindo recuperação e organização futura.

## Motivação

Este projeto foi desenvolvido para facilitar a criação de arquivos `.strm` com listas `.m3u` que contêm diversos tipos de mídia. Com isso, você pode usufruir da sua lista para criar uma biblioteca de mídia personalizada, diretamente integrada ao **Emby** ou **Jellyfin**.

## Uso

1. **Processadores disponíveis:**

   - Canais de TV
   - Filmes
   - Séries
   - Conteúdo adulto

2. **Saída:**
   - Geração de diretórios organizados.
   - Arquivos `.strm` para cada conteúdo identificado.
   - Metadados salvos em um banco de dados SQLite.

## Versão

**Versão atual**: 1.0.0-beta  
Este é um lançamento beta para testes. As buscas retornam grande parte dos conteúdos, mas ainda é necessário ampliar os padrões da regex para cobrir 100% dos casos.

## Funcionalidades

- Processamento de diferentes tipos de conteúdo: canais de TV, filmes, séries e conteúdo adulto.
- Suporte a armazenamento em banco de dados SQLite para canais de TV.
- Extração de informações usando expressões regulares.
- Criação de arquivos `.strm` organizados por diretórios.

## Requisitos

- Python 3.8 ou superior
- SQLite (opcional, apenas para canais de TV)

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/liuBsb/m3u-processor.git
   cd m3u-processor
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Comando Básico

Execute o aplicativo com os seguintes argumentos:

```bash
python main.py <tipo_de_processador> <arquivo_m3u> <diretorio_saida> [--db_path <caminho_db>]
```

- `<tipo_de_processador>`: Tipo de conteúdo a ser processado (`adult`, `movie`, `series`, `tv_channel`).
- `<arquivo_m3u>`: Caminho para o arquivo M3U de entrada.
- `<diretorio_saida>`: Diretório onde os arquivos `.strm` serão criados.
- `--db_path`: Caminho opcional para o banco de dados SQLite. Padrão: `database.db`.

### Exemplos

1. Processar canais de TV e salvar no banco de dados:

   ```bash
   python main.py tv_channel input.m3u output_dir --db_path database.db
   ```

2. Processar filmes e gerar arquivos `.strm`:

   ```bash
   python main.py movie input.m3u output_dir
   ```

3. Processar conteúdo adulto:

   ```bash
   python main.py adult input.m3u output_dir
   ```

### Consultar o Banco de Dados

Se você processou canais de TV com `--db_path`, pode consultar os dados salvos no SQLite:

1. Abra o banco de dados:

   ```bash
   sqlite3 database.db
   ```

2. Execute uma consulta:

   ```sql
   SELECT * FROM tv_channels;
   ```

## Estrutura do Banco de Dados

Para canais de TV, os dados são armazenados na tabela `tv_channels` com os seguintes campos:

| Campo          | Tipo    | Descrição                            |
| -------------- | ------- | ------------------------------------ |
| `id`           | INTEGER | ID único do canal (chave primária).  |
| `channel_name` | TEXT    | Nome do canal.                       |
| `tvg_id`       | TEXT    | Identificador do canal (opcional).   |
| `tvg_logo`     | TEXT    | URL do logotipo do canal (opcional). |
| `group_title`  | TEXT    | Nome do grupo de canais.             |
| `url`          | TEXT    | URL do canal.                        |

## Desenvolvimento

### Adicionar um Novo Processador

1. Crie um novo arquivo em `processors/` (exemplo: `my_processor.py`).
2. Estenda a classe `MediaProcessor` e implemente o método `process`.
3. Registre o processador em `processor_factory.py`.

### Testes

Certifique-se de testar cada funcionalidade após modificações:

```bash
python -m unittest discover
```

## Contribuições

Contribuições são bem-vindas! Por favor, siga estas etapas:

1. Faça um fork do repositório.
2. Crie uma branch para sua funcionalidade ou correção:

   ```bash
   git checkout -b minha-nova-funcionalidade
   ```

3. Envie um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
