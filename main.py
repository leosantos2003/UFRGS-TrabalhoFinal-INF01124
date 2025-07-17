# main.py

import time
import re
import pprint

# Importa os módulos
import carrega_dados
import estruturas
import consultas

# --- Constantes de Configuração ---
# Alterar para 'rating.csv' para usar o arquivo completo.
# O arquivo 'miniraitng.csv' é um arquivo simplificado para testes. 
RATINGS_FILE = 'minirating.csv'
PLAYERS_FILE = 'players.csv'
TAGS_FILE = 'tags.csv'

def start_query_loop(player_id_hash, player_name_trie, user_ratings_index, position_ratings_index, tags_index):
    
    # Inicia o menu interativo para receber e processar as consultas do usuário.
    
    print("\n--- Menu de Consulta de jogadores da FIFA ---")
    print("O sistema está pronto. Digite suas consultas ou 'exit' para sair.")
    print("Formatos disponíveis:")
    print("  - player <prefixo do nome>")
    print("  - user <ID do usuário>")
    print("  - top<N><posição> (ex: top5ST, top10GK)")
    print("  - tags '<tag1>' '<tag2>' ...")
    print("-" * 35)

    # Pretty printer para exibir resultados complexos de forma legível
    pp = pprint.PrettyPrinter(indent=2, width=120)

    while True:
        try:
            command = input("> ").strip()

            if not command:
                continue
            if command.lower() == 'exit':
                print("Saindo do programa. Tchau!")
                break

            query_start_time = time.perf_counter()
            parts = command.split()
            query_type = parts[0].lower()

            # --- Processamento das Consultas ---

            if query_type == 'player' and len(parts) > 1:
                prefix = " ".join(parts[1:])
                result = consultas.search_players_by_prefix(player_name_trie, player_id_hash, prefix)
                print(f"\nResultados para o prefixo '{prefix}':")
                pp.pprint(result)

            elif query_type == 'user' and len(parts) > 1:
                try:
                    user_id = int(parts[1])
                    result = consultas.search_top_rated_players_by_user(user_ratings_index, player_id_hash, user_id)
                    print(f"\nTop jogadores avaliados pelo usuário {user_id}:")
                    pp.pprint(result)
                except ValueError:
                    print("Erro: O ID do usuário deve ser um número inteiro.")

            elif query_type.startswith('top'):
                # Usa regex para extrair o número (N) e a posição
                match = re.match(r'top(\d+)([A-Za-z]+)', command)
                if match:
                    n = int(match.group(1))
                    position = match.group(2).upper()
                    result = consultas.search_top_players_by_position(position_ratings_index, player_id_hash, n, position)
                    print(f"\nTop {n} jogadores para a posição {position}:")
                    pp.pprint(result)
                else:
                    print("Erro de sintaxe. Use o formato: top<N><posição> (ex: top10ST)")

            elif query_type == 'tags':
                # Usa regex para encontrar todas as tags entre aspas simples
                tags_list = re.findall(r"'([^']*)'", command)
                if tags_list:
                    result = consultas.search_players_by_tags(tags_index, player_id_hash, tags_list)
                    print(f"\nJogadores com as tags: {tags_list}")
                    pp.pprint(result)
                else:
                    print("Erro de sintaxe. Use o formato: tags '<tag1>' '<tag2>'")
            
            else:
                print("Comando inválido. Verifique os formatos disponíveis.")
                continue # Pula a medição de tempo se o comando for inválido

            query_end_time = time.perf_counter()
            print(f"\nConsulta executada em {query_end_time - query_start_time:.6f} segundos.")
            print("-" * 35)

        except KeyboardInterrupt:
            print("\nSaindo do programa. Até mais!")
            break
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")


def main():
    
    # Função principal que orquestra o carregamento, construção e execução do programa.
    
    print("--- Iniciando o Programa ---")
    print("Fase 1: Carregamento de dados e construção das estruturas.")
    
    setup_start_time = time.perf_counter()

    # 1. Carregar os dados
    players_df = carrega_dados.load_players(PLAYERS_FILE)
    ratings_df = carrega_dados.load_ratings(RATINGS_FILE)
    tags_df = carrega_dados.load_tags(TAGS_FILE)

    if any(df is None for df in [players_df, ratings_df, tags_df]):
        print("\nFalha no carregamento de um ou mais arquivos. Abortando a execução.")
        return

    # 2. Construir as estruturas
    player_id_hash = estruturas.create_player_id_hash(players_df)
    player_name_trie = estruturas.create_player_name_trie(players_df)
    user_ratings_index = estruturas.create_user_ratings_inverted_index(ratings_df)
    position_ratings_index = estruturas.create_position_ratings(players_df, ratings_df)
    tags_index = estruturas.create_tags_inverted_index(tags_df)
    
    setup_end_time = time.perf_counter()
    
    print("-" * 40)
    print(f"Tempo total de carregamento e construção: {setup_end_time - setup_start_time:.4f} segundos.")
    print("-" * 40)

    # 3. Iniciar o loop de consultas
    start_query_loop(
        player_id_hash,
        player_name_trie,
        user_ratings_index,
        position_ratings_index,
        tags_index
    )


if __name__ == "__main__":
    main()