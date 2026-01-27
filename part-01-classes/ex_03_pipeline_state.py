"""
Parte 1: Classes Python
Exercício 3: Composição e State Management

---------- Revisão ----------

Composition vs inheritance
Both used for code reuse and organizing classes, but the model 
different types of relationships

Inheritance - is as "is-a" relationship (o que é)
Composition - is a "has-a" relationship (o que faz)

- Favor composition over inheritance for more flexible and maintainabel==le
code

Desvantagem da herança:
- Heranças profundas podem ser dificeis de entender, debug e manter
- Mudanças na classe pai podem ter efeitos colaterais não intencionais
nas subclasses, o que torna o código difícil de manter e evoluir

----- Composição (classes que contêm outras classes) -----

Envolve construir objetos complexos combinando instâncias de outras classes
mais simples como atributos. Foca no que um objeto faz, usando as funcionalidades
de outros objetos, em vez do que ele é

- Ao invés de dizer: um carro é um motor (herança)
- Você diz: um carro tem um motos (composição)

Isso deixa o código mais flexível, menos frágil e mais fácil de manter

Vantagens
- Flexibilidade: o comportamento pode ser alterado em tempo de execução (runtime) 
ao trocar os componentes internos
- Acoplamento Fraco: Leva a um acoplamento fraco entre as classes, tornando o códico
mais fácil de testar e manter
- Responsabilidade Única: os componentes são geralmente focados em uma única
responsabilidade (single responsibility) e são mais reutilizáveis em diferentes
contextos

Desvantagens
- Código Repetitivo (Boilerplate): exige o encaminhamento explícito de chamadas para 
os métodos do componente (delegação), o que pode gerar código repetitivo e aumentar
a complexidade inicial.
- Complexidade de Design: Pode tornar o design do sistema mais dificil de entender 
se for usado excessivamente ou se houver muitos níveis de aninhamento
- Polimorfismo Manual: Não suporta polimorfismo automaticamente da mesma forma que a 
herança; exige trabalho adicional para garantir que diferentes componentes sigam a 
mesma interface (ex: usando typing.Protocol) 
"""
"""
from typing import Protocol

# Separar os comportamentos em classes menores e "montar" o robô injetando esses
# comportamentos

# Definimos o que é um comportamento (Interface)
class ComportamentoTarefa(Protocol): 
    # criei uma regra, e quem quiser ser ferramenta do robô, tem que seguir ela
    def executar(self) -> None: # -> None: botão serve para fazer uma ação 
        ... # ...: não vou explicar o que cada botão faz, porque cada ferramenta é única
    # qualquer peça que eu inventar do robô tem que ter um botão chamado executar

# Componentes reutilizaveis
class Limpeza:
    def executar(self):
        print("Ação: Limpando o ambiente.")

class Voo:
    def executar(self):
        print("Ação: Voando a 10 metros de altura")

# A classe principal compostas por partes
class Robo:
    def __init__(self, tarefa: ComportamentoTarefa):
        self.tarefa = tarefa # O robô "TEM UM" comportamento
    
    def ligar(self): # gatilho do corpo do robô
        print("Robô iniciado") # indicação de que ta ligada a ferramenta
        self.tarefa.executar() # robô repassando a ordem para ferramenta trabalhar
# aqui é o corpo do robô

# Encaixando as peças em robos 

# crio meu robô com uma tarefa, 
# que eu defini no construtor ser obrigatória

limpador = Robo(tarefa=Limpeza()) 
drone = Robo(tarefa=Voo())

#class Robo: - aqui nasceria vazio, ai eu faria limpador = Robo()
#    def __init__(self, tarefa=None): # O None significa "pode ser vazio"
#        self.tarefa = tarefa


# Vantagem: Mudança em tempo de execução
print("--- Upgrade de hardware ---")
limpador.tarefa = Voo() 
limpador.ligar() 
"""

"""

----- Type hints em Python -----
nome: str = "Robotino"  # Esta caixa SÓ deve ter Texto (str)
idade: int = 8          # Esta caixa SÓ deve ter Números Inteiros (int)

def __init__(self, tarefa: ComportamentoTarefa):
- : ComportamentoTarefa é a Type Hint.
- Quando alguém for criar um Robô, ele precisa entregar uma peça que siga 
o manual ComportamentoTarefa"

----- Gerenciamento de estado mutável -----
No código do robô, o "estado" é a ferramenta (self.tarefa). Como é possível 
trocar vassoura por asa, dizemos que o estado é mutável

Como gerenciar isso sem virar bagunça?
1. Controlar quem pode mexer (Encapsulamento)
self._tarefa - "_" avisa "não mexa aqui direto"

2. Evite mudanças desnecessárias
as vezes é melhor criar um robô novo do que mudar o antigo

3. Usar type hints para garantir a segurança

----- Metodos que retornam self (method chaining) -----

return self
limpador = Robo(tarefa=Limepza()
limpador.ligar().apitar()
"""

"""
3.3 Exercício
Crie um sistema de Pipeline que gerencia múltiplos agentes processando dados sequencialmente:

Requisitos:

Classe Estado:

Atributos: dados (any), mensagens (list)
Método adicionar_mensagem(msg: str) que retorna self
Método atualizar_dados(novos_dados) que retorna self
---
Classe Pipeline:

Atributo: agentes (lista de agentes)
Atributo: estado (instância de Estado)
Método adicionar_agente(agente): adiciona agente à lista
Método executar(): executa processar() de cada agente sequencialmente, atualizando o estado
Teste seu código:
"""

from ex_02_heranca import AgenteBase, AgenteFiltro, AgenteTransformador

class Estado:
    """
    O papel dessa classe é centralizar tudo que muda durante a execução
    Ele carrega os dados atuais
    O histórico, inclusive de mensagens
    O que for mudar ao longo do caminho
    """
    def __init__(self): 
        self.dados = any
        self.mensagens = [] 

    def adicionar_mensagem(self, msg: str):
        self.mensagens.append(msg) # adiciona a mensagem
        return self # encadeamento  ok 
    
    def atualizar_dados(self, novos_dados):
        self.dados = novos_dados # atualiza meus dados
        return self # encadeamento  ok 

class Pipeline:
    def __init__(self, dados_iniciais): 
        self.agentes = [] # lista de agentes
        self.estado = Estado() # recebe a instância
        self.estado.dados = dados_iniciais # quando o Pipeline nasce ele começa com esses dados dentro do estado

    def adicionar_agente(self, agente: AgenteBase): # recebe a instancia Agente
        self.agentes.append(agente) 

    def executar(self): # executa processar() de cada agente sequencialmente
        for item in self.agentes: # para cada agente eu vou processar a instância Estado
            nova_lista = item.processar(self.estado.dados)
            self.estado.atualizar_dados(nova_lista) # usa o método do estado
            self.estado.adicionar_mensagem(
                f"{item.nome} processou os dados"
            ) # usa o método do estado
        return self.estado 

from typing import List

# Reutilize os agentes do exercício 2
pipeline = Pipeline([1, 2, 3, 4, 5, 6, 7, 8])
pipeline.adicionar_agente(AgenteFiltro("Filtro1"))
pipeline.adicionar_agente(AgenteTransformador("Transformador1"))

resultado = pipeline.executar()

print(f"Dados finais: {resultado.dados}")
print(f"Mensagens: {resultado.mensagens}")
