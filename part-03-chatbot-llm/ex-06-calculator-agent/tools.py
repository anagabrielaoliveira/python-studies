from langchain_core.tools import tool

@tool
def calculadora_simples(
    metodo: str, 
    entrada_1: float, 
    entrada_2: float,
    ) -> str:
    """
    Ferramenta para realizar calculos matematicos basicos. 
    Argumentos:
    - metodo: A operação desejada (soma, subtracao, multiplicacao, divisao).
    - entrada_1: O primeiro numero.
    - entrada_2: O segundo numero.
    """
    if metodo == "divisao" and entrada_2 == 0:
        return "Erro: divisao por zero."
    
    operacoes = {
        "soma": entrada_1 + entrada_2,
        "subtracao": entrada_1 - entrada_2,
        "multiplicacao": entrada_1 * entrada_2,
        "divisao": entrada_1/entrada_2 
    }
    resultado = operacoes.get(metodo)
    return f"O resultado da {metodo} entre {entrada_1} e {entrada_2} e {resultado}."
        