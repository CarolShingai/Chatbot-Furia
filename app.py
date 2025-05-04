from flask import Flask, request, jsonify, render_template
from core.firebase_fetch_data import initialize_furia_data
from core.chat_storage import (
    add_message, create_new_conversation)
from core.chatbot import send_message
import random

app = Flask(__name__, template_folder="template", static_folder="static")

# Lista de mensagens de abertura aleatórias com gírias de gaming/FURIA
open_message = [
    "Salve, lenda! Como posso ajudar?",
    "Pode ficar tranquilo, aqui ninguém vai te dar TK. Bora trocar uma ideia?",
    "Cheguei na paz — só headshot de informação. Como posso ajudar?",
    "Relaxa que aqui o lag é zero. Manda tua dúvida!",
    "Tô na área, e juro que não vou camperar a resposta!",
    "Se a dúvida for clutch, tamo junto pra resolver. Qual é a call?",
    "Tá na call com o FURIABOT. Pode perguntar?",
    "Relaxa, essa conversa aqui é mais safe que base no eco round.",
    "Joga na minha tela. Tô pronto pro clutch!",
    "A pantera tá on! Manda a bronca."
]

# Inicializa dados da FURIA (masculino e feminino)
initialize_furia_data()
initialize_furia_data("furia-fe")

# Cria uma nova conversa
conversation = create_new_conversation()

@app.route("/")
def index():
    """
    Rota principal que serve a página do chat.
    
    Retorna:
        Template HTML: A página index.html contendo a interface do chat
        
    Observações:
        - Usa o render_template do Flask para servir o arquivo HTML
        - O template deve estar localizado na pasta 'template'
    """
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    Processa mensagens do chat e gera respostas.
    
    Entrada JSON esperada:
        {
            "mensagem": "conteúdo da mensagem do usuário"
        }
    
    Retorna:
        Resposta JSON: Contém a resposta do chatbot no formato {"resposta": "mensagem"}
        
    Comportamento:
        - Processa a mensagem do usuário
        - Trata o comando especial "tchau" para saída
        - Mantém o histórico da conversa
        - Gera respostas usando o motor do chatbot
        
    Exemplo de Resposta:
        {
            "resposta": "A FURIA tem um histórico forte no CS:GO..."
        }
    """
    data = request.json
    user_input = data.get("mensagem", "")
    input_lower = user_input.lower()
    if input_lower == "tchau":
        return jsonify({"resposta": "GG? Beleza se precisar de mais alguma coisa é só chamar!🔥"})
    history = [{"role": msg["role"], "content": msg["content"]} for msg in conversation["messages"]]
    response = send_message(history, user_input)
    add_message(conversation, "user", user_input)
    add_message(conversation, "assistant", response)
    return jsonify({"resposta": response})

@app.route("/init_message")
def init_message():
    """
    Fornece uma mensagem de boas-vindas aleatória ao iniciar o chat.
    
    Retorna:
        Resposta JSON: Contém uma mensagem aleatória no formato {"mensagem": "texto"}
        
    Observações:
        - Seleciona aleatoriamente da lista open_message
        - Mensagens usam gírias temáticas de gaming/FURIA
    """
    message = random.choice(open_message)
    return jsonify({"mensagem": message})

if __name__ == "__main__":
    """
    Ponto principal de execução da aplicação Flask.
    
    Observações:
        - Executa o app em modo debug quando rodado diretamente
        - Modo debug fornece auto-reloader e páginas de erro detalhadas
    """
    app.run(debug=True)
