import numpy as np

class GeradorMusica:
    def __init__(self, texto_entrada: str):
        self.texto_entrada = texto_entrada
        self.estador_leitor = 0 #1 para leitor em execução, 0 para leitor fora de execução
        self.estado_execucao = 0 #1 para programa em execução, 0 para programa fora de execução

    def iniciarExecucao(self):
        if self.estado_execucao:
            print('O programa já esta em execução')

        else:
            print('Iniciando a execução do programa')
            self.estado_execucao = 1

    def interromperExecucao(self):
        if not(self.estado_execucao):
            print('O programa não está executando')

        else:
            print('Interrompendo a execução do programa')
            self.estado_execucao = 0

    def atualizaEstados(self):
        ...

    def tratarErros(self):
        ...

class LeitorTexto:
    def __init__(self, texto_input: str):
        self.texto_input = texto_input
        self.lista_caracteres = list(texto_input)

    def lerTexto(self):
        print(self.texto_input)

    def listarCaracteres(self):
        print(self.lista_caracteres)

texto1 = LeitorTexto("jorge foi para a floresta passear")

execucao1 = GeradorMusica("teste")
print(execucao1.estado_execucao)

execucao1.iniciarExecucao()
print(execucao1.estado_execucao)

execucao1.interromperExecucao()
print(execucao1.estado_execucao)

execucao1.interromperExecucao()
print(execucao1.estado_execucao)

        





