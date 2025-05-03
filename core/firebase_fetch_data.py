from core.config.firebase_config import db
from core.furia_team_info import FuriaTeamInfo
from core.firebase_storage import (
    save_team_to_firebase, save_players_to_firebase, save_player_stats_to_firebase, 
    save_matches_to_firebase)
from datetime import datetime, timedelta, timezone

def load_furia_data_from_firebase():
    furia_doc = db.collection("teams").document("furia").get()
    players_ref = db.collection("teams").document("furia").collection("players")
    upcoming_ref = db.collection("teams").document("furia").collection("upcoming_matches")
    past_ref = db.collection("teams").document("furia").collection("past_matches")

    furia_info = furia_doc.to_dict() if furia_doc.exists else {}
    players_list = [p.to_dict() for p in players_ref.stream()]
    upcoming_matches = [m.to_dict() for m in upcoming_ref.stream()]
    past_matches = [m.to_dict() for m in past_ref.stream()]
    return furia_info, players_list, upcoming_matches, past_matches

def initialize_furia_data():
    furia_info, players, upcoming, past = load_furia_data_from_firebase()
    furia_api = FuriaTeamInfo()
    if not furia_info:
        furia_info = fetch_and_save_team_data(furia_api)
    if not players:
        players = fetch_and_save_players_data(furia_api)
    upcoming, past = fetch_and_save_matches_data(furia_api)
    return furia_info, players, upcoming, past

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
    upcoming_matches = furia_api.get_upcoming_matches()
    past_matches_raw = furia_api.get_all_past_matches()
    print(f"\nDebug - Partidas passadas brutas: {len(past_matches_raw)}")
    past_matches = filter_recent_matches(past_matches_raw, max_days_old=90)
    print(f"Debug - Partidas após filtro: {len(past_matches)}")
    if past_matches:
        print(f"Exemplo de partida recente: {past_matches[0].get('begin_at')}")
        save_matches_to_firebase(past_matches, "past_matches")
    else:
        print("Nenhuma partida recente para salvar") 
    if upcoming_matches:
        save_matches_to_firebase(upcoming_matches, "upcoming_matches")
    if past_matches:
        save_matches_to_firebase(past_matches, "past_matches")
    return upcoming_matches, past_matches

from datetime import datetime, timedelta, timezone

def filter_recent_matches(matches: list, max_days_old: int = 90) -> list:
    if not matches:
        return []
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=max_days_old)
    recent_matches = []
    for match in matches:
        try:
            date_str = (match.get('begin_at') or 
                       match.get('scheduled_at') or 
                       match.get('original_scheduled_at'))
            if not date_str:
                continue
            if date_str.endswith('Z'):
                date_str = date_str[:-1] + '+00:00'
            match_date = datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)
            if match_date > cutoff_date:
                recent_matches.append(match)
        except (ValueError, TypeError, AttributeError) as e:
            print(f"Erro ao processar partida {match.get('id')}: {e}")
            continue
    return recent_matches

from core.config.firebase_config import db

def clean_old_matches():
    try:
        past_ref = db.collection("teams").document("furia").collection("past_matches")
        cutoff = datetime.now(timezone.utc) - timedelta(days=90)
        deleted_count = 0
        for doc in past_ref.stream():
            match_data = doc.to_dict()
            match_date_str = match_data.get('begin_at') or match_data.get('scheduled_at')
            if match_date_str:
                try:
                    if match_date_str.endswith('Z'):
                        match_date_str = match_date_str[:-1] + '+00:00'
                    match_date = datetime.fromisoformat(match_date_str)
                    if match_date < cutoff:
                        doc.reference.delete()
                        deleted_count += 1
                except ValueError:
                    continue
        print(f"Removidas {deleted_count} partidas antigas")
    except Exception as e:
        print(f"Erro ao limpar partidas antigas: {e}")