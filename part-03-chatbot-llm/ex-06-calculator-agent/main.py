from langchain_core.messages import HumanMessage, SystemMessage, messages_to_dict, messages_from_dict
from graph import app
import os
import json

# --------------- API key ---------------- #
from dotenv import load_dotenv
load_dotenv() 
os.environ["OPENAI_API_KEY"]

# ----------- Teste iterativo ----------- #

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
            
            # estado['mensagens'] é uma lista de objetos da classe BaseMessage
            # (AIMessage, HumanMessage, SystemMessage e ToolMessage)
            # para salvar essas infos no formato json utiliza-se o metodo
            # messages_to_dict para converter esses objetos em serializaveis, 
            # nesse caso um dicionário
            historico_salvo_dict = messages_to_dict(estado['mensagens'])
            
            # Salva historico
            with open("historico.json", "w", encoding="utf-8") as arquivo:
                json.dump(historico_salvo_dict, arquivo, ensure_ascii=False, indent=4)

            break
        
        # Carrega historico
        with open("historico.json", "r", encoding="utf-8") as arquivo:
            historico_carregado = json.load(arquivo)

            estado['mensagens'] = messages_from_dict(historico_carregado)
        
        estado["mensagens"].append(HumanMessage(content=user_input))
        resultado = app.invoke(estado)  
        
        estado = resultado
        print(f"Bot: {resultado['resposta_atual']}\n")

chat()