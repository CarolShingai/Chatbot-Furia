import json
from datetime import datetime
from uuid import uuid4
import os

FILENAME = "chat_store.json"

def load_conversations():
    """
    Carrega todas as conversas armazenadas no arquivo JSON.
    
    Returns:
        list: Lista de conversas carregadas do arquivo.
              Retorna lista vazia se o arquivo não existir ou estiver vazio.
              
    Notes:
        - Verifica a existência e tamanho do arquivo antes de carregar
        - O caminho do arquivo é fixo: '/nfs/homes/cshingai/furia/chat_store.json'
    """
    path = "/nfs/homes/cshingai/furia/chat_store.json"
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, 'r') as file:
            return json.load(file)
    return []

def save_conversation(chat_store, filename="chat_store.json"):
    """
    Salva a lista de conversas em um arquivo JSON.
    
    Args:
        chat_store (list): Lista de conversas a serem salvas
        filename (str, optional): Nome do arquivo de saída. Padrão: "chat_store.json"
        
    Notes:
        - Usa encoding UTF-8 para suportar caracteres especiais
        - Formata o JSON com indentação para melhor legibilidade
    """
    with open("chat_store.json", "w", encoding="utf-8") as file:
        json.dump(chat_store, file, ensure_ascii=False, indent=2)


def create_new_conversation():
    """
    Cria uma nova conversa com estrutura inicial.
    
    Returns:
        dict: Dicionário representando uma nova conversa com:
            - id (str): UUID único
            - created_at (str): Timestamp de criação
            - messages (list): Lista vazia para armazenar mensagens
    """
    return {
		"id": str(uuid4()),
		"created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		"messages":[]
	}

def add_message(conversation, role, content):
    """
    Adiciona uma nova mensagem a uma conversa existente.
    
    Args:
        conversation (dict): Conversa à qual a mensagem será adicionada
        role (str): Papel do autor da mensagem (ex: 'user', 'assistant')
        content (str): Conteúdo/texto da mensagem
        
    Notes:
        - A mensagem é adicionada com timestamp atual
        - Modifica a conversa in-place adicionando à lista de mensagens
    """
    conversation["messages"].append({
		"role": role,
		"content": content,
		"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	})
