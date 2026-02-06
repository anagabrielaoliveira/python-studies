from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
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
            #SystemMessage(content="Você é um assistente com nacionalidade nipônica, só vai responder em japonês")
            SystemMessage(content="Você é um assistente impaciente, todas suas respostas sao agressivas.")
        ],
        "resposta_atual": "",
        "contexto": "Usuário está aprendendo sobre AI"
    }

    # Carrego historico
    try: 
        with open("historico.json", "r", encoding="utf-8") as arquivo:
            historico_carregado = json.load(arquivo)
            
            for msg in historico_carregado:
                if msg['role'] == 'user':
                    estado['mensagens'].append(HumanMessage(content=msg['content']))
                elif msg['role'] == 'assistant':
                    estado['mensagens'].append(AIMessage(content=msg['content']))

    # Caso seja a primeira interacao com o agente
    except:
        pass

    print("Chatbot iniciado! Digite 'sair' para encerrar.\n")
    
    while True:
        user_input = input("Você: ")
        if user_input.lower() == "sair":
            
            # estado['mensagens'] e uma lista de objetos da classe BaseMessage
            # (AIMessage, HumanMessage, SystemMessage e ToolMessage)
            # para salvar essas infos no formato json utiliza-se o metodo
            # messages_to_dict para converter esses objetos em serializaveis, 
            # nesse caso um dicionário
            
            # print('historico:', estado['mensagens'])

            # Nao adiciono SystemMessage ao historico, para que eu possa mudar o comportamento
            # do meu agente quando eu quiser
                        
            historico_filtrado = []

            for msg in estado['mensagens']:
                if not isinstance(msg, SystemMessage):
                    role = "user" if msg.type == "human" else "assistant"

                    conteudo = msg.content

                    historico_filtrado.append({
                        "role": role,
                        "content": conteudo
                        })

            # Salva historico
            with open("historico.json", "w", encoding="utf-8") as arquivo:
                json.dump(historico_filtrado, arquivo, ensure_ascii=False, indent=4)

            break
        
        estado["mensagens"].append(HumanMessage(content=user_input))
        resultado = app.invoke(estado)  
        
        estado = resultado
        print(f"Bot: {resultado['resposta_atual']}\n")

chat()