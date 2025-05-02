import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# load_dotenv()

class FuriaTeamInfo:
    def __init__(self):
        self.token = os.environ.get("PANDASCORE_KEY")
        self.base_url = "https://api.pandascore.co"
        self.team_id = None
        self.players = []

    def make_request(self, endpoint, params=None):
        if params is None:
            params = {}
        params["token"] = self.token
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro na requisição: {response.status_code}")
                print(response.text)
                return None
        except Exception as e:
            print(f"Erro de conexão: {str(e)}")
            return None

    def get_team_furia_id(self):
        params = {"filter[slug]": "furia"}
        team_data = self.make_request("csgo/teams", params)
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

    def get_upcomin_matches(self, limit=5):
        params = {
            "filter[opponent_id]": self.team_id,
            "per_page": limit
            }
        if not self.team_id:
            self.get_team_furia_id()
        return self.make_request("csgo/matches/upcoming", params)

    def get_past_matches(self, page=1, per_page=10):
        params = {
            "filter[opponent_id]": self.team_id,
            "page": page,
            "per_page": per_page,
            "sort": "begin_at"
        }
        if not self.team_id:
            self.get_team_furia_id()
        return self.make_request("csgo/matches/past", params)

    def get_live_matches(self):
        params = {"filter[opponent_id]": self.team_id}
        if not self.team_id:
            self.get_team_furia_id()
        return self.make_request("csgo/matches/running", params)

    def get_player_stats(self, player_id):
        return self.make_request(f"csgo/players/{player_id}/stats")

    def get_tournamet_results(self, tournament_id):
        params = {"filter[team_id]": self.team_id}
        if not self.team_id:
            self.get_team_furia_id()
        return self.make_request("csgo/tournaments/{tournament_id}/matches", params)
