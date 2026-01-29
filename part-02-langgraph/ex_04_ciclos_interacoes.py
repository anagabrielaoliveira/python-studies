# Parte 3: LangGraph
# 4 Ciclos e Iterações

# --------------------------------------------------
# 4.1 Como criar loops em LangGraph
# --------------------------------------------------
# No LangGraph, loops são implementados por meio de arestas condicionais.
# Essas arestas permitem que o fluxo do grafo retorne a um nó anterior
# ou seja encerrado, dependendo do estado atual da execução.
#
# A criação do loop envolve:
# - Um nó que será repetido
# - Uma função de decisão
# - Um mapeamento condicional que define para onde o fluxo deve seguir
#
# Essa lógica é configurada durante a construção do grafo com StateGraph.

# --------------------------------------------------
# 4.2 Condições de parada (O "Router")
# --------------------------------------------------
# É aqui que o loop infinito é evitado.
# A função condicional lê o state["loop_count"] e decide
# qual caminho o fluxo deve seguir.

from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END

class MyState(TypedDict):
    input: str
    loop_count: int

def check_limit(state: MyState):
    if state["loop_count"] >= 3:
        return "finish"    # Caminho de saída
    return "continue"      # Caminho de volta

# --------------------------------------------------
# Usar o estado para contar iterações
# --------------------------------------------------
# O State funciona como uma "memória" que persiste entre os nós.
# Para contar iterações, define-se uma chave no estado (ex: loop_count),
# que deve ser incrementada dentro do nó que será repetido.

# --------------------------------------------------
# Retornar ao mesmo nó ou nó anterior
# --------------------------------------------------
# Essa lógica acontece exclusivamente dentro do método
# add_conditional_edges.
# É aqui que você "desenha a seta" de volta no fluxo do grafo.

workflow = StateGraph(MyState)

workflow.add_conditional_edges(
    "seu_no_de_processamento",
    check_limit,  # Função de roteamento
    {
        "continue": "seu_no_de_processamento",  # Volta para o mesmo nó (loop)
        "finish": END                           # Encerra o fluxo
    }
)

# --------------------------------------------------
# Exercício: Crie um processador que retenta operações 
# até sucesso ou limite de tentativas
#
# - Requisitos:
# -- Estado:
# tarefa: str
# tentativas: int (começa em 0)
# max_tentativas: int
# sucesso: bool
# log: lista de strings
# -- Nós:
# processar: incrementa tentativas, simula processamento (50% de chance de sucesso)
# verificar: adiciona log sobre sucesso/falha
# -- Função de roteamento após verificar:
# Se sucesso == True → END
# Se tentativas >= max_tentativas → END
# Caso contrário → volta para processar
# --------------------------------------------------

import random

# 1. Definindo o Estado
class Estado(TypedDict):
    tarefa: str
    tentativas: int
    max_tentativas: int
    sucesso: bool
    log: List[str]

# 2. Definindo os Nós
def processar(state:Estado):
    """
    Incrementa tentativas e simula sucesso
    """
    return {
        "sucesso": random.choice([True, False]),
        "tentativas": state["tentativas"] + 1
    }

def verificar(state:Estado):
    """
    Adiciona log sobre sucesso/falha
    """ 
    msg = "Sucesso!" if state["sucesso"] else "Falhou"
    novo_log = [f"Tentativa {state['tentativas']}: {msg}"]
    return { 
        'log': state['log'] + novo_log 
        }

# 3. Função de roteamento (router)
def roteamento(state: Estado):
    """
    Se sucesso == True → END
    Se tentativas >= max_tentativas → END
    Caso contrário → volta para processar
    """
    if state['sucesso'] == True:
        return END
    elif state['tentativas'] >= state['max_tentativas']:
        return END
    else:
        return 'processar'

# 4. Montando o Grafo 
workflow = StateGraph(Estado)

# 5. Adicionando os Nós
workflow.add_node('processar', processar)
workflow.add_node('verificar', verificar)

# 6. Adicionando as Arestas
workflow.add_edge(START, 'processar')    
workflow.add_edge('processar', 'verificar')

workflow.add_conditional_edges(
    'verificar', # de onde sai a condição
    roteamento, 
    {
        'processar': 'processar',
        END: END
    } # retornos do roteador
)

# 7. Compilando o Grafo
graph = workflow.compile()

# 8. Teste
def processar(estado):
    estado["tentativas"] += 1
    # Simula 50% de chance de sucesso
    estado["sucesso"] = random.random() > 0.5
    return estado

# Rode algumas vezes para ver comportamentos diferentes
estado_inicial = {
    "tarefa": "Conectar ao banco de dados",
    "tentativas": 0,
    "max_tentativas": 3,
    "sucesso": False,
    "log": []
}

resultado = graph.invoke(estado_inicial)
print(f"Tentativas: {resultado['tentativas']}")
print(f"Sucesso: {resultado['sucesso']}")
print(f"Log: {resultado['log']}")

# 9. Gerando imagem do fluxo na pasta
png_data = graph.get_graph().draw_mermaid_png()

with open("ex_04_imagem_fluxo.png", "wb") as f:
    f.write(png_data)