from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

client = Groq(
        api_key=os.environ.get("GROP_KEY"),)

def send_mensage(mensage):
    response = client.chat.completions.create(
        model ="llama3-8b-8192",
        messages = [
            {"role": "system",
             "content": "Você é o FURIABOT, o mascote digital da torcida da FURIA Esports!"
             "Fale com energia, emoção e gírias da torcida. Use emojis, expressões de hype, gifs e sempre mostre orgulho pelo time."
             },
            {
                "role": "user", "content": mensage}],
            temperature=0.9,
            max_tokens=200
    )
    return response.choices[0].message.content
    
print(send_mensage("FURIABOT quando a FURIA surgiu?"))