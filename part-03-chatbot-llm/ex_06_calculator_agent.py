# Parte 3: Bônus
# Bônus - Chatbot com LLM

# LangChain relies on components like memory, prompts, LLMs, and agents to 
# form chains. LangGraph uses nodes, edges, and states do build graphs.

# LangChain can passa information through the chian but doesnt easily maintain
# persistent state across multiple runs. LangGrah, however, has robust state 
# management. The state is a core component that all nodes can access and modify,
# enablong more cmoples, context-aware behaviours

# LangChain excels at sequential tasks, like retrieving data, processing it, and
# outputting a result. LangGraph is better suited for complex, adaptive sysyems
# that require ongoin interaction, such as virtual assistantes that need to maintain
# context over long conversations

# LangChain provides the building blocks,
# while LangGraph organizes how those blocks interact.

import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage


# HumanMessage(content = "Pergunta")
# AIMessage(content = "Resposta")
# SystemMessage(content = "Como defino o comportamento da AI")

# "system" - SystemMessage.
# "user" - HumanMessage.
# "assistant" - AIMessage.

# API key
from dotenv import load_dotenv
load_dotenv() 
os.environ["OPENAI_API_KEY"]

class EstadoChat(TypedDict):
    mensagens: List[dict] # lista de dicts com histórico
    resposta_atual: str
    contexto: str 

# Nós
def processar_entrada(estado: EstadoChat):
    # Adiciona mensagem do usuário ao histórico
    return estado # recebo o estado como ele foi definido em chat()



def gerar_resposta(estado: EstadoChat): 
    llm = ChatOpenAI(model="gpt-3.5-turbo") 
    llm_com_tool = llm.bind_tools([calculadora_simples]) 
    resposta = llm_com_tool.invoke(estado["mensagens"])
    # pegue esse histórico de menssagens e peça para o modelo decidir o 
    # próximo passo

    #print(resposta.tool_calls)
    if resposta.tool_calls: 
        estado["mensagens"].append(resposta) 
        for tool_call in resposta.tool_calls:    
            #tool_call.name #operacao_multiplicacao
            #tool_call.args # entrada_1 e entrada_2
            
            #tool_call_id = tool_call['id']
            tool_output = calculadora_simples.invoke(tool_call['args'])
            tool_msg = ToolMessage(content=str(tool_output), tool_call_id=tool_call['id'])

            print('tool msg:', tool_msg)
            estado["mensagens"].append(tool_msg)
            estado["resposta_atual"] = tool_msg.content

            return estado
            
    estado["mensagens"].append(resposta.content) #adiciona a resposta ao historico
    estado["resposta_atual"] = resposta.content #atualiza a resposta atual
        
    return estado #retorna estado atualizado

# defining the tool, binding it to a compatible language model (LLM), 
# # and then handling the execution when the model decides to use it. 


def salvar_resposta(estado: EstadoChat):
    # Adiciona resposta ao histórico
    estado["mensagens"].append('resposta_atual')
    return estado

# Grafo
graph = StateGraph(EstadoChat)

# Nós 
graph.add_node('processar_entrada', processar_entrada)
graph.add_node('gerar_resposta', gerar_resposta)
#graph.add_node('tools', tool_node) 
graph.add_node('salvar_resposta', salvar_resposta)

# Arestas 
graph.add_edge(START, 'processar_entrada')   
graph.add_edge('processar_entrada', 'gerar_resposta')
#graph.add_edge('tool', 'gerar_resposta')
graph.add_edge('gerar_resposta', 'salvar_resposta')  
graph.add_edge('salvar_resposta', END)  

# Compile
app = graph.compile()

# ----------- Teste interativo
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