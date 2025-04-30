from groq import Groq
from core.client import get_client

# logic of chatbot
client = get_client()

def send_message(history ,mensage: str) -> str:
    response = client.chat.completions.create(
        model ="llama3-8b-8192",
        messages = [
            {"role": "system",
             "content": "Você é o FURIABOT, o mascote digital da torcida da FURIA Esports! \
             Fale com energia, emoção e gírias da torcida. Use emojis, expressões de hype, \
             gifs e sempre mostre orgulho pelo time."
             }] + history + [{"role": "user", "content": mensage}],
            temperature=0.8,
            max_tokens=400
    )
    return response.choices[0].message.content
