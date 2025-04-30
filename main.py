from core.games import GAME_SLUGS
from core.chatbot import send_message
from core.storage import (
    load_conversations, save_conversation, create_new_conversation, add_message)
from core.esports import *

def choose_conversation(conversations):
    if not conversations:
        print("Nenhuma conversa salva. Criando uma nova.\n")
        return create_new_conversation()
    print("Conversas disponíveis:")
    for idx, conv in enumerate(conversations):
        print(f"[{idx}] {conv['created_at']} ({len(conv['messages'])} mensagens)")
    choice = input("\nDigite o número da conversa para continuar. Ou enter para inserir uma nova.")
    if choice.isdigit() and int(choice) < len(conversations):
        return conversations[int(choice)]
    else:
        return create_new_conversation()

def detect_game_from_input(text):
    text_lower = text.lower()
    for name, slug in GAME_SLUGS.items():
        if name in text_lower:
            return slug
    return None

def handle_exit(input_lower, conversation, conversations):
    if input_lower == "sair":
        existing = [c for c in conversations if c["id"] == conversation["id"]]
        if existing:
            existing[0].update(conversation)
        else:
            conversations.append(conversation)
        save_conversation(conversations)
        return True
    return False

def main():
    furia = FuriaTeamInfo()
    conversations = load_conversations()
    conversation = choose_conversation(conversations)
    print("Bem-vindo ao FURIABOT! Digite 'sair' para encerrar.\n")
    while True:
        user_input = input("Escreva aqui sua mensagem para o FURIABOT: ")
        input_lower = user_input.lower()
        is_about_matches = any(word in input_lower for word in ["partidas", "partida", "jogo", "jogos"])
        game_slug = detect_game_from_input(user_input)
        if handle_exit(input_lower ,conversation, conversations):
            break
        # if is_about_matches:
        #     matches = get_upcoming_matches(game=game_slug)
        #     furia_reply = build_furia_match_response(game_slug)
        #     print("FURIABOT:", furia_reply)
        #     add_message(conversation, "user", user_input)
        #     add_message(conversation, "assistant", furia_reply)
        #     continue
        
        print("FURIABOT:", furia.get_furia_info())
        history = [{"role": msg["role"], "content": msg["content"]} for msg in conversation["messages"]]
        response = send_message(history, user_input)
        print("FURIABOT:", response)
        add_message(conversation, "user", user_input)
        add_message(conversation, "assistant", response)


if __name__ == "__main__":
    main()
