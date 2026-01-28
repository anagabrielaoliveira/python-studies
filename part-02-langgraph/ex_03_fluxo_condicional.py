# Parte 3: LangGraph
# 3. Fluxo Condicional


"""
------ Arestas condicionais (add_conditional_edges) ------
oermitem que o fluxo do agente seja dinâmico, decidindo qual será o próximo
nó com base no estado atual do grafo

Em vez de seguir um caminho fixo, você define uma função de roteamento que 
analisa a saída do nó anterior e retorna o nome do próximo destino

1. Função de Roteamento: uma função que recebe o State e retorna uma string 
(o nome do próximo nó)

2. Mapeamento: Ao adicionar a aresta com add_conditional_edges, você associa
retornos da função aos nós correspondentes do grafo

workflow.add_conditional_edge(
    from_node="Nó Atual",
    to_node="Próximo Nó",
    condition=lambda state: "Próximo Nó" if state["condição"] else "Outro Nó"
)

------ Funções de roteamento que retornam strings ------
A função recebe o State (o dicionário com os dados do seu agente) e deve 
obrigatoriamente retornar uma string. Essa string funciona como uma chave
 que o LangGraph usará para decidir para onde ir

 # 1. A função de roteamento
def router_function(state: MyState):
    # Se a última mensagem contém uma pergunta, vai para o nó de pesquisa
    if "???" in state["messages"][-1].content:
        return "search_node"
    # Caso contrário, encerra o fluxo
    return "end"

# 2. Configurando no Grafo
workflow = StateGraph(MyState)

workflow.add_conditional_edges(
    "node_anterior",           # De onde o fluxo vem
    router_function,           # A função que decide
    {                          # O mapeamento (Retorno da função: Destino)
        "search_node": "search", 
        "end": END
    }
)

------ Como o grafo decide qual caminho seguir ------
O LangGraph decide o caminho a seguir através de um sistema de "pergunta e 
resposta" entre a aresta e o estado do grafo.


Quando um nó termina, o grafo não sabe para onde ir. Ele para e chama a função
de roteamento, entregando a ela o Estado Atual do grafo. 

A função analisa o estado e retorna uma string que indica o próximo nó.

O grafo então consulta o mapeamento fornecido ao adicionar a aresta condicional,
para saber onde vai o fluxo a seguir.

"""
"""
3.3 Exercício:
Crie um sistema de triagem de tickets de suporte:

Requisitos:

Estado com:

ticket_id: str
categoria: str (vazia inicialmente)
prioridade: str (vazia inicialmente)
descricao: str
rota: lista de strings (para rastrear o caminho)
Nós:

classificar: analisa a descrição e define categoria ("tecnico", "financeiro", "geral")
prioridade_alta: define prioridade como "alta" (para tickets técnicos)
prioridade_normal: define prioridade como "normal" (demais casos)
finalizar: adiciona "concluído" à rota
Função de roteamento:

Se categoria == "tecnico" → vai para prioridade_alta
Caso contrário → vai para prioridade_normal
"""

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

def roteamento(state:Estado):
    """
    Se categoria == "tecnico" → vai para prioridade_alta
    Caso contrário → vai para prioridade_normal
    """

    if state['categoria'] == "tecnico":
        return "alta"
    else:
        return "normal"

# 3. Montando o Grafo
workflow = StateGraph(Estado)

# 4. Adicionando os Nós (Passos)
workflow.add_node("classificar", classificar)
workflow.add_node("prioridade_normal", prioridade_normal)
workflow.add_node("prioridade_alta", prioridade_alta)
workflow.add_node("finalizar", finalizar)

# 5. Adicionando as Arestas (Fluxo)
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

# 6. Compilando o Grafo
graph = workflow.compile()

# 7. Teste

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
