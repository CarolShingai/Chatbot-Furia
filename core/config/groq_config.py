from dotenv import load_dotenv
from groq import Groq
import os

# Get saved Key
load_dotenv()

# initiate Groq client
def get_client():
    """
    Cria e retorna uma instância do cliente Groq.

    Esta função utiliza a biblioteca Groq para criar um cliente autenticado
    com base na chave de API fornecida na variável de ambiente "GROP_KEY".

    Returns:
        Groq: Uma instância do cliente Groq autenticado.

    Raises:
        KeyError: Se a variável de ambiente "GROP_KEY" não estiver definida.
        Exception: Se houver um erro ao inicializar o cliente Groq.
    """
    return Groq(api_key=os.environ.get("GROP_KEY"),)
