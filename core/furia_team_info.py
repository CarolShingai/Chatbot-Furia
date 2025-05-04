import os
import requests
from datetime import datetime, timedelta, timezone

class FuriaTeamInfo:
    def __init__(self, slug="furia", game="csgo"):
        """
        Inicializa a instância da FuriaTeamInfo para acessar dados da API PandaScore.

        Args:
            slug (str): Slug do time (ex: "furia" ou "furia-fe").
            game (str): Jogo alvo da API (padrão: "csgo").
        """
        self.slug = slug
        self.token = os.environ.get("PANDASCORE_KEY")
        self.base_url = "https://api.pandascore.co"
        self.team_id = None
        self.players = []
        self.game = game

    def make_request(self, endpoint, params=None):
        """
        Realiza uma requisição GET à API da PandaScore.

        Args:
            endpoint (str): Endpoint da API (ex: "teams", "matches/past").
            params (dict, optional): Parâmetros de filtro para a requisição.

        Returns:
            dict or list: Resposta JSON da API em caso de sucesso, None em caso de erro.
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        if params is None:
            params = {}
        try:
            url = f"{self.base_url}/{self.game}/{endpoint.lstrip('/')}"
            print(f"Carregando informações de url: {url}")
            response = requests.get(url, params=params, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"Erro {response.status_code}: {response.text}")
                return None
            return response.json()
        except Exception as e:
            print(f"Erro na requisição: {str(e)}")
            return None

    def get_team_furia_id(self):
        """
        Busca os dados da equipe com base no slug e armazena o ID da equipe.

        Returns:
            list: Lista de dicionários com os dados da equipe.
        """
        params = {"filter[slug]": "furia"}
        if self.slug == "furia-fe":
            params = {"filter[slug]": f"{self.slug}"}
        team_data = self.make_request("teams", params)
        if team_data and len(team_data) > 0:
            self.team_id = team_data[0]["id"]
            if "players" in team_data[0]:
                self.players = team_data[0]["players"]
            else:
                self.players = []
        return team_data

    def get_furia_players(self):
        """
        Retorna a lista de jogadores da equipe, buscando primeiro via `get_team_furia_id` se necessário.

        Returns:
            list: Lista de dicionários representando os jogadores.
        """
        if not self.players:
            self.get_team_furia_id()
        return self.players

    def get_upcoming_matches(self, limit=5):
        """
        Busca as próximas partidas da equipe.

        Args:
            limit (int): Número máximo de partidas a serem retornadas (padrão: 5).

        Returns:
            list: Lista de partidas futuras, ou None se ocorrer erro.
        """
        if not self.team_id:
            self.get_team_furia_id()
        params = {
            "filter[opponent_id]": self.team_id,
            "sort": "begin_at",
            "page[size]": limit
        }
        return self.make_request("matches/upcoming", params)

    def get_all_past_matches(self, days=90, max_pages=5):
        """
        Recupera várias páginas de partidas passadas da equipe, até um limite de dias.

        Args:
            days (int): Número máximo de dias passados a considerar (não usado diretamente aqui).
            max_pages (int): Número máximo de páginas a consultar.

        Returns:
            list: Lista de partidas passadas.
        """
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
        """
        Busca uma página de partidas passadas da equipe.

        Args:
            days (int): Número de dias de corte (não usado diretamente aqui).
            page (int): Número da página da requisição.
            per_page (int): Número de partidas por página.

        Returns:
            list: Lista de partidas da página solicitada.
        """
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
        """
        Busca as estatísticas de um jogador específico.

        Args:
            player_id (str): ID do jogador.

        Returns:
            dict: Dados estatísticos do jogador.
        """
        return self.make_request(f"csgo/players/{player_id}/stats")

    def get_tournament_results(self, tournament_id):
        """
        Retorna os resultados da equipe em um torneio específico.

        Args:
            tournament_id (str): ID do torneio.

        Returns:
            list: Lista de partidas da equipe nesse torneio.
        """
        if not self.team_id:
            self.get_team_furia_id()
        params = {
            "filter[team_id]": self.team_id,
            "sort": "-begin_at"
        }
        return self.make_request(f"csgo/tournaments/{tournament_id}/matches", params)
