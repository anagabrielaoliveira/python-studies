"""
Parte 2: LangGraph

1. Introdução ao LangGraph
O LangGraph é a biblioteca para criar fluxos de IA que não são apenas uma 
linha reta, mas sim um sistema com ciclos e decisões, onde múltiplos 
agentes podem colaborar.

--- Conceitos principais ---
1) Estado(State): Dicionário que passa por todos os nós do grafo
2) Nós (Nodes): Funções que processam e modificam o estado
3) Atestas (Edges): Conexões entre nós (podem ser condicionais)
4) Grafo (Graph): A estrutura completa do workflow


2. Definindo a "Prancheta" (TypedDict)
Antes de construir, você define o que o seu robô pode anotar. Usamos o 
TypedDict para criar um Contrato de Dados. Se você tentar anotar algo 
fora do contrato, o Python te avisa.


from typing import TypedDict, Annotated, Union
from langchain_core.messages import BaseMessage
from langchain_core.agents import AgentAction, AgentFinish
import operator

class AgenteState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    # O Annotated + operator.add faz com que novos passos sejam SOMADOS à lista, em vez de apagar os antigos
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]


3. O Engenheiro da Obra (StateGraph)
O StateGraph é a classe que você usa para montar o mapa. Você o inicia passando o seu TypedDict.


from langgraph.graph import StateGraph

# Criando o construtor baseado na nossa prancheta
workflow = StateGraph(AgenteState)


4. Instalando as Máquinas (Nodes)
Cada nó é uma função. No LangGraph, você "instala" essas funções no seu mapa usando o add_node.


def pensador_ia(state: AgenteState):
    # Lógica: Lê o state["input"], decide o que fazer
    return {"agent_outcome": "Algum resultado"}

def executor_ferramentas(state: AgenteState):
    # Lógica: Executa uma ação (ex: conta matemática)
    return {"intermediate_steps": [("ação", "resultado")]}

# Registrando no fluxo
workflow.add_node("no_agente", pensador_ia)
workflow.add_node("no_tools", executor_ferramentas)


5. Desenhando as Estradas (Edges)
As arestas dizem quem trabalha depois de quem. Existem nós especiais: START (Início) e END (Fim).


from langgraph.graph import START, END

# Define o ponto de partida
workflow.add_edge(START, "no_agente")

# Define que após a IA pensar, ela vai para as ferramentas
workflow.add_edge("no_agente", "no_tools")

# Define que após as ferramentas, ela volta para a IA (Ciclo!)
workflow.add_edge("no_tools", "no_agente")


6. Finalizando e Rodando (Compile)
Depois de desenhar tudo, você precisa "validar" o mapa para ele virar um programa executável.


# Transforma o desenho em um robô funcional
app = workflow.compile()

# Dá o "play" passando a entrada inicial
resultado = app.invoke({"input": "Olá, qual a raiz quadrada de 144?"})
"""
# ------------- EXEMPLO COMPLETO -------------- #

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. A MOCHILA (O que vamos carregar)
class EstadoSimples(TypedDict):
    nome: str

# 2. OS TRABALHADORES (As funções/Nós)
def no_gritador(state: EstadoSimples):
    print("--- Nó 1: Gritando o nome ---")
    return {"nome": state["nome"].upper()}

def no_emojizador(state: EstadoSimples):
    print("--- Nó 2: Colocando emoji ---")
    return {"nome": state["nome"] + " 🚀"}

# 3. O ENGENHEIRO (StateGraph)
workflow = StateGraph(EstadoSimples)

# 4. ADICIONANDO AS ESTAÇÕES
workflow.add_node("gritar", no_gritador)
workflow.add_node("emoji", no_emojizador)

# 5. DESENHANDO AS SETAS (O Fluxo)
workflow.add_edge(START, "gritar")     # Começa no gritar
workflow.add_edge("gritar", "emoji")    # Vai para o emoji
workflow.add_edge("emoji", END)         # Termina aqui

# 6. CRIANDO O APP E RODANDO
app = workflow.compile()

# O invoke inicia a prancheta
resultado = app.invoke({"nome": "heitor"})

print("\nResultado Final:", resultado["nome"])
