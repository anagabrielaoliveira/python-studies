from langchain_core.messages import HumanMessage, SystemMessage
from graph import app
import os

# --------------- API key ---------------- #
from dotenv import load_dotenv
load_dotenv() 
os.environ["OPENAI_API_KEY"]

# ----------- Teste interativo ----------- #
def chat():
    estado = {
        "mensagens": [
            SystemMessage(content="Você é um assistente prestativo e amigável.")
        ],
        "resposta_atual": "",
        "contexto": "Usuário está aprendendo sobre AI"
    }
    
    print("Chatbot iniciado! Digite 'sair' para encerrar.\n")
    
    while True:
        user_input = input("Você: ")
        if user_input.lower() == "sair":
            break
        
        estado["mensagens"].append(HumanMessage(content=user_input))
        resultado = app.invoke(estado)  
        
        estado = resultado
        
        print(f"Bot: {resultado['resposta_atual']}\n")

chat()