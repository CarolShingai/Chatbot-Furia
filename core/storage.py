import json
from datetime import datetime
from uuid import uuid4
import os

FILENAME = "chat_store.json"

def load_conversations():
	if os.path.exists(FILENAME):
		with open(FILENAME, "r", encoding="utf-8") as file:
			return json.load(file)
	return []

def save_conversation(chat_store, filename="chat_store.json"):
	with open("chat_store.json", "w", encoding="utf-8") as file:
		json.dump(chat_store, file, ensure_ascii=False, indent=2)

def create_new_conversation():
	return {
		"id": str(uuid4()),
		"created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		"messages":[]
	}

def add_message(conversation, role, content):
    conversation["messages"].append({
		"role": role,
		"content": content,
		"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	})
