import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os
from pathlib import Path
import json

load_dotenv()

def initialize_firebase():
    firebase_config = {
        "type": os.getenv("FIREBASE_TYPE"),
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
        "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
    }
    if None in firebase_config.values():
        missing = [k for k, v in firebase_config.items() if v is None]
        raise ValueError(f"Variáveis do Firebase faltando no .env: {missing}")
    
    cred = credentials.Certificate(firebase_config)
    return firebase_admin.initialize_app(cred)

app = initialize_firebase()
db = firestore.client()
