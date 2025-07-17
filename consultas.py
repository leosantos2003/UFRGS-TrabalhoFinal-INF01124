# consultas.py

from estruturas import Trie

def search_players_by_prefix(name_trie: Trie, player_hash: dict, prefix: str) -> list[dict]:
    
    # 1. Busca até 20 jogadores cujo nome (curto ou longo) começa com um determinado prefixo.

    # Argumentos:
    #     name_trie (Trie): A árvore Trie contendo os nomes dos jogadores.
    #     player_hash (dict): A tabela hash com os dados completos dos jogadores.
    #     prefix (str): O prefixo do nome a ser buscado.

    # Retornos:
    #     list[dict]: Uma lista de dicionários, onde cada dicionário representa um jogador.
    #                 Retorna uma lista vazia se nenhum jogador for encontrado.
    
    if not prefix:
        return []

    # Busca na Trie para obter os IDs dos jogadores
    player_ids = name_trie.search_prefix(prefix)

    # Limita a 20 resultados e busca os detalhes na hash
    results = []
    for player_id in player_ids[:20]:
        player_data = player_hash.get(player_id)
        if player_data:
            # Adiciona o ID ao dicionário de dados do jogador para exibição
            player_info = {'sofifa_id': player_id, **player_data}
            results.append(player_info)

    return results

def search_player_by_id(player_hash: dict, sofifa_id: int) -> dict | None:
    
    # 2. Busca um jogador específico pelo seu sofifa_id.

    # Argumentos:
    #     player_hash (dict): A tabela hash com os dados dos jogadores.
    #     sofifa_id (int): O ID do jogador a ser buscado.

    # Retornos:
    #     dict | None: Um dicionário com os dados do jogador ou None se não for encontrado.
    
    player_data = player_hash.get(sofifa_id)
    if player_data:
        return {'sofifa_id': sofifa_id, **player_data}
    return None

def search_top_rated_players_by_user(user_ratings_index: dict, player_hash: dict, user_id: int) -> list[dict]:
    
    # 3. Retorna os 20 jogadores mais bem avaliados por um usuário específico.

    # Argumentos:
    #     user_ratings_index (dict): O índice invertido de avaliações por usuário.
    #     player_hash (dict): A tabela hash com os dados dos jogadores.
    #     user_id (int): O ID do usuário.

    # Retornos:
    #     list[dict]: Uma lista de dicionários com os dados dos jogadores e sua avaliação.
    
    # Busca a lista de (rating, sofifa_id) para o usuário
    user_ratings = user_ratings_index.get(user_id, [])

    # Pega os top 20 e busca os detalhes dos jogadores
    results = []
    for rating, player_id in user_ratings[:20]:
        player_data = player_hash.get(player_id)
        if player_data:
            player_info = {
                'sofifa_id': player_id,
                'long_name': player_data.get('long_name'),
                'player_positions': player_data.get('player_positions'),
                'rating': rating  # Adiciona a avaliação do usuário ao resultado
            }
            results.append(player_info)

    return results

def search_top_players_by_position(position_ratings_index: dict, player_hash: dict, n: int, position: str) -> list[dict]:
    
    # 4. Retorna os 'n' melhores jogadores de uma determinada posição pela média de avaliação.

    # Argumentos:
    #     position_ratings_index (dict): O dicionário de posições com jogadores ordenados.
    #     player_hash (dict): A tabela hash com os dados dos jogadores.
    #     n (int): O número de jogadores a serem retornados.
    #     position (str): A posição a ser buscada.

    # Retornos:
    #     list[dict]: Uma lista com os 'n' melhores jogadores da posição.
    
    # Busca a lista de (avg_rating, sofifa_id) para a posição
    position_players = position_ratings_index.get(position.upper(), [])

    # Pega os top 'n' e busca os detalhes
    results = []
    for avg_rating, player_id in position_players[:n]:
        player_data = player_hash.get(player_id)
        if player_data:
            player_info = {
                'sofifa_id': player_id,
                'long_name': player_data.get('long_name'),
                'player_positions': player_data.get('player_positions'),
                'average_rating': round(avg_rating, 2) # Arredonda para 2 casas decimais
            }
            results.append(player_info)

    return results

