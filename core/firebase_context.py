from core.firebase_fetch_data import load_furia_data_from_firebase, load_furia_fe_data_from_firebase
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
        opponents = [t.get('opponent', 'Adversário').get('acronym', 'adversário') for t in match.get('opponents', [])]
        line = f"- {result_emoji} " if result_emoji else "- "
        line += f"{' vs '.join(opponents)}"
        if 'scheduled_at' in match:
            line += f" 🗓️ {match['scheduled_at']}"
        elif 'begin_at' in match:
            line += f" 📅 {match['begin_at']}"
        section += line + "\n"
    return section + "\n"

def build_full_team_context(info, players, upcoming_matches, past_matches, live_matches=None, title="FURIA", emoji="🔹"):
    context = f"{emoji} **{title}** {emoji}\n\n"
    context += build_team_section(info)
    context += build_players_section(players)
    context += build_matches_section(upcoming_matches, "Próximos Jogos", "⏳")
    print(f"Info: {info}")
    if live_matches:
        context += build_matches_section(live_matches, "JOGOS AO VIVO", "🔥")
    if past_matches:
        context += "📊 **Últimos Resultados:**\n"
        for match in past_matches[:3]:
            opponents = [o.get("opponent", "Desconhecido").get("acronym", "Desconhecido") for o in match.get("opponents", [])]
            result = "✅" if match.get("winner_id") == info.get("id") else "❌"
            context += f"- {result} {' vs '.join(opponents)} 📅 {match.get('begin_at', '')}\n"
    return context + "\n"

def build_context_from_firebase(include_furia_fe=True) -> str:
    furia_info, players, upcoming_matches, past_matches = load_furia_data_from_firebase()
    context = build_full_team_context(
        info=furia_info,
        players=players,
        upcoming_matches=upcoming_matches,
        past_matches=past_matches,
        title="FURIA (CS:GO Masculino)",
        emoji="🔹"
    )
    if include_furia_fe:
        fe_info, fe_players, fe_upcoming_matches, fe_past_matches = load_furia_fe_data_from_firebase()
        context += build_full_team_context(
            info=fe_info,
            players=fe_players,
            upcoming_matches=fe_upcoming_matches,
            past_matches=fe_past_matches,
            title="FURIA FE (CS:GO Feminino)",
            emoji="🌸"
        )
    return context
