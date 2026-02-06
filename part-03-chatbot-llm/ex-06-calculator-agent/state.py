from typing import TypedDict, List, Annotated
import operator

class EstadoChat(TypedDict):
    mensagens: List[dict]
    resposta_atual: str
    contexto: str 