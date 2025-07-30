# Data Search and Classification System - FIFA 21

**INF01124 - Classificação e Pesquisa de Dados - UFRGS - 2024/1**

## About the Project

The goal is to build a high-performance search system for a large volume of FIFA 21 game data. The main challenge is the implementation of efficient data structures (Hash Table, Trie Tree, etc.) from scratch, without the use of high-level language libraries (such as dictionaries/dictfrom Python), to support a set of complex queries in console mode.

The system operates in two phases:

1. **Loading and Indexing:** Reading CSV files ( players.csv, rating.csv, tags.csv), processing data and building in-memory data structures.

2. **Query Interface:** An interactive loop in the console where the user can perform predefined searches.

## Architecture and Data Structures

First of all, here are the five first lines of each `.csv` file:

* **players.csv**:

```csv
sofifa_id,short_name,long_name,player_positions,nationality,club_name,league_name
158023,L. Messi,Lionel Andrés Messi Cuccittini,"RW, ST, CF",Argentina,FC Barcelona,Spain Primera Division
20801,Cristiano Ronaldo,Cristiano Ronaldo dos Santos Aveiro,"ST, LW",Portugal,Juventus,Italian Serie A
200389,J. Oblak,Jan Oblak,GK,Slovenia,Atlético Madrid,Spain Primera Division
188545,R. Lewandowski,Robert Lewandowski,ST,Poland,FC Bayern München,German 1. Bundesliga
```

* **minirating.csv** (short version of **rating.csv**):

```csv
user_id,sofifa_id,rating
52505,158023,4.0
54989,158023,5.0
5409,158023,4.5
126061,158023,5.0
2782,158023,4.0
```

* **tags.csv**:

```csv
user_id,sofifa_id,tag
17800,158023,Clinical Finisher
17800,158023,Complete Forward
17800,158023,Dribbler
17800,158023,Distance Shooter
17800,158023,FK Specialist
```

To achieve the search requirements, four main data structures have been implemented in the file **estruturas.py** and are loaded through **carrega_dados.py.**

1. **Hash Table for Players (Structure 1):**

   * **Purpose:** To store and provide quick access to each player's information.

   * **Implementation:** A Hash Table was implemented to index all 18,944 players.

     * **Key:** Player's sofifa_id.

     * **Data:** Stores player data from **players.csv** (name, positions, nationality, etc.) and aggregated information calculated from the player from **rating.csv**, such as the average rating and total rating count for each player.

     * **Collision Handling:** Collision is handled through chaining , where elements with the same hash are stored in a linked list.

2. **Trie Tree for Player Names (Structure 2):**

   * **Goal:** Support efficient prefix searches in player names.

   * **Implementation:** A Trie Tree (Prefix Tree) was built to store the long name ( long_name) of all players.

     * Each node in the tree represents a character.

     * At the end of a valid name, the sofifa_id of the player is stored to indicate the end of the string and serve as a pointer to the Player Hash Table.

3. **Hash Table for User Reviews (Structure 3):**

   * **Objective:** Map which players were evaluated by each user and with what grade.

   * **Implementation:** A Hash Table was used .

     * **Key:** user_id .

     * **Data:** A list of tuples, where each tuple contains the sofifa_idevaluated player's and the ratingassigned player's.

4. **Inverted Index with Hash Table for Tags (Structure 4):**

   * **Objective:** Find all players associated with one or more specific tags.

   * **Implementation:** An Inverted Index was created using a Hash Table .

     * **Key:** A tag (string).

     * **Data:** A list of sofifa_id of all players who have received that tag.

## Features (Supported Queries)

The system supports four types of queries, implemented in **consultas.py**:

1. `player <prefix>`:

Returns all players whose long_name starts with the given <prefix>. Results are sorted by the player's overall average rating, in descending order.

* Example: `player Neymar`

```bash
> player Neymar

Resultados para o prefixo 'Neymar':
[ { 'club_name': 'Paris Saint-Germain',
    'league_name': 'French Ligue 1',
    'long_name': 'Neymar da Silva Santos Junior',
    'nationality': 'Brazil',
    'player_positions': 'LW, CAM',
    'short_name': 'Neymar Jr',
    'sofifa_id': 190871}]

Consulta executada em 0.002950 segundos.
-----------------------------------
```

2. `user <user_id>`:

Returns the 20 highest-rated players by a given user <user_id>. Sorting is done first by the user's rating (primary) and then by the player's overall rating (secondary).

* Example: `user 118046`

```bash
> user 118046

Top jogadores avaliados pelo usuário 118046:
[{'long_name': 'Mads Sande', 'player_positions': 'CM', 'rating': 1.5, 'sofifa_id': 256417}]

Consulta executada em 0.001556 segundos.
-----------------------------------
```

3. `top<N><position>`:

Returns the <N> best players of a specific <position>, who have at least 1000 reviews. The position can be enclosed in quotation marks.

