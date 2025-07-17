# estruturas.py

import pandas as pd
from collections import defaultdict

# --- Estrutura 1: Tabela Hash para busca por ID ---

def create_player_id_hash(players_df: pd.DataFrame) -> dict:
    
    # Cria uma tabela hash (dicionário) mapeando sofifa_id para os dados do jogador.

    # Argumentos:
    #     players_df (pd.DataFrame): DataFrame com os dados dos jogadores.

    # Retornos:
    #     dict: Dicionário no formato {sofifa_id: player_data_dict}.
    
    # Converte o DataFrame para um dicionário orientado por registros
    # e depois cria um dicionário com sofifa_id como chave.
    # Isso é muito mais rápido do que iterar sobre as linhas.
    print("Criando tabela hash de jogadores por ID...")
    player_hash = players_df.set_index('sofifa_id').to_dict('index')
    print("Tabela hash de jogadores criada com sucesso.")
    return player_hash

# --- Estrutura 2: Árvore Trie para busca por prefixo de nome ---

class TrieNode:
    # Nó da árvore Trie.
    def __init__(self):
        self.children = {}
        self.player_ids = set() # Usar set para evitar IDs duplicados

class Trie:
    # Estrutura de dados Trie para busca por prefixo.
    def __init__(self):
        self.root = TrieNode()

    def insert(self, name: str, player_id: int):
        # Insere um nome e o ID do jogador associado na Trie.
        node = self.root
        for char in name.lower(): # Armazenar em minúsculas para busca case-insensitive
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.player_ids.add(player_id)

    def search_prefix(self, prefix: str) -> list:
        # Busca por todos os IDs de jogadores cujos nomes começam com o prefixo.
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        return list(node.player_ids)

def create_player_name_trie(players_df: pd.DataFrame) -> Trie:
    
    # Cria e popula uma árvore Trie com os nomes curtos e longos dos jogadores.

    # Argumentos:
    #     players_df (pd.DataFrame): DataFrame com os dados dos jogadores.

    # Retornos:
    #     Trie: A árvore Trie preenchida.
    
    print("Criando árvore Trie para nomes de jogadores...")
    trie = Trie()
    for index, player in players_df.iterrows():
        sofifa_id = player['sofifa_id']
        # Inserir nome longo e curto na Trie
        trie.insert(player['long_name'], sofifa_id)
        trie.insert(player['short_name'], sofifa_id)
    print("Árvore Trie criada com sucesso.")
    return trie

# --- Estrutura 3: Índice Invertido para avaliações de usuários ---

def create_user_ratings_inverted_index(ratings_df: pd.DataFrame) -> dict:
    
    # Cria um índice invertido de user_id para uma lista de (rating, sofifa_id).

    # Argumentos:
    #     ratings_df (pd.DataFrame): DataFrame com as avaliações.

    # Retornos:
    #     dict: Dicionário no formato {user_id: [(rating, sofifa_id), ...]}.
    #           As listas são ordenadas por rating em ordem decrescente.
    
    print("Criando índice invertido de avaliações por usuário...")
    user_ratings = defaultdict(list)
    # Agrupa por usuário e itera sobre os grupos para construir a lista
    for user_id, group in ratings_df.groupby('user_id'):
        # Cria tuplas (rating, sofifa_id)
        ratings_list = list(zip(group['rating'], group['sofifa_id']))
        # Ordena a lista de avaliações em ordem decrescente
        ratings_list.sort(key=lambda x: x[0], reverse=True)
        user_ratings[user_id] = ratings_list
    print("Índice invertido de avaliações criado com sucesso.")
    return dict(user_ratings)

# --- Estrutura 4: Dicionário de Posições com médias de avaliação ---

