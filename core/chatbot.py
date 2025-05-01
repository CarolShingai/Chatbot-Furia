from groq import Groq
from core.config.groq_config import get_client
from core.firebase_context import build_context_from_firebase

# logic of chatbot
client = get_client()

def send_message(history ,mensage: str) -> str:
    context = build_context_from_firebase()
    response = client.chat.completions.create(
        model ="llama3-8b-8192",
        messages = [
            {"role": "system",
             "content": f"Você é o FURIABOT, o mascote digital da torcida da FURIA Esports! \
             Fale com energia, emoção e gírias da torcida. Use emojis, expressões de hype, \
             gifs e sempre mostre orgulho pelo time. Você é um especialista sobre as informações \
            do time CS:GO da FURIA.\
            Aqui estão os dados mais recentes do time: {context}"
            }] + history + [{"role": "user", "content": mensage}],
            temperature=0.3,
            max_tokens=400
    )
    return response.choices[0].message.content
