"""
Parte 2: LangGraph

1. Introdução ao LangGraph
LangGraph é uma biblioteca para construir aplicações com múltiplos agentes
e fluxos complexos. 

Conceitos principais: 
1) Estado(State): Dicionário que passa por todos os nós do grafo
2) Nós (Nodes): Funções que processam e modificam o estado
3) Atestas (Edges): Conexões entre nós (podem ser condicionais)
4) Grafo (Graph): A estrutura completa do workflow

StateGraph is a class that represents de graph. 
You initialize this class by passing a state definition

As conexões têm uma seta com direção única. Se você vai do ponto A para o 
ponto B, caso queira voltar, precisa de uma nova conexão entre B e A.

Arestas: Definem o fluxo entre nós. "Depois que 



"""

# GraphState 
# Defini o estado do agente

import operator
from typing import TypedDict, Annotated, List, Union
from  langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage



# input, um historico de conversa, ter etapas intermediarias, instrução final
#sinalizando que o agente deve terminar

class AgenteState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
    # lista de resultados ou açoes do agente

from langchain_core.tools import BaseTool, StructuredTool, Tool, tool
import random

@tool("lower_case", return_direct=True)
def to_lower_case(input: str) -> str:
    """Retorna a entrada em minúsculas"""
    return input.lower()

@tool("random_number", return_direct=True)
def random_number_maker(input:str) -> str:
    """Retorna um número aleatório entre 0 e 100"""
    return str(random.randint(0,100))

tools = [to_lower_case, random_number_maker]
         
random_number_maker.run("random")

to_lower_case.run('HEITOR')


