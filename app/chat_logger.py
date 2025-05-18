from pymongo import MongoClient
from datetime import datetime
from config import Config

class ChatLogger:
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client["cuidar_com_amor"]
        self.collection = self.db["chats"]

    def guardar_chat(self, usuario, agente, mensaje_usuario, respuesta_gemini):
        doc = {
            "fecha": datetime.utcnow(),
            "usuario": usuario,
            "agente": agente,
            "mensaje_usuario": mensaje_usuario,
            "respuesta_gemini": respuesta_gemini
        }
        self.collection.insert_one(doc)