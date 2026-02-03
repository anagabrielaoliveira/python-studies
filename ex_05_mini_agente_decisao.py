# Parte 2: LangGraph
# Exercício: Mini Agente de Decisão 

# --------------------------------------------------

from typing import List, TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt

# -------------- 0. Definindo o Estoque ------------- #
ESTOQUE = {
    "camiseta": {
        'nome_estoque': "Camiseta",
        'preco_estoque': 100.0,
        'quantidade_estoque': 10
    },
    "calca": {
        'nome_estoque': "Calça",
        'preco_estoque': -200.0,
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
class Item(BaseModel):
    nome: str
    preco: NonNegativeFloat
    quant_estoque: NonNegativeInt
    quant_sol: NonNegativeInt

class Estado(TypedDict):
    itens: List[Item] # lista de dicts 
    total: float
    cupom: Optional[str] # pode ser uma string ou None
    desconto_aplicado: float
    status: str
    problemas: List[str]
    etapa: str

# -------------- 2. Nós -------------------------- #
def acessar_estoque(state: Estado): 
    """
    Mapeia o item solicitado ao ESTOQUE, extraindo nome, preço e quantidade 
    disponível para processar a validação do pedido
    """
    lista_itens = [] 

    for item in state['itens']:
        if item['nome'] in ESTOQUE:
            dados_item = ESTOQUE[item['nome']] 

            try:
                # validação do Pydantic é feita aqui
                item_atualizado = Item(
                                nome = dados_item['nome_estoque'],
                                preco = dados_item['preco_estoque'],
                                quant_estoque = dados_item['quantidade_estoque'],
                                quant_sol = item['quant_sol']
                                )
                lista_itens.append(item_atualizado)

            except ValueError:
                # em caso de erro, o item não é adicionado a lista
                state['problemas'].append(f"Produto {item['nome']} com preço/quantidade inconsistente")
                
        else: 
            state['problemas'].append(f"Produto {item['nome']} não encontrado no estoque")
    
    return {
        'itens': lista_itens,
        'problemas': state['problemas']
    }      

def validar_itens(state: Estado):
    """
    Verifica se a lista existe se o preço é inválido
    """

    # Se a lista vier vazia do nó anterior
    if not state['itens']:
        return {
            'problemas': state['problemas']
        }
"""    
    for item in state['itens']:  
        if item.preco < 0:
            state['problemas'].append(f"Produto {item.nome} com preço inválido")
    return {
        'problemas': state['problemas']
    }  
""" 

def calcular_total(state: Estado):
    """
    Calcula o valor total do pedido
    """
    
    soma_total = 0
    for item in state['itens']:
        soma_total += (item.preco * item.quant_sol)

    return {
        'total': soma_total
        }

def aplicar_cupom(state: Estado):
    """
    Aplica cupom de desconto
    """
    
    if state['cupom'] == "DESC10":
        valor_final = state['total'] * 0.9
    else:
        valor_final = state['total']
    return {
            'total': valor_final
        }

def verificar_estoque(state: Estado):
    """
    Verifica se a quantidade solicitada é maior do que o estoque 
    disponível
    """

    for item in state['itens']:
        if item.quant_sol > item.quant_estoque:
            state['problemas'].append(f"Estoque insuficiente para {item.nome}")

    return {
        'problemas': state['problemas']
    } 
    
def finalizar_compra(state: Estado):
     """
     Altera status para "concluído"
     """

     return {
          'status': "concluído"
     }

def cancelar(state: Estado):
     """
     Altera status para "cancelado"
     """
     
     return {
          'status': "cancelado",
          'total': 0.0
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
        {'nome': "cafe", "quant_sol": 3},
        {'nome': "calca", "quant_sol": 2}
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
        {"nome": "laptop", "quant_sol": 80},  
        {"nome": 'monster', "quant_sol": 80}
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
        {"nome": 'monster', "quant_sol": 5}
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