# Parte 2: LangGraph
# Exercício: Mini Agente de Decisão 

# --------------------------------------------------

from typing import List, TypedDict, Optional
from langgraph.graph import StateGraph, START, END

# -------------- 1. Definindo o Estado ------------- #
class Item(TypedDict):
     nome: str
     preco: float
     quantidade: int

class Estado(TypedDict):
    itens: List[Item] # lista de dicts [{'nome': 'Monster', 'preco': 8.99, ...}, {...}]
    total: float
    cupom: Optional[str] # pode ser uma string ou None
    desconto_aplicado: float
    status: str
    problemas: List[str]
    etapa: str


# -------------- 2. Nós -------------------------- #
def validar_itens(state: Estado):
     # Verifica se há itens, se preços > 0
     #Ou seja, preciso percorrer minha lista de dicionários verificando
     #o preço dos itens 
    if not state['itens']:
         lista_vazia = [f"Não há produtos na lista"]
         return {
              'problemas': lista_vazia
              }

    for item in state['itens']:
         if item['preco'] < 0:
            preco_invalido = [f"Produto {item['nome']} com preço inválido"]
            return {
                    'problemas': preco_invalido
                    }
    return {
         'problemas': []
    }              

        #print (item)

def calcular_total(state: Estado):
    soma_total = 0
    for item in state['itens']:
        soma_total += (item['preco'] * item['quantidade'])
    return {
        'total': soma_total
    }
    
def aplicar_cupom(state: Estado):
    if state['cupom'] == "DESC10":
        valor_final = state['total'] * 0.9
    else:
        valor_final = state['total']
    return {
            'total': valor_final
        }

def verificar_estoque(state: Estado):
    for item in state['itens']:
        estoque = item['quantidade']
        if estoque > 5:
            return {
                'problemas': [f"Estoque insuficiente para {item['nome']}"],
                'total': item['preco'] * 0.0
            }
    return {
        'problemas': []
    }
    
def finalizar_compra(state: Estado):
     return {
          'status': "concluído"
     }

def cancelar(state: Estado):
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
workflow.add_node('validar_itens', validar_itens)
workflow.add_node('calcular_total', calcular_total)
workflow.add_node('aplicar_cupom', aplicar_cupom)
workflow.add_node('verificar_estoque', verificar_estoque)
workflow.add_node('finalizar_compra', finalizar_compra)
workflow.add_node('cancelar', cancelar)

# -------------- 6. Adicionando as Arestas -------- #
workflow.add_edge(START, 'validar_itens')   

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

# Teste 1: Compra bem-sucedida
carrinho1 = {
    "itens": [
        {"nome": "Livro", "preco": 50.0, "quantidade": 2},
        {"nome": "Caneta", "preco": 5.0, "quantidade": 3}
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
        {"nome": "Laptop", "preco": 2000.0, "quantidade": 10}  # Quantidade > 5
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
        {'nome': 'Monster', 'preco': 8.99, 'quantidade': 5},
        {'nome': 'Café', 'preco': 25, 'quantidade': 3},
        {'nome': 'Abacate', 'preco': -9, 'quantidade': 1}
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