def create_position_ratings(players_df: pd.DataFrame, ratings_df: pd.DataFrame) -> dict:
    
    # Cria um dicionário de posições com jogadores ordenados pela média de avaliação.

    # Argumentos:
    #     players_df (pd.DataFrame): DataFrame dos jogadores.
    #     ratings_df (pd.DataFrame): DataFrame das avaliações.

    # Retornos:
    #     dict: Dicionário {posicao: [(media_rating, sofifa_id), ...]}.
    
    print("Calculando médias de avaliação e criando estrutura por posições...")
    # Calcula a média de rating para cada jogador
    average_ratings = ratings_df.groupby('sofifa_id')['rating'].mean().reset_index()
    average_ratings.rename(columns={'rating': 'average_rating'}, inplace=True)

    # Junta a média de ratings com os dados dos jogadores
    players_with_avg_rating = pd.merge(players_df, average_ratings, on='sofifa_id')

    position_players = defaultdict(list)
    for index, player in players_with_avg_rating.iterrows():
        # As posições podem ser uma string separada por vírgulas (ex: "ST, CF")
        positions = [p.strip() for p in player['player_positions'].split(',')]
        for pos in positions:
            position_players[pos].append((player['average_rating'], player['sofifa_id']))

    # Ordena os jogadores dentro de cada posição pela média de rating
    for pos in position_players:
        position_players[pos].sort(key=lambda x: x[0], reverse=True)

    print("Estrutura por posições criada com sucesso.")
    return dict(position_players)

# --- Estrutura 5: Índice Invertido para Tags ---

def create_tags_inverted_index(tags_df: pd.DataFrame) -> dict:
    
    # Cria um índice invertido de tags para um conjunto de sofifa_ids.

    # Argumentos:
    #     tags_df (pd.DataFrame): DataFrame com as tags.

    # Retornos:
    #     dict: Dicionário no formato {tag: {sofifa_id_1, sofifa_id_2, ...}}.
    
    print("Criando índice invertido de tags...")
    tag_index = defaultdict(set)
    # Garante que a coluna 'tag' seja do tipo string e remove valores nulos
    tags_df.dropna(subset=['tag'], inplace=True)
    tags_df['tag'] = tags_df['tag'].astype(str)

    for index, row in tags_df.iterrows():
        # Normaliza a tag para minúsculas para consistência
        tag = row['tag'].lower()
        tag_index[tag].add(row['sofifa_id'])
    print("Índice invertido de tags criado com sucesso.")
    return dict(tag_index)

# --- Bloco Principal para Testes ---

if __name__ == '__main__':
    # Este bloco serve para demonstrar o uso do módulo.
    # Requer o módulo 'carrega_dados' e os arquivos de dados.
    import carrega_dados

    # Carrega os dados
    players, ratings, tags = (
        carrega_dados.load_players('players.csv'),
        carrega_dados.load_ratings('minirating.csv'),
        carrega_dados.load_tags('tags.csv')
    )

    if players is not None and ratings is not None and tags is not None:
        print("\n--- Testando a criação das estruturas ---")

        # Teste da Tabela Hash de Jogadores
        player_hash = create_player_id_hash(players)
        print(f"Exemplo de jogador no hash (ID 158023): {player_hash.get(158023, 'Não encontrado')}")
        print("-" * 30)

        # Teste da Árvore Trie
        name_trie = create_player_name_trie(players)
        prefix_results = name_trie.search_prefix('messi')
        print(f"IDs encontrados para o prefixo 'messi': {prefix_results[:5]}...") # Mostra os 5 primeiros
        print("-" * 30)

        # Teste do Índice Invertido de Avaliações
        user_ratings_index = create_user_ratings_inverted_index(ratings)
        # Exemplo para um usuário (pega o primeiro que aparecer)
        sample_user_id = next(iter(user_ratings_index))
        print(f"Avaliações para o usuário {sample_user_id}: {user_ratings_index[sample_user_id][:5]}")
        print("-" * 30)

        # Teste da Estrutura de Posições
        position_ratings_index = create_position_ratings(players, ratings)
        print(f"Melhores jogadores (média, id) para a posição 'ST': {position_ratings_index.get('ST', [])[:5]}")
        print("-" * 30)

        # Teste do Índice Invertido de Tags
        tags_index = create_tags_inverted_index(tags)
        sample_tag = 'dribbler'
        print(f"IDs de jogadores com a tag '{sample_tag}': {list(tags_index.get(sample_tag, set()))[:5]}...")
        print("-" * 30)