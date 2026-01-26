"""
Parte 1: Classes Python
Exercício 1: Fundamentos de Classes
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
        self.estado_atual="concluído"
    
    def mostrar_info(self):
        print("Nome:", self.nome, "|", "Estado:", self.estado_atual, "|","Ações realizadas:", len(self.historico))

agente1 = Agente("Explorador")
agente1.executar_acao("buscar_dados")
agente1.executar_acao("processar_dados")
agente1.mostrar_info()
agente1.finalizar()
agente1.mostrar_info()

# O método mostrar_info printa o nome (Explorador); o estado atual, de acordo com o método
# utilizado; e o histórico, que é uma lista de strings passada com o método executar_acao.





    




