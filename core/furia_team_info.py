import os
import requests
from datetime import datetime, timedelta, timezone

class FuriaTeamInfo:
    def __init__(self):
        self.token = os.environ.get("PANDASCORE_KEY")
        self.base_url = "https://api.pandascore.co"
        self.team_id = None
        self.players = []
        self.game = "csgo"

    def make_request(self, endpoint, params=None):
        headers = {"Authorization": f"Bearer {self.token}"}
        if params is None:
            params = {}
        try:
            url = f"{self.base_url}/{self.game}/{endpoint.lstrip('/')}"
            print(f"Debug - Requisitando: {url}")  # Log para debug
            print(f"Debug - Parâmetros: {params}")  # Log para debug
            response = requests.get(url, params=params, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"Erro {response.status_code}: {response.text}")
                return None
            return response.json()
        except Exception as e:
            print(f"Erro na requisição: {str(e)}")
            return None

    def get_team_furia_id(self):
        params = {"filter[slug]": "furia"}
        team_data = self.make_request("teams", params)
        if team_data and len(team_data) > 0:
            self.team_id = team_data[0]["id"]
            if "players" in team_data[0]:
                self.players = team_data[0]["players"]
            else:
                self.players = []
        return team_data

    def get_furia_players(self):
        if not self.players:
            self.get_team_furia_id()
        return self.players

    def get_upcoming_matches(self, limit=5):
        if not self.team_id:
            self.get_team_furia_id()
        params = {
            "filter[opponent_id]": self.team_id,
            "sort": "begin_at",
            "page[size]": limit
        }
        return self.make_request("matches/upcoming", params)

    def get_all_past_matches(self, days=90, max_pages=5):
        all_matches = []
        for page in range(1, max_pages + 1):
            matches = self.get_past_matches(days=days, page=page)
            if not matches:
                break
            all_matches.extend(matches)
            if len(matches) < 100:
                break
        return all_matches

    def get_past_matches(self, days=30, page=1, per_page=100):
        if not self.team_id:
            self.get_team_furia_id()
        params = {
            "filter[opponent_id]": self.team_id,
            "sort": "-begin_at",
            "page[size]": per_page,
            "page[number]": page
        }
        return self.make_request("matches/past", params)

    def get_player_stats(self, player_id):
        return self.make_request(f"csgo/players/{player_id}/stats")

    def get_tournament_results(self, tournament_id):
        if not self.team_id:
            self.get_team_furia_id()
        params = {
            "filter[team_id]": self.team_id,
            "sort": "-begin_at"
        }
        return self.make_request(f"csgo/tournaments/{tournament_id}/matches", params)

