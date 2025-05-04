import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path
import json

def get_credential_file_path():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    credential_dir = os.path.join(base_dir, "credentials")
    files = [f for f in os.listdir(credential_dir) if f.endswith(".json") and os.path.isfile(os.path.join(credential_dir, f))]
    if not files:
        raise FileNotFoundError("Nenhum arquivo encontrado na pasta 'credential/'.")
    selected_file = files[0]
    full_path = os.path.join(credential_dir, selected_file)
    return full_path

def get_firestore_db():
    cred = credentials.Certificate(f"{get_credential_file_path()}")
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = get_firestore_db()
