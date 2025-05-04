from core.config.firebase_config import db

def save_team_to_firebase(team_data, slug):
    """
    Salva os dados do time no Firestore na coleção 'teams'.

    Args:
        team_data (list): Lista contendo um dicionário com as informações do time.
        slug (str): Identificador do time (ex: 'furia' ou 'furia-fe').

    Returns:
        None
    """
    if not team_data:
        print("Nenhum dado da FURIA para salvar.")
        return
    furia_doc = db.collection("teams").document(slug)
    furia_doc.set(team_data[0])

def save_players_to_firebase(players, slug):
    """
    Salva os dados dos jogadores no Firestore, na subcoleção 'players' do time.

    Args:
        players (list): Lista de dicionários com os dados dos jogadores.
        slug (str): Identificador do time.

    Returns:
        None
    """
    players_collection = db.collection("teams").document(slug).collection("players")
    for player in players:
        player_id_str = str(player["id"])
        players_collection.document(player_id_str).set(player)

def save_matches_to_firebase(matches, slug, match_type="upcoming"):
    """
    Salva partidas no Firestore na subcoleção 'upcoming' ou 'past_matches'.

    Args:
        matches (list): Lista de dicionários representando partidas.
        slug (str): Identificador do time.
        match_type (str): Tipo de partida ("upcoming" ou "past_matches").

    Returns:
        None
    """
    matches_collection = db.collection("teams").document(slug).collection(match_type)
    for match in matches:
        match_id_str = str(match["id"])
        matches_collection.document(match_id_str).set(match)

def save_player_stats_to_firebase(player_stats, slug, player_id):
    """
    Salva estatísticas de um jogador no Firestore, em 'players/{player_id}/stats'.

    Args:
        player_stats (list): Lista de dicionários com estatísticas do jogador.
        slug (str): Identificador do time.
        player_id (str or int): ID do jogador.

    Returns:
        None
    """
    stats_collection = db.collection("teams").document(slug).collection("players").document(str(player_id)).collection("stats")
    for stat in player_stats:
        stat_id_str = str(stat["id"])
        stats_collection.document(stat_id_str).set(stat)

def save_tournament_results_to_firebase(matches, slug, tournament_id):
    """
    Salva partidas de um torneio específico no Firestore em 'tournaments/{tournament_id}/matches'.

    Args:
        matches (list): Lista de dicionários com os dados das partidas.
        slug (str): Identificador do time.
        tournament_id (str or int): ID do torneio.

    Returns:
        None
    """
    tournaments_collection = db.collection("teams").document(slug).collection("tournaments").document(str(tournament_id)).collection("matches")
    for match in matches:
        match_id_str = str(match["id"])
        tournaments_collection.document(match_id_str).set(match)
