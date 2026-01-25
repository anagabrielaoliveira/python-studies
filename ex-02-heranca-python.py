"""
Parte 1: Classes Python
Exercício 2: Herança e Métodos Especiais

---------- Revisão ----------

----- Herança em Python (class Filho(Pai)) -----
- Herança permite a criação de novas classes reutilizando e ampliando
a funcionalidade das classes existentes. 
- A classe filha herda atributos e métodos da classe pai, permitindo 
que você use a funcionalidade definida na classe principal
Use a herança quando os objetos forem naturalmente hierárquicos
Use a composição quando os objetos compartilharem funcionalidades, mas 
não estiverem relacionados

----- Classe Pai -----
class ParentClass:
    def __init__(self, attributes):
        # Initialize attributes
        pass
    def method(self):
        # Define behavior
        pass

----- Classe Filha -----
class ChildClass(ParentClass):
    def additional_method(self):
        # Define new behavior
        pass

----- Exemplo -----
Defining the Parent Class

class Person:
    def __init__(self, name, id):
        self.name = name
        self.id = id
    def display_info(self):
        return f"Name: {self.name}, ID: {self.id}"

Defining the Child Class
class Student(Person):
    def study(self):
        return f"{self.name} is studying."
    
Creating and Testing Instances
student = Student("Heitor", 12345)
print(student.display_info())  # Inherited method from Person
print(student.study())         # Method from Student

----- Herança Única -----
Ocorre quando uma classe filha herda de uma única classe pai
Útil quando um objeto compartilha propriedades comuns com uma
categoria mais ampla, mas também requer atributos ou comportamentos adicionais

----- Herança Múltipla -----
Permite que a classe filha herde de várias classes pai
Pode levar a conflitos, que o Python resolvem usando a ordem de resolução de métodos (MRO)
MRO determina a ordem que as classes são pesquisadas em busca
de métodos e atributos. 
__mro__ ou mro() pode ser usado para inspecionar a ordem de resolução de métodos

----- Herança Multinível -----
Ocorre quando uma classe filha herda de outra classe filha, e essa classe filha
herda de uma classe pai. 

----- Herança Hierárquica -----
Várias classes filhas herdam de uma única classe mãe

----- Herança Híbrida -----
Combina dois ou mais tipos de herança mencionados acima

----- Substituição de Métodos -----
class Person:
    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def get_details(self):
        return f"Name: {self.name}, ID: {self.id}"

class Student(Person):
    def __init__(self, name, id, grade):
        super().__init__(name, id)
        self.grade = grade
    
    # Overriding the get_details method
    def get_details(self):
        return f"Name: {self.name}, ID: {self.id}, Grade: {self.grade}"

A classe Student substitui o método get_detalis da classe pai, para fornecer
suas próprias implementações específicas

----- super() -----
A função super() é usada para chamar métodos da classe pai a partir da classe filha
Útil para estender ou modificar a funcionalidade de um método da classe ptrincipal
como o método construtor __init__()
Evita nomear explecitamente a classe principal, o que é útil principalmente em casos 
de herança múltipla

----- ABCs - Classes básicas abstratas -----
Classe que não pode ser usada diretamente para criar objetos.
Objetivo é definir um conjunto comum de métodos que outras classes
devem implementar 
Úteis quando deseja garantir que determinados métodos estejam sempre presentes
classes filhas

from abc import ABC, abstractmethod

class Person(ABC):
    @abstractmethod
    def get_detais(self):
        pass

A classe Person é abstrata. Exige que qualquer classe filha implemente o método
get_detais(). 

----- Polimorfismo -----
Permite que classes diferentes usem o mesmo nome de método, mas casa um pode 
implementar esse método de uma maneira diferente

----- Métodos Especiais -----
Dunder methods ou double underline
__str__: Focado no Usuário, retorna uma string legível
__repr__: Focado no Desenvolvedor, retorna uma string detalhada, usada para debugging
Se tiver um print ele chamará o método especial
"""

from abc import ABC, abstractmethod

class AgenteBase(ABC):
    """
    Classe base Agente Base
    - Atributos: nome, tipo, historico
    - Método __str__ que retorna "Agente {nome} ({tipo})"
    - Método abstrato processar(dados) que apenas adiciona ao histórico
    """

    def __init__(self, nome: str): # aqui o nome é a única coisa essencial que precisa passar ao criar o objeto
        self.nome = nome
        self.tipo = ""
        self.historico = []

    def __str__ (self):
        return f"Agente {self.nome} ({self.tipo})"

    @abstractmethod
    def processar(self, dados:list):
        pass
        """ Um método abstrato serve para dizer que as classes filhas 
        são obrigadas a criar a sua própria versão desse métodos.
        O método abstrato não deve ter lógica, ou seja, apenas define que o método
        deve existir, mas não diz como ele funciona"""

class AgenteFiltro(AgenteBase):
    """
    - tipo = "filtro"
    - processar(dados:list): retorna apenas números pares da lista
    """

    def __init__(self, nome): 
        super().__init__(nome) 
        self.tipo = "filtro"

    def processar(self, dados: list):
        self.historico = dados
        resultado1 = [dados for dados in self.historico if dados % 2 == 0]
        return resultado1

class AgenteTransformador(AgenteBase):
    """
    - tipo = "transformador"
    - processar(dados:list): retorna cada número multiplicado por 2    
    """

    def __init__(self, nome): 
        super().__init__(nome) 
        self.tipo = "transformador"

    def processar(self, dados: list):
        self.historico = dados 
        resultado2 = dados * 2 
        return resultado2 


# --- Processamento com os agentes ---

dados = [1, 2, 3, 4, 5, 6]

filtro = AgenteFiltro("FiltroNumeros")
transformador = AgenteTransformador("Duplicador")

resultado1 = filtro.processar(dados)
print(filtro)  # Deve usar __str__
print(f"Resultado: {resultado1}")

resultado2 = transformador.processar(resultado1)
print(transformador)
print(f"Resultado: {resultado2}")

# Já que meu atributo de instância self.historico está nas 2 classes filhas, não teria como definir ele no pai?