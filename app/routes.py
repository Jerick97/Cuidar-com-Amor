from flask import Blueprint, request, jsonify, render_template
from app.chat_logger import ChatLogger
from config import Config
import google.generativeai as genai
from datetime import datetime
from .agents import agente_emociones
main = Blueprint('main', __name__)
logger = ChatLogger()

# Configura Gemini
genai.configure(api_key=Config.GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

@main.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json()
    usuario = data.get("usuario", "Usuario")
    agente = data.get("agente", "General")
    mensaje_usuario = data.get("mensaje", "")

    if not mensaje_usuario:
        return jsonify({"error": "Mensaje vacío"}), 400

    try:
        # Obtiene respuesta desde Gemini
        respuesta = model.generate_content(mensaje_usuario).text
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Guarda en MongoDB
    logger.guardar_chat(usuario, agente, mensaje_usuario, respuesta)

    return jsonify({
        "usuario": usuario,
        "agente": agente,
        "mensaje_usuario": mensaje_usuario,
        "respuesta": respuesta
    })
    
@main.route("/api/chat/historial")
def obtener_historial():
    # Obtener filtros de la query string
    usuario = request.args.get("usuario")
    agente = request.args.get("agente")

    # Construir el filtro dinámicamente
    filtro = {}
    if usuario:
        filtro["usuario"] = usuario
    if agente:
        filtro["agente"] = agente

    # Buscar en MongoDB con filtros aplicados
    historial = list(logger.collection.find(filtro).sort("fecha", 1))

    # Formatear los resultados
    mensajes = []
    for doc in historial:
        mensajes.append({
            "usuario": doc.get("usuario"),
            "agente": doc.get("agente"),
            "mensaje_usuario": doc.get("mensaje_usuario"),
            "respuesta_gemini": doc.get("respuesta_gemini"),
            "fecha": doc.get("fecha").isoformat()
        })

    return jsonify(mensajes)

@main.route("/api/emociones", methods=["POST"])
def emociones():
    data = request.get_json()
    mensaje = data.get("mensaje", "")

    if not mensaje:
        return jsonify({"error": "Mensaje vacío"}), 400

    respuesta = agente_emociones(mensaje)

    # ✅ Guarda en MongoDB
    logger.guardar_chat(usuario="Jerick", agente="Emociones", mensaje_usuario=mensaje, respuesta_gemini=respuesta)


    return jsonify({"respuesta": respuesta})

@main.route('/')
def index():
    return render_template('index.html')
