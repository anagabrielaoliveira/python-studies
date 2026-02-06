from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from state import EstadoChat
from tools import calculadora_simples

def processar_entrada(estado: EstadoChat):
    """
    Adiciona mensagem do usuario ao historico
    """
    return estado 
    
def gerar_resposta(estado: EstadoChat): 
    """
    Chama o LLM. Se houver 'tool_calls', content=""
    Retorno o historico de mensagens
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo") 
    
    llm_com_tool = llm.bind_tools([calculadora_simples]) 
    
    resposta = llm_com_tool.invoke(estado["mensagens"])
    
    estado["mensagens"].append(resposta)
    estado["resposta_atual"] = resposta.content

    return estado

def usar_ferramenta(estado: EstadoChat): 
    """
    Diferente de 'gerar_resposta' (que retorna uma AIMessage com o pedido da tool),
    esta funcao executa a logica da ferramenta e retorna uma ToolMessage que e 
    adicionado ao historico de mensagens. 
    """
    # Usa tool_calls passadas na ultima mensagem
    ultima_msg = estado['mensagens'][-1]
    tool_chamada = ultima_msg.tool_calls 

    for ferramenta in tool_chamada:
        # executa a funcao usando os argumentso passados
        tool_output = calculadora_simples.invoke(ferramenta['args'])

        # cria o objeto ToolMessage, ele vincula o resultado ao pedido original
        # através do tool_call_id, permitindo que o historico mantenha a coerencia
        tool_msg = ToolMessage(content=str(tool_output), tool_call_id=ferramenta['id'])   
    
    estado["mensagens"].append(tool_msg)
    estado["resposta_atual"] = tool_msg.content

    return estado

def roteador(estado: EstadoChat):
    """
    Logica:
    - Se a IA gerou 'tool_calls' a execucao segue para funcao usar_ferramenta'
    - Caso contrario, a IA ja entregou uma resposta final e a execucao segue para
    a funcao salvar_resposta 
    """
    #print('apos resposta:', estado['mensagens'])
    ultima_msg = estado['mensagens'][-1]

    if ultima_msg.tool_calls:
        return 'gerar_resposta_ferramenta'
    else:
        return 'seguir'

# Comentei, pois duplica as respostas adicionadas ao historico.
# Os nos nao retornam apenas a estado['resposta_atual'], pois 
# o fluxo do grafo depende de AIMessage e ToolMessage em 
# estado["mensagens"
# def salvar_resposta(estado: EstadoChat):
    # """
    # Adiciona resposta ao histórico
    # """
    # estado["mensagens"].append(resposta)
    # return estado