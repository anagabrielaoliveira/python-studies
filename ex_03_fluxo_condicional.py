# Parte 3: LangGraph
# 3. Fluxo Condicional

# --------------------------------------------------
# 3.1 Fluxo Condicional (add_conditional_edges)
# --------------------------------------------------
# Permitem que o fluxo do agente seja dinâmico, decidindo o próximo
# nó com base no estado atual do grafo.
#
# Em vez de seguir um caminho fixo, define-se uma função de roteamento
# que analisa a saída do nó anterior e retorna o destino.
#
# Componentes principais:
# 1. Função de Roteamento: Recebe o State e retorna uma string.
# 2. Mapeamento: Associa os retornos da função aos nós do grafo.

# --------------------------------------------------
# 3.2 Funções de roteamento que retornam strings
# --------------------------------------------------
# A função recebe o State (dicionário de dados) e deve obrigatoriamente
# retornar uma string. Essa string funciona como uma chave que o
# LangGraph usará para decidir a direção.
#
# Exemplo de lógica:
# def router_function(state: MyState):
#     if "???" in state["messages"][-1].content:
#         return "search_node"
#     return "end"

# --------------------------------------------------
# 3.3 Configurando o Grafo com Mapeamento
# --------------------------------------------------
# Ao adicionar arestas condicionais, conectamos o retorno da função
# aos nomes reais dos nós registrados no workflow.
#
# workflow.add_conditional_edges(
#     "node_anterior",     # Origem do fluxo
#     router_function,     # Função de decisão
#     {                    # Dicionário de mapeamento
#         "search_node": "search", 
#         "end": END
#     }
# )

# --------------------------------------------------
# 3.4 O Sistema de "Pergunta e Resposta"
# --------------------------------------------------
# O LangGraph decide o caminho através de um ciclo de consulta:
#
# 1. Finalização: Um nó termina sua execução.
# 2. Consulta: O grafo para e entrega o Estado Atual ao roteador.
# 3. Resposta: A função devolve uma string indicando o próximo passo.
# 4. Salto: O grafo consulta o mapeamento e move o fluxo para o destino.


# --------------------------------------------------
# Exercício: Crie um sistema de triagem de tickets de suporte:
#
# - Requisitos:
# -- Estado com:
# ticket_id: str
# categoria: str (vazia inicialmente)
# prioridade: str (vazia inicialmente)
# descricao: str
# rota: lista de strings (para rastrear o caminho)
# -- Nós:
# classificar: analisa a descrição e define categoria ("tecnico", "financeiro", "geral")
# prioridade_alta: define prioridade como "alta" (para tickets técnicos)
# prioridade_normal: define prioridade como "normal" (demais casos)
# finalizar: adiciona "concluído" à rota
# -- Função de roteamento:
# Se categoria == "tecnico" → vai para prioridade_alta
# Caso contrário → vai para prioridade_normal
# --------------------------------------------------

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Definindo o Estado
class Estado(TypedDict):
    ticket_id: str
    categoria: str # vazia inicialmente
    prioridade: str # vazia inicialmente
    descricao: str
    rota: list[str] # para rastrear o caminho 

# 2. Definindo os Nós
def classificar(state:Estado):
    descricao = state['descricao'].lower()

    keywords_tecnico = ["servidor", "erro", "sistema"]
    keywords_financeiro = ["fatura", "pagamento", "cobrança"]
    
    if any(word in descricao for word in keywords_tecnico):             
        categoria = "tecnico"
    elif any(word in descricao for word in keywords_financeiro):
        categoria = "financeiro"
    else:
        categoria = "geral"

    return {
        'categoria': categoria
    }

def prioridade_alta(state:Estado):
    if state['categoria'] == "tecnico":
        return {
            'prioridade': "alta"
        }

def prioridade_normal(state:Estado):
    if state['categoria'] != "tecnico":
        return {
             'prioridade': "normal"
        }

def finalizar(state:Estado):
    return {
        'rota': state['rota'] + ["concluído"]
    }

# 3. Função de roteamento (router)
def roteamento(state:Estado):
    """
    Se categoria == "tecnico" → vai para prioridade_alta
    Caso contrário → vai para prioridade_normal
    """

    if state['categoria'] == "tecnico":
        return "alta"
    else:
        return "normal"

# 4. Montando o Grafo
workflow = StateGraph(Estado)

# 5. Adicionando os Nós (Passos)
workflow.add_node("classificar", classificar)
workflow.add_node("prioridade_normal", prioridade_normal)
workflow.add_node("prioridade_alta", prioridade_alta)
workflow.add_node("finalizar", finalizar)

# 6. Adicionando as Arestas (Fluxo)
workflow.add_edge(START, "classificar")     

workflow.add_conditional_edges(
    "classificar",
    roteamento,
    {
        "normal": "prioridade_normal",
        "alta": "prioridade_alta"
    }

)

workflow.add_edge("prioridade_normal", "finalizar")
workflow.add_edge("prioridade_alta", "finalizar")

workflow.add_edge("finalizar", END)

# 7. Compilando o Grafo
graph = workflow.compile()

# 8. Teste

# Teste 1: Ticket técnico
ticket1 = {
    "ticket_id": "T001",
    "categoria": "",
    "prioridade": "",
    "descricao": "O servidor está fora do ar",
    "rota": []
}

# Teste 2: Ticket geral
ticket2 = {
    "ticket_id": "T002",
    "categoria": "",
    "prioridade": "",
    "descricao": "Como faço para trocar minha senha?",
    "rota": []
}

resultado1 = graph.invoke(ticket1)
print(f"Ticket 1 - Categoria: {resultado1['categoria']}, Prioridade: {resultado1['prioridade']}")

resultado2 = graph.invoke(ticket2)
print(f"Ticket 2 - Categoria: {resultado2['categoria']}, Prioridade: {resultado2['prioridade']}")