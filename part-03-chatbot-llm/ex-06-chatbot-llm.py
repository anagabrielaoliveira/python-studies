# Parte 3: Bônus
# Bônus - Chatbot com LLM

import os
from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI  # ou langchain_anthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
"""
LangChain relies on components like memory, prompts, LLMs, and agents to 
form chains. LangGraph uses nodes, edges, and states do build graphs.

LangChain can passa information through the chian but doesnt easily maintain
persistent state across multiple runs. LangGrah, however, has robust state 
management. The state is a core component that all nodes can access and modify,
enablong more cmoples, context-aware behaviours

LangChain excels at sequential tasks, like retrieving data, processing it, and
outputting a result. LangGraph is better suited for complex, adaptive sysyems
that require ongoin interaction, such as virtual assistantes that need to maintain
context over long conversations

LangChain provides the building blocks,
while LangGraph organizes how those blocks interact.

pip install -U "langchain[openai]"


import os

from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-4.1")

response = model.invoke("Why do parrots talk?")
"""

from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="You are a helpful assistant! Your name is Bob."),
    HumanMessage(content="What is your name?"),
]
model = ChatOpenAI("")
# Define a chat model and invoke it with the messages
print(model.invoke(messages))






# Source - https://stackoverflow.com/q/76639580
# Posted by cserpell
# Retrieved 2026-01-31, License - CC BY-SA 4.0

import os
from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# HumanMessage(content = "Pergunta")
# AIMessage(content = "Resposta")
# SystemMessage(content = "Como defino o comportamento da AI")

from dotenv import load_dotenv

# Configure sua API key
os.environ["OPENAI_API_KEY"]

class EstadoChat(TypedDict):
    mensagens: List[dict] # lista de dicts com histórico
    resposta_atual: str
    contexto: str #informações sobre o usuário

# "system" - SystemMessage.
# "user" - HumanMessage.
# "assistant" - AIMessage.


# Implemente os nós aqui
def processar_entrada(estado: EstadoChat):
    # Adiciona mensagem do usuário ao histórico
   
    # pass 

def gerar_resposta(estado: EstadoChat): # Esse é o nó que chama a API
    # Usa LLM para gerar resposta baseada no histórico

    # Instantiation
    llm = ChatOpenAI(model="gpt-3.5-turbo") 
    
    # Invocation 
    resposta = llm.invoke(estado['mensagens'])

    
    # pass

def salvar_resposta(estado: EstadoChat):
    # Adiciona resposta ao histórico
    # estado['mensagens'].append .... role e content?
    pass

# Monte o grafo
graph = StateGraph(EstadoChat)
# ... adicione nós e edges

# Compile
app = graph.compile()

# Teste interativo
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

# Rode o chat
chat()


