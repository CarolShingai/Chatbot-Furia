from core.config.firebase_config import db
from core.furia_team_info import FuriaTeamInfo
from core.firebase_storage import (
    save_team_to_firebase, save_players_to_firebase, save_player_stats_to_firebase, 
    save_matches_to_firebase)

def load_furia_data_from_firebase():
    furia_doc = db.collection("teams").document("furia").get()
    players_ref = db.collection("teams").document("furia").collection("players")
    upcoming_ref = db.collection("teams").document("furia").collection("upcoming_matches")
    past_ref = db.collection("teams").document("furia").collection("past_matches")
    live_ref = db.collection("teams").document("furia").collection("live_matches")

    furia_info = furia_doc.to_dict() if furia_doc.exists else {}
    players_list = [p.to_dict() for p in players_ref.stream()]
    upcoming_matches = [m.to_dict() for m in upcoming_ref.stream()]
    past_matches = [m.to_dict() for m in past_ref.stream()]
    live_matches = [m.to_dict() for m in live_ref.stream()]
    return furia_info, players_list, upcoming_matches, past_matches, live_matches

def initialize_furia_data():
    furia_info, players, upcoming, past, live = load_furia_data_from_firebase()
    if not furia_info or not players or not upcoming or not past:
        furia_api = FuriaTeamInfo()
        if not furia_info:
            furia_info = fetch_and_save_team_data(furia_api)
        if not players:
            players = fetch_and_save_players_data(furia_api)
        if not upcoming or not past:
            upcoming, past, live = fetch_and_save_matches_data(furia_api)
    return furia_info, players, upcoming, past, live

def fetch_and_save_team_data(furia_api):
    team_data = furia_api.get_team_furia_id()
    if team_data:
        save_team_to_firebase(team_data)
        return team_data[0]
    return {}

def fetch_and_save_players_data(furia_api):
    players_data = furia_api.get_furia_players()
    if players_data:
        save_players_to_firebase(players_data)
        for player in players_data:
            stats = furia_api.get_player_stats(player["id"])
            if stats:
                save_player_stats_to_firebase(stats, player["id"])
        return players_data
    return []

def fetch_and_save_matches_data(furia_api):
    upcoming_matches = furia_api.get_upcomin_matches()
    past_matches = furia_api.get_past_matches()
    live_matches = furia_api.get_live_matches()
    if upcoming_matches:
        save_matches_to_firebase(upcoming_matches, "upcoming_matches")
    if past_matches:
        save_matches_to_firebase(past_matches, "past_matches")
    if live_matches:
        save_matches_to_firebase(live_matches, "live_matches")
    return upcoming_matches or [], past_matches or [], live_matches or []