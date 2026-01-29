# Parte 2: LangGraph
# 2. Primeiro Grafo - Estados e Nós

"""
Crie um grafo simples que processa pedidos de uma loja:

Requisitos:

Defina um Estado com:
    pedido_id: str
    valor: float
    status: str
    mensagens: lista de strings

Crie três nós:
    receber_pedido: adiciona mensagem "Pedido recebido" e atualiza status para "recebido"
    calcular_desconto: se valor > 100, aplica 10% de desconto e adiciona mensagem
    finalizar: atualiza status para "finalizado" e adiciona mensagem
    Monte o grafo: receber → calcular → finalizar
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Definindo o Estado
class Estado(TypedDict):
    pedido_id: str
    valor: float
    status: str
    mensagens: list[str]

# 2. Definindo os Nós
def receber_pedido(state: Estado):
    return {
        'mensagens': state['mensagens'] + ["Pedido recebido"],
        'status': "recebido"
    }

def calcular_desconto(state: Estado):
    valor_atual = state['valor']

    if valor_atual > 100:
        desconto = valor_atual * 0.1
        valor_final = valor_atual - desconto
        return{
        'valor': valor_final,
        'mensagens': state['mensagens'] + [f"Desconto de 10% aplicado"]
        }
    else:
        return {
            'valor': valor_atual,
            'mensagens': state['mensagens'] + ["Nenhum desconto aplicado"]
        }

def finalizar(state: Estado):
    return {
        'mensagens': state['mensagens'] + ["Pedido finalizado"],
        'status': "finalizado"
    }

# 3. Montando o Grafo
workflow = StateGraph(Estado)

# 4. Adicionando os Nós (Passos)
workflow.add_node("receber", receber_pedido)
workflow.add_node("desconto", calcular_desconto)
workflow.add_node("finalizar", finalizar)

# 5. Adicionando as Arestas (Fluxo)
workflow.add_edge(START, "receber")     
workflow.add_edge("receber", "desconto")    
workflow.add_edge("desconto", "finalizar")
workflow.add_edge("finalizar", END)

# 6. Compilando o Grafo
graph = workflow.compile()

# 7. Teste
estado_inicial = {
    "pedido_id": "PED001",
    "valor": 150.0,
    "status": "novo",
    "mensagens": []
}

resultado = graph.invoke(estado_inicial)
print(f"Status final: {resultado['status']}")
print(f"Valor final: {resultado['valor']}")
print(f"Mensagens: {resultado['mensagens']}")