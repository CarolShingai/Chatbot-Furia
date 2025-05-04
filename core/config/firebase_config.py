import firebase_admin
from firebase_admin import credentials, firestore
import os

def get_credential_file_path():
    """
    Obtém o caminho completo do primeiro arquivo de credencial JSON encontrado no diretório de credenciais.

    Returns:
        str: Caminho absoluto para o arquivo de credencial (.json)

    Raises:
        FileNotFoundError: Se nenhum arquivo JSON for encontrado no diretório de credenciais

    Notes:
        - Procura na pasta 'credentials' dois níveis acima do diretório atual
        - Seleciona automaticamente o primeiro arquivo JSON encontrado
        - O arquivo deve ter extensão .json e ser um arquivo regular (não diretório)
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    credential_dir = os.path.join(base_dir, "credentials")
    files = [f for f in os.listdir(credential_dir) if f.endswith(".json") and os.path.isfile(os.path.join(credential_dir, f))]
    if not files:
        raise FileNotFoundError("Nenhum arquivo encontrado na pasta 'credential/'.")
    selected_file = files[0]
    full_path = os.path.join(credential_dir, selected_file)
    return full_path

def get_firestore_db():
    """
    Inicializa e retorna uma instância do cliente Firestore.

    Returns:
        google.cloud.firestore_v1.client.Client: Cliente Firestore configurado

    Notes:
        - Utiliza as credenciais obtidas através de get_credential_file_path()
        - Inicializa o app Firebase Admin apenas uma vez (evita reinicialização)
        - Requer que o arquivo de credencial seja válido para o projeto Firebase

    Example:
        >>> db = get_firestore_db()
        >>> users_ref = db.collection('users')
    """
    cred = credentials.Certificate(f"{get_credential_file_path()}")
    firebase_admin.initialize_app(cred)
    return firestore.client()

db = get_firestore_db()
