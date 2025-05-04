from core.chatbot import send_message
from core.chat_storage import (
    load_conversations, save_conversation, create_new_conversation, add_message)
from core.firebase_fetch_data import initialize_furia_data

def choose_conversation(conversations):
    """
    Permite ao usuário selecionar uma conversa existente ou criar uma nova.
    
    Args:
        conversations (list): Lista de conversas disponíveis
        
    Returns:
        dict: A conversa selecionada ou uma nova conversa
        
    Behavior:
        - Se não houver conversas, cria e retorna uma nova
        - Lista todas as conversas com data e quantidade de mensagens
        - Permite ao usuário escolher pelo índice ou criar nova
    """
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

def handle_exit(input_lower, conversation, conversations):
    """
    Verifica e trata o comando de saída do usuário.
    
    Args:
        input_lower (str): Input do usuário em minúsculas
        conversation (dict): Conversa atual
        conversations (list): Lista de todas as conversas
        
    Returns:
        bool: True se foi um comando de saída, False caso contrário
        
    Side Effects:
        - Salva a conversa atual se o comando for 'sair'
        - Atualiza conversa existente ou adiciona nova à lista
    """
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
    """
    Função principal que gerencia o fluxo do chatbot FURIABOT.
    
    Fluxo de operação:
    1. Inicializa dados da FURIA (masculino e feminino)
    2. Carrega conversas existentes
    3. Permite selecionar ou criar conversa
    4. Inicia loop de interação:
       - Recebe input do usuário
       - Verifica comando de saída
       - Gera resposta do chatbot
       - Armazena mensagens no histórico
       
    Comportamento de saída:
    - Digitar 'sair' encerra o programa e salva a conversa
    """
    initialize_furia_data()
    initialize_furia_data("furia-fe")
    conversations = load_conversations()
    conversation = choose_conversation(conversations)
    print("Bem-vindo ao FURIABOT! Digite 'sair' para encerrar.\n")
    while True:
        user_input = input("Escreva aqui sua mensagem para o FURIABOT: ")
        input_lower = user_input.lower()
        if handle_exit(input_lower ,conversation, conversations):
            break
        history = [{"role": msg["role"], "content": msg["content"]} for msg in conversation["messages"]]
        response = send_message(history, user_input)
        print("FURIABOT:", response)
        add_message(conversation, "user", user_input)
        add_message(conversation, "assistant", response)

if __name__ == "__main__":
    main()
