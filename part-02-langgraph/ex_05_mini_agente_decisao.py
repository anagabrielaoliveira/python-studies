# Parte 2: LangGraph
# Exercício: Mini Agente de Decisão 

# --------------------------------------------------

from typing import List, TypedDict, Optional
from langgraph.graph import StateGraph, START, END

# -------------- 0. Definindo o Estoque ------------- #
ESTOQUE = {
    "camiseta": {
        'nome_estoque': "Camiseta",
        'preco_estoque': 100.0,
        'quantidade_estoque': 10
    },
    "calca": {
        'nome_estoque': "Calça",
        'preco_estoque': 200.0,
        'quantidade_estoque': 10
    },
    "laptop": {
        'nome_estoque': "Laptop",
        'preco_estoque': 2000.0,
        'quantidade_estoque': 10
    },
    "monster": {
        'nome_estoque': "Monster",
        'preco_estoque': 8.99,
        'quantidade_estoque': 10
    }
}

# -------------- 1. Definindo o Estado ------------- #
class Item(TypedDict):
    nome: str
    preco: float
    quant_estoque: int
    quant_sol: int

class Estado(TypedDict):
    itens: List[Item] # lista de dicts [{'nome': 'Monster', 'preco': 8.99, ...}, {...}]
    total: float
    cupom: Optional[str] # pode ser uma string ou None
    desconto_aplicado: float
    status: str
    problemas: List[str]
    etapa: str

# -------------- 2. Nós -------------------------- #
def acessar_estoque(state: Estado): 
    """
    Através do nome do item, procuro qual a chave do meu estoque
    associada a ele. Resgato o restante das informações a respeito do item 
    e passo para state['itens']. Por fim, retorno as atualizaçõe ao meu estado
    """
    for item in state['itens']:
        nome_procurado = item['nome'] # Procurar o nome passado

        for chave, valor in ESTOQUE.items():
            if valor['nome_estoque'] == nome_procurado:
                item['preco'] = valor['preco_estoque']
                item['quant_estoque'] = valor['quantidade_estoque']
                break # próximo item

    return state # retorna com as infos que 

def validar_itens(state: Estado):
    # Verifica se a lista existe
    if not state['itens']:
        state['problemas'].append(f"Não há produtos na lista")
        # return state - quero que continue 

    # Verifica se o preço é inválido
    for item in state['itens']:
        if item['preco'] < 0:
            state['problemas'].append(f"Produto {item['nome']} com preço inválido")
            
    return state # se nenhum erro desses 2 for encontrado, vamos ao próximo nó        

def calcular_total(state: Estado):
    # Calcula o valor total do pedido
    soma_total = 0
    for item in state['itens']:
        soma_total += (item['preco'] * item['quant_sol'])

    state['total'] = soma_total 
    return state

def aplicar_cupom(state: Estado):
    # Aplica cupom de desconto
    if state['cupom'] == "DESC10":
        valor_final = state['total'] * 0.9
    else:
        valor_final = state['total']
    return {
            'total': valor_final
        }

def verificar_estoque(state: Estado):
    # Verifica se a quantidade solicitada é maior do que o estoque disponível
    for item in state['itens']:
        if item['quant_sol'] > item['quant_estoque']:
            return {
                'problemas': [f"Estoque insuficiente para {item['nome']}"],
                'total': item['preco'] * 0.0
            }
    return {
    'problemas': []
    }
    
def finalizar_compra(state: Estado):
     # Altera status para "concluído"
     return {
          'status': "concluído"
     }

def cancelar(state: Estado):
     # Altera status para "cancelado"
     return {
          'status': "cancelado"
     }

def roteamento(state: Estado):
     if state['problemas'] == []:
        return 'proximo_passo'
     else:
        return 'cancelar'
        
# -------------- 4. Montando o Grafo -------------- #
workflow = StateGraph(Estado)

# -------------- 5. Adicionando os Nós ------------ #
workflow.add_node('acessar_estoque', acessar_estoque)
workflow.add_node('validar_itens', validar_itens)
workflow.add_node('calcular_total', calcular_total)
workflow.add_node('aplicar_cupom', aplicar_cupom)
workflow.add_node('verificar_estoque', verificar_estoque)
workflow.add_node('finalizar_compra', finalizar_compra)
workflow.add_node('cancelar', cancelar)

# -------------- 6. Adicionando as Arestas -------- #
workflow.add_edge(START, 'acessar_estoque')   
workflow.add_edge('acessar_estoque', 'validar_itens') 

workflow.add_conditional_edges(
    'validar_itens', # de onde sai a condição
    roteamento, 
    {
        'proximo_passo': 'calcular_total',
        'cancelar': 'cancelar'
    } # retornos do roteador
)

workflow.add_edge('calcular_total', 'aplicar_cupom')  
workflow.add_edge('aplicar_cupom', 'verificar_estoque')  

workflow.add_conditional_edges(
    'verificar_estoque', # de onde sai a condição
    roteamento, 
    {
        'proximo_passo': 'finalizar_compra',
        'cancelar': 'cancelar'
    } # retornos do roteador
)

workflow.add_edge('finalizar_compra', END)

# -------------- 7. Compilando o Grafo ------------- #
graph = workflow.compile()

# -------------- 8. Testes ------------------------- #

carrinho1 = {
    "itens": [
        {"nome": "Camiseta", "quant_sol": 2},
        {"nome": "Calça", "quant_sol": 3}
    ],
    "total": 0,
    "cupom": "DESC10",
    "desconto_aplicado": 0,
    "status": "novo",
    "problemas": [],
    "etapa": ""
}

carrinho2 = {
    "itens": [
        {"nome": "Laptop", "quant_sol": 80}  
    ],
    "total": 0,
    "cupom": "",
    "desconto_aplicado": 0,
    "status": "novo",
    "problemas": [],
    "etapa": ""
}

carrinho3 = {
    'itens': [
        {'nome': 'Monster',  'quant_sol': 5}
    ],
    'total': 0.0,
    'cupom': None,
    'desconto_aplicado': 0,
    'status': 'novo',
    'problemas': [],
    'etapa': ""
}

resultado1 = graph.invoke(carrinho1)
print(f"Carrinho 1 - Status: {resultado1['status']}, Total: {resultado1['total']}, Problemas: {resultado1['problemas']}")

resultado2 = graph.invoke(carrinho2)
print(f"Carrinho 2 - Status: {resultado2['status']}, Total: {resultado2['total']}, Problemas: {resultado2['problemas']}")

resultado3 = graph.invoke(carrinho3)
print(f"Carrinho 3 - Status: {resultado3['status']}, Total: {resultado3['total']}, Problemas: {resultado3['problemas']}")