def search_players_by_tags(tags_index: dict, player_hash: dict, tags: list[str]) -> list[dict]:
    
    # 5. Busca até 20 jogadores que possuam TODAS as tags fornecidas.

    # Argumentos:
    #     tags_index (dict): O índice invertido de tags.
    #     player_hash (dict): A tabela hash com os dados dos jogadores.
    #     tags (list[str]): Uma lista de tags a serem buscadas.

    # Retornos:
    #     list[dict]: Uma lista de jogadores que correspondem a todas as tags.
    
    if not tags:
        return []

    # Converte as tags de busca para minúsculas
    search_tags = [tag.lower() for tag in tags]

    # Encontra o conjunto de IDs para a primeira tag
    # Se a tag não existir, o resultado da interseção será vazio
    initial_ids = tags_index.get(search_tags[0], set()).copy()

    # Faz a interseção com os conjuntos de IDs das outras tags
    for tag in search_tags[1:]:
        initial_ids.intersection_update(tags_index.get(tag, set()))
        # Se a interseção ficar vazia, podemos parar
        if not initial_ids:
            break

    # Busca os detalhes dos jogadores encontrados (até 20)
    results = []
    for player_id in list(initial_ids)[:20]:
        player_data = player_hash.get(player_id)
        if player_data:
            player_info = {'sofifa_id': player_id, **player_data}
            results.append(player_info)

    return results


# --- Bloco Principal para Testes ---

if __name__ == '__main__':
    # Este bloco demonstra como usar as funções de consulta.
    # Requer os módulos 'carrega_dados' e 'estruturas'.
    import carrega_dados
    import estruturas
    import pprint # Para imprimir os dicionários de forma legível

    # 1. Carregar os dados
    print("Carregando dados...")
    players_df = carrega_dados.load_players('players.csv')
    ratings_df = carrega_dados.load_ratings('minirating.csv')
    tags_df = carrega_dados.load_tags('tags.csv')

    # 2. Construir as estruturas
    print("\nConstruindo estruturas de dados...")
    if all(df is not None for df in [players_df, ratings_df, tags_df]):
        player_id_hash = estruturas.create_player_id_hash(players_df)
        player_name_trie = estruturas.create_player_name_trie(players_df)
        user_ratings_index = estruturas.create_user_ratings_inverted_index(ratings_df)
        position_ratings_index = estruturas.create_position_ratings(players_df, ratings_df)
        tags_index = estruturas.create_tags_inverted_index(tags_df)

        print("\n--- Testando as Funções de Consulta ---")
        pp = pprint.PrettyPrinter(indent=2)

        # Teste 1: Busca por prefixo
        print("\n1. Buscando jogadores com prefixo 'Neymar':")
        result_prefix = search_players_by_prefix(player_name_trie, player_id_hash, 'Neymar')
        pp.pprint(result_prefix)

        # Teste 2: Busca por ID
        print("\n2. Buscando jogador com ID 20801:")
        result_id = search_player_by_id(player_id_hash, 20801) # Cristiano Ronaldo
        pp.pprint(result_id)

        # Teste 3: Busca por avaliações de usuário
        print("\n3. Buscando top 5 jogadores para o usuário 130556:")
        result_user = search_top_rated_players_by_user(user_ratings_index, player_id_hash, 130556)
        pp.pprint(result_user[:5]) # Mostra os 5 primeiros

        # Teste 4: Busca por posição
        print("\n4. Buscando top 5 jogadores para a posição 'GK':")
        result_pos = search_top_players_by_position(position_ratings_index, player_id_hash, 5, 'GK')
        pp.pprint(result_pos)

        # Teste 5: Busca por tags
        print("\n5. Buscando jogadores com as tags 'Dribbler' e 'Playmaker':")
        result_tags = search_players_by_tags(tags_index, player_id_hash, ['Dribbler', 'Playmaker'])
        pp.pprint(result_tags)