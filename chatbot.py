from dotenv import load_dotenv
import os
from groq import Groq

# Get saved Key
load_dotenv()

# initiate Groq client
client = Groq(api_key=os.environ.get("GROP_KEY"),)

# logic of chatbot
def send_mensage(mensage, list_msg=[]):
    list_msg.append()
    response = client.chat.completions.create(
        model ="llama3-8b-8192",
        messages = [
            {"role": "system",
             "content": "Você é o FURIABOT, o mascote digital da torcida da FURIA Esports!"
             "Fale com energia, emoção e gírias da torcida. Use emojis, expressões de hype, gifs e sempre mostre orgulho pelo time."
             },
            {
                "role": "user", "content": mensage}],
            temperature=0.8,
            max_tokens=200
    )
    return response.choices[0].message.content

# chatbot loop
while True:
    text = input("Escreva aqui sua mensagem para o FURIABOT: ")
    if text.lower() == "sair":
        break
    else:
        response = send_mensage(text)
        print("FURIABOT:", response)