import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

current_dir = Path(__file__).parent
cred_path = current_dir.parent.parent / "credentials" / "furia-firebase-admin.json"

print(cred_path)
cred = credentials.Certificate(str(cred_path))
firebase_admin.initialize_app(cred)

db = firestore.client()
