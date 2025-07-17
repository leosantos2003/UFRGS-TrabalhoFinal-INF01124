# carrega_dados.py

import pandas as pd

def load_players(file_path: str) -> pd.DataFrame | None:

    # Carrega os dados dos jogadores do arquivo players.csv.

    # Argumentos:
    #     file_path (str): O caminho para o arquivo players.csv.

    # Retornos:
    #     pd.DataFrame | None: Um DataFrame do pandas com os dados dos jogadores
    #                          ou None se o arquivo não for encontrado.

    try:
        # A especificação de 'low_memory=False' pode ajudar a evitar avisos
        # sobre tipos de dados mistos em colunas grandes.
        players_df = pd.read_csv(file_path, low_memory=False)
        print(f"Arquivo '{file_path}' carregado com sucesso.")
        return players_df
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao carregar '{file_path}': {e}")
        return None

def load_ratings(file_path: str) -> pd.DataFrame | None:
    
    # Carrega os dados de avaliação do arquivo de ratings (ex: minirating.csv).

    # Argumentos:
    #     file_path (str): O caminho para o arquivo de ratings.

    # Retornos:
    #     pd.DataFrame | None: Um DataFrame do pandas com os dados de avaliação
    #                          ou None se o arquivo não for encontrado.
    
    try:
        ratings_df = pd.read_csv(file_path)
        print(f"Arquivo '{file_path}' carregado com sucesso.")
        return ratings_df
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao carregar '{file_path}': {e}")
        return None

def load_tags(file_path: str) -> pd.DataFrame | None:
    
    # Carrega os dados de tags do arquivo tags.csv.

    # Argumentos:
    #     file_path (str): O caminho para o arquivo tags.csv.

    # Retornos:
    #     pd.DataFrame | None: Um DataFrame do pandas com os dados das tags
    #                          ou None se o arquivo não for encontrado.
    
    try:
        tags_df = pd.read_csv(file_path)
        print(f"Arquivo '{file_path}' carregado com sucesso.")
        return tags_df
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao carregar '{file_path}': {e}")
        return None

# Exemplo de como usar o módulo
if __name__ == '__main__':
    # Caminhos para os arquivos (ajuste se necessário)
    PLAYERS_FILE = 'players.csv'
    RATINGS_FILE = 'minirating.csv'
    TAGS_FILE = 'tags.csv'

    print("--- Testando o carregador de dados ---")

    # Carregar dados dos jogadores
    players_data = load_players(PLAYERS_FILE)
    if players_data is not None:
        print("Amostra dos dados de jogadores:")
        print(players_data.head())
        print("-" * 30)

    # Carregar dados de avaliações
    ratings_data = load_ratings(RATINGS_FILE)
    if ratings_data is not None:
        print("Amostra dos dados de avaliações:")
        print(ratings_data.head())
        print("-" * 30)

    # Carregar dados das tags
    tags_data = load_tags(TAGS_FILE)
    if tags_data is not None:
        print("Amostra dos dados de tags:")
        print(tags_data.head())
        print("-" * 30)