* Example: `top10 'ST'`

```bash
> top10ST

Top 10 jogadores para a posição ST:
[ {'average_rating': 5.0, 'long_name': 'Luis Alberto Suarez Diaz', 'player_positions': 'ST', 'sofifa_id': 176580},
  {'average_rating': 5.0, 'long_name': 'Anthony Martial', 'player_positions': 'ST', 'sofifa_id': 211300},
  {'average_rating': 5.0, 'long_name': 'Josip Ilicic', 'player_positions': 'CF, ST', 'sofifa_id': 200647},
  {'average_rating': 5.0, 'long_name': 'Dario Ismael Benedetto', 'player_positions': 'ST', 'sofifa_id': 215061},
  {'average_rating': 5.0, 'long_name': 'Carlos Alberto Tevez', 'player_positions': 'ST, CAM, CF', 'sofifa_id': 143001},
  {'average_rating': 4.83, 'long_name': 'Eden Hazard', 'player_positions': 'LW, ST', 'sofifa_id': 183277},
  { 'average_rating': 4.75,
    'long_name': 'Cristiano Ronaldo dos Santos Aveiro',
    'player_positions': 'ST, LW',
    'sofifa_id': 20801},
  { 'average_rating': 4.75,
    'long_name': 'Alejandro Dario Gomez',
    'player_positions': 'CAM, CF, ST',
    'sofifa_id': 143076},
  {'average_rating': 4.75, 'long_name': 'Jozy Altidore', 'player_positions': 'ST', 'sofifa_id': 176237},
  {'average_rating': 4.5, 'long_name': 'Ciro Immobile', 'player_positions': 'ST', 'sofifa_id': 192387}]

Consulta executada em 0.007636 segundos.
-----------------------------------
```

4. `tags '<tag1>' '<tag2>' ...`

Returns players who have all the listed tags. Each tag must be enclosed in quotation marks. The search is performed by the intersection of the player lists for each tag.

* Example: `tags 'Brazil' 'Dribbler'`

```bash
> tags 'Brazil' 'Dribbler'

Jogadores com as tags: ['Brazil', 'Dribbler']
[ { 'club_name': 'Juventus',
    'league_name': 'Italian Serie A',
    'long_name': 'Arthur Henrique Ramos de Oliveira Melo',
    'nationality': 'Brazil',
    'player_positions': 'CM',
    'short_name': 'Arthur',
    'sofifa_id': 230658},
  { 'club_name': 'Shakhtar Donetsk',
    'league_name': 'Ukrainian Premier League',
    'long_name': 'Taison Barcellos Freda',
    'nationality': 'Brazil',
    'player_positions': 'LM, CAM',
    'short_name': 'Taison',
    'sofifa_id': 188803},

            [...]  

  { 'club_name': 'SL Benfica',
    'league_name': 'Portuguese Liga ZON SAGRES',
    'long_name': 'Everton Sousa Soares',
    'nationality': 'Brazil',
    'player_positions': 'LM',
    'short_name': 'Everton',
    'sofifa_id': 222716}]

Consulta executada em 0.050452 segundos.
-----------------------------------
```

## How to Run the Project

* **Prerequisites:**

  * Python version 3.0 or superior
  * **Pandas** library for Python
  * All the the .csv are in the project directory

* **Installing Pandas:**

Open the terminal at the root of the project and run the following command to install Pandas:

`py -m pip install pandas`

* **Running:**

After installation, you can run the project with the following command:

`py main.py`

Once you run the project, you will see the apllication menu on your terminal. You can type `exit` to stop running.

```bash
--- Iniciando o Programa ---
Fase 1: Carregamento de dados e construção das estruturas.
Arquivo 'players.csv' carregado com sucesso.
Arquivo 'minirating.csv' carregado com sucesso.
Arquivo 'tags.csv' carregado com sucesso.
Criando tabela hash de jogadores por ID...
Tabela hash de jogadores criada com sucesso.
Criando árvore Trie para nomes de jogadores...
Árvore Trie criada com sucesso.
Criando índice invertido de avaliações por usuário...
Índice invertido de avaliações criado com sucesso.
Calculando médias de avaliação e criando estrutura por posições...
Estrutura por posições criada com sucesso.
Criando índice invertido de tags...
Índice invertido de tags criado com sucesso.
----------------------------------------
Tempo total de carregamento e construção: 12.7448 segundos.
----------------------------------------

--- Menu de Consulta de jogadores da FIFA ---
O sistema está pronto. Digite suas consultas ou 'exit' para sair.
Formatos disponíveis:
  - player <prefixo do nome>
  - user <ID do usuário>
  - top<N><posição> (ex: top5ST, top10GK)
  - tags '<tag1>' '<tag2>' ...
-----------------------------------
>
```

## License

Distributed under the MIT license. See `LICENSE.txt` for more information.

## Contact

Leonardo Santos - <leorsantos2003@gmail.com>
