from langgraph.graph import StateGraph, END, START
from state import EstadoChat
from nodes import processar_entrada, gerar_resposta, usar_ferramenta, roteador

# ---------------- Grafo ----------------- #
graph = StateGraph(EstadoChat)

# ----------------- Nos ------------------ #
graph.add_node('processar_entrada', processar_entrada)
graph.add_node('gerar_resposta', gerar_resposta)
graph.add_node('usar_ferramenta', usar_ferramenta)
#graph.add_node('salvar_resposta', salvar_resposta)

# --------------- Arestas ---------------- #
graph.add_edge(START, 'processar_entrada')   
graph.add_edge('processar_entrada', 'gerar_resposta')

graph.add_conditional_edges(
    'gerar_resposta',
    roteador, 
    {
    'gerar_resposta_ferramenta': 'usar_ferramenta',
    'seguir': END
    }
)

# graph.add_edge('usar_ferramenta', 'salvar_resposta')   
# graph.add_edge('salvar_resposta', END)  
graph.add_edge('usar_ferramenta', END) 

# --------------- Compile ---------------- #
app = graph.compile()