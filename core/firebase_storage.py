from core.config.firebase_config import db

def save_team_to_firebase(team_data):
    if not team_data:
        print("Nenhum dado da FURIA para salvar.")
        return
    furia_doc = db.collection("teams").document("furia")
    furia_doc.set(team_data[0])
    
def save_players_to_firebase(players):
    players_collection = db.collection("teams").document("furia").collection("players")
    for player in players:
        player_id_str = str(player["id"])
        players_collection.document(player_id_str).set(player)
        
def save_matches_to_firebase(matches, match_type="upcoming"):
    matches_collection = db.collection("teams").document("furia").collection(match_type)
    for match in matches:
        match_id_str = str(match["id"])
        matches_collection.document(match_id_str).set(match)
        
def save_player_stats_to_firebase(player_stats, player_id):
    stats_collection = db.collection("teams").document("furia").collection("players").document(str(player_id)).collection("stats")
    for stat in player_stats:
        stat_id_str = str(stat["id"])
        stats_collection.document(stat_id_str).set(stat)
        
def save_tournament_results_to_firebase(matches, tournament_id):
    tournaments_collection = db.collection("teams").document("furia").collection("tournaments").document(str(tournament_id)).collection("matches")
    for match in matches:
        match_id_str = str(match["id"])
        tournaments_collection.document(match_id_str).set(match)
        
