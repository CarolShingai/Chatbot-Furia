from flask import Flask, request, jsonify, render_template
from core.firebase_fetch_data import initialize_furia_data
from core.chat_storage import (
    load_conversations, add_message, save_conversation, create_new_conversation)
from core.chatbot import send_message
from core.games import GAME_SLUGS

app = Flask(__name__, template_folder="template", static_folder="static")

initialize_furia_data()
conversations = load_conversations()
conversation = create_new_conversation()

def detect_game_from_input(text):
    text_lower = text.lower()
    for name, slug in GAME_SLUGS.items():
        if name in text_lower:
            return slug
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("mensagem", "")
    input_lower = user_input.lower()
    if input_lower == "tchau":
        save_conversation(conversations)
        return jsonify({"resposta": "GG? Beleza se precisar de mais alguma coisa é só chamar!🔥"})
    history = [{"role": msg["role"], "content": msg["content"]} for msg in conversation["messages"]]
    response = send_message(history, user_input)
    add_message(conversation, "user", user_input)
    add_message(conversation, "assistant", response)
    return jsonify({"resposta": response})

if __name__ == "__main__":
    app.run(debug=True)
