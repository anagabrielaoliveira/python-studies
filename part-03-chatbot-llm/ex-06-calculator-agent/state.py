from typing import TypedDict, List, Annotated
import operator

class EstadoChat(TypedDict):
    mensagens: Annotated[List[dict], operator.add] 
    resposta_atual: str
    contexto: str 