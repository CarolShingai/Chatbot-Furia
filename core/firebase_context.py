from core.firebase_fetch_data import load_furia_data_from_firebase
from datetime import datetime

def build_team_section(furia_info: dict) -> str:
    section = f"🏆 **Time:** {furia_info.get('name', 'FURIA Esports')}\n"
    section += f"📍 **Localização:** {furia_info.get('location', 'Brasil')}\n"
    section += f"🎮 **Jogo Principal:** {furia_info.get('current_videogame', {}).get('name', 'CS:GO')}\n\n"
    return section

def build_players_section(players: list) -> str:
    if not players:
        return ""
    section = "👥 **Jogadores Atuais:**\n"
    for player in players[:6]:
        full_name = f"{player.get('first_name', '')} {player.get('last_name', '')}".strip()
        player_line = f"- {player.get('name', 'N/A')}"
        if full_name:
            player_line += f" ({full_name})"
        player_line += f" 🌍 {player.get('nationality', 'N/A')}\n"
        section += player_line
    return section + "\n"

def build_matches_section(matches: list, title: str, emoji: str, result_emoji: str = None) -> str:
    if not matches:
        return ""
    section = f"{emoji} **{title}:**\n"
    for match in matches[:3]:
        opponents = [t.get('name', 'Adversário') for t in match.get('opponents', [])]
        line = f"- {result_emoji} " if result_emoji else "- "
        line += f"vs {', '.join(opponents)}"
        if 'scheduled_at' in match:
            line += f" 🗓️ {match['scheduled_at']}"
        elif 'begin_at' in match:
            line += f" 📅 {match['begin_at']}"
        section += line + "\n"
    return section + "\n"

def build_context_from_firebase() -> str:
    furia_info, players, upcoming_matches, past_matches, live_matches = load_furia_data_from_firebase()
    context = "🔹 **Informações da FURIA Esports** 🔹\n\n"
    context += build_team_section(furia_info)
    context += build_players_section(players)
    context += build_matches_section(upcoming_matches, "Próximos Jogos", "⏳")
    context += build_matches_section(live_matches, "JOGOS AO VIVO", "🔥")
    if past_matches:
        context += "📊 **Últimos Resultados:**\n"
        for match in past_matches[:3]:
            opponents = match.get('opponents', [])
            if isinstance(opponents, list):
                opponents = [opponent.get('name', 'Desconhecido') for opponent in opponents]
            else:
                opponents = []
            result = "✅" if match.get('winner_id') == furia_info.get('id') else "❌"
            context += f"- {result} vs {', '.join(opponents)} 📅 {match.get('begin_at', '')}\n"
    return context