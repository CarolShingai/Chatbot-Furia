from core.config.firebase_config import db

def save_team_to_firebase(team_data, slug):
    if not team_data:
        print("Nenhum dado da FURIA para salvar.")
        return
    furia_doc = db.collection("teams").document(slug)
    furia_doc.set(team_data[0])

def save_players_to_firebase(players, slug):
    players_collection = db.collection("teams").document(slug).collection("players")
    for player in players:
        player_id_str = str(player["id"])
        players_collection.document(player_id_str).set(player)

def save_matches_to_firebase(matches, slug, match_type="upcoming"):
    matches_collection = db.collection("teams").document(slug).collection(match_type)
    for match in matches:
        match_id_str = str(match["id"])
        matches_collection.document(match_id_str).set(match)

def save_player_stats_to_firebase(player_stats, slug, player_id):
    stats_collection = db.collection("teams").document(slug).collection("players").document(str(player_id)).collection("stats")
    for stat in player_stats:
        stat_id_str = str(stat["id"])
        stats_collection.document(stat_id_str).set(stat)

def save_tournament_results_to_firebase(matches, slug, tournament_id):
    tournaments_collection = db.collection("teams").document(slug).collection("tournaments").document(str(tournament_id)).collection("matches")
    for match in matches:
        match_id_str = str(match["id"])
        tournaments_collection.document(match_id_str).set(match)
