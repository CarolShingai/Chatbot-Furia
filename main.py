from core.chatbot import send_mensage
from core.storage import save_conversation, add_msg

# List to store all conversation
chat_store = []

def main():
	print("Bem-vindo ao FURIABOT! Digite 'sair' para encerrar.\n")
	while True:
		user_input = input("Escreva aqui sua mensagem para o FURIABOT: ")
		if user_input.lower() == "sair":
			save_conversation(chat_store)
			break
		else:
			response = send_mensage(user_input)
			add_msg(chat_store, user_input, response)
			print("FURIABOT:", response)


if __name__ == "__main__":
    main()
