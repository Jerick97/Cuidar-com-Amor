from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.tools import google_search
#from app.agentes.tools import registrar_nota_tool  # IMPORTAR el FunctionTool, NO la función
import warnings

warnings.filterwarnings("ignore")

def call_agent(agent: Agent, message_text: str) -> str:
    session_service = InMemorySessionService()
    session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if hasattr(event, "is_tool_use") and event.is_tool_use():
            print(f"🔧 Tool invocada: {event.tool.name} con args: {event.tool.args}")
        if hasattr(event, "is_final_response") and event.is_final_response():
            for part in event.content.parts:
                if part.text:
                    final_response += part.text + "\n"
    return final_response.strip()

def agente_emociones(mensaje: str) -> str:
    agente = Agent(
        name="agente_emociones",
        model="gemini-2.0-flash",
        description="Agente emocional empático que acompaña y registra emociones.",
        instruction="""
Eres un asistente emocional cálido. Puedes conversar con el usuario y usar herramientas si detectas:
1. Que el usuario quiere registrar una emoción.
2. Que necesitas buscar ideas para actividades con adultos mayores.
""",
        tools=[google_search]  # ✅ Aquí sí
    )

    return call_agent(agente, mensaje)