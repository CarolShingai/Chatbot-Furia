import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class FuriaTeamInfo:
    def __init__(self):
        self.token = os.environ.get("PANDASCORE_KEY")
        self.base_url = "https://api.pandascore.co"
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.team_id = None




    def search_furia_team(self, game="csgo"):
        if not game:
            game = "csgo"
        page = 1
        while page < 11:
            endpoint = f"/{game}/teams?page={page}"
            try:
                response=requests.get(self.base_url + endpoint, headers=self.headers)
                response.raise_for_status()
                teams = response.json()
                if not teams:
                    break
                for team in teams:
                    if "furia" in team.get("name", "").lower():
                        self.team_id = team.get("id")
                        return team
                page += 1
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar time da FURIA: {e}")
                return None
        print("❌ A FURIA não foi encontrada após buscar todas as páginas.")
        return None

    def get_furia_players(self):
        if not self.team_id:
            self.search_furia_team()
        endpoint = f"/teams/{self.team_id}"
        try:
            response = requests.get(self.base_url + endpoint, headers=self.headers)
            response.raise_for_status()
            team_data = response.json()
            return [p.get("name") for p in team_data.get("players", []) if p.get("name")]
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar jogadores da FURIA: {e}")
            return []

    def get_furia_info(self, game="csgo"):
        """Retorna info geral e lista de jogadores"""
        team = self.search_furia_team(game=game)
        if not team:
            return "❌ Não encontrei a FURIA nesse jogo."
        players = self.get_furia_players()
        return (
            f"🐾 **Informações da FURIA - {game.upper()}** 🐾\n"
            f"🏆 Nome: {team.get('name')}\n"
            f"🌍 Local: {team.get('location', 'Desconhecido')}\n"
            f"🔢 ID: {self.team_id}\n"
            f"👥 Jogadores: {', '.join(players) if players else 'Nenhum listado'}"
        )







PANDASCORE_TOKEN = os.environ.get("PANDASCORE_KEY")
BASE_URL = "https://api.pandascore.co/"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {PANDASCORE_TOKEN}"
}

def get_upcoming_matches(game="csgo", team="FURIA"):
    if not game:
        game = "csgo"
    endpoint = f"/{game}/matches/upcoming"
    headers = {"Authorization": f"Bearer {PANDASCORE_TOKEN}"}
    try:
        response = requests.get(BASE_URL + endpoint, headers=headers)
        response.raise_for_status()
        matches = response.json()
        team_matches = []
        for m in matches:
            for opponent in m.get("opponents", []):
                opponent_name = opponent.get("opponent", {}).get("name", "").lower()
                if team.lower() in opponent_name:
                    team_matches.append(m)
                    break
        return team_matches
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar partidas: {e}")
        return []

def format_match_teams(match):
    teams = []
    for opponent in match.get("opponents", []):
        team_name = opponent.get("opponent", {}).get("name", "Equipe desconhecida")
        teams.append(team_name)
    return " vs ".join(teams)

def format_match_time(match):
    match_time = datetime.fromisoformat(match.get("scheduled_at", "").replace("Z", "+00:00"))
    return match_time.strftime("%d/%m/%Y às %H:%M")

def format_match_league(match):
    return match.get("league", {}).get("name", "Liga desconhecida")

def format_match_details(match):
    match_format = match.get("match_type", "Formato desconhecido")
    series_type = match.get("number_of_games", 1)
    return f"Formato: {match_format} (MD{series_type})"

def build_furia_match_response(game_slug):
    matches = get_upcoming_matches(game=game_slug)
    if not matches:
        return "😢 Nenhuma partida futura da FURIA foi encontrada nesse jogo. \
        Mas a próxima vem aí, é só aguardar! 💪🐾"
    match = matches[0]  # Pega a mais próxima
    teams = format_match_teams(match)
    date = format_match_time(match)
    league = format_match_league(match)
    details = format_match_details(match)
    return (
        f"OH, QUE EMPOLGAÇÃO! 🎉🔥🎊\n\n"
        f"A PRÓXIMA PARTIDA DA FURIA É... 🤔\n\n"
        f"**{teams}**\n\n"
        f"📅 Data: {date}\n"
        f"🏆 Liga: {league}\n"
        f"🎮 {details}\n\n"
        f"ESSA SERÁ UMA BATALHA! 💥 A FURIA VAI DAR O SANGUE! VAMOOOOSSSS! 🐾🖤"
    )
