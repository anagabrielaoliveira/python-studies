"""
Part 01 – Object-Oriented Programming
Exercise 01 – Class Fundamentals
"""
class Agente():
    def __init__(self, nome=""):
        self.nome = nome
        self.estado_atual = ""
        self.historico = []

    def executar_acao(self, acao: str):
        self.historico.append(acao)
        self.estado_atual = "executando"

    def finalizar(self):
        self.estado_atual="concluido"
    
    def mostrar_info(self):
        print(self.nome, self.estado_atual, self.historico)

agente1 = Agente("Explorador")
agente1.executar_acao("buscar_dados")
agente1.executar_acao("processar_dados")
agente1.mostrar_info()
agente1.finalizar()
agente1.mostrar_info()

# O método mostrar_info print nome (Explorador), o estado atual, de acordo com o método
# utilizado, e o histórico, que é uma lista de strings passada com o método executar_acao.





    




