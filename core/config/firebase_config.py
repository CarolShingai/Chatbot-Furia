import firebase_admin
from firebase_admin import credentials, firestore
# from dotenv import load_dotenv
import os
from pathlib import Path
import json

# load_dotenv()

def get_firestore_db():
    cred = credentials.Certificate("credentials/furia-chatbot-firebase-admin.json")
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = get_firestore_db()
