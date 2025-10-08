import numpy as np


class GeradorMusica:
    def __init__(self, texto_entrada: str):
        self.texto_entrada = texto_entrada
        self.texto_convertido = None  # texto convertido sera recebido posteriormente
        self.estador_leitor = 0  # 1 para leitor em execução, 0 para leitor fora de execução
        # 1 para programa em execução, 0 para programa fora de execução
        self.estado_execucao = 0

    def iniciarExecucao(self):
        if self.estado_execucao:
            print('O programa já esta em execução')

        else:
            print('Iniciando a execução do programa')
            self.estado_execucao = 1

    def interromperExecucao(self):
        if not (self.estado_execucao):
            print('O programa não está executando')

        else:
            print('Interrompendo a execução do programa')
            self.estado_execucao = 0

    def atualizaEstado(self):
        ...

    def tratarErros(self):
        ...


class LeitorTexto:
    def __init__(self, texto_input: str):
        if texto_input is None or texto_input == "":
            self.texto_input = None
            self.lista_caracteres = None
        else:
            self.texto_input = texto_input
            self.lista_caracteres = list(texto_input)

    def lerTexto(self):
        if self.texto_input is not None:
            print(self.texto_input)
        else:
            print('Texto inválido.')

    def listarCaracteres(self):
        if self.lista_caracteres is not None:
            print(self.lista_caracteres)
        else:
            print('Lista inválida.')


class TransformaMusica:
    def __init__(self, lista_entrada, mapa_transformacao):
        self.lista_entrada = lista_entrada
        self.mapa_transformacao = mapa_transformacao
        self.lista_saida = []

    def converteCaracteres(self):
        self.lista_saida = []
        for caractere in self.lista_entrada:
            nota_atual = self.mapa_transformacao.get(caractere, -1)
            self.lista_saida.append(nota_atual)


mapa = {
    "A": "NOTA LÁ",
    "B": "NOTA DÓ",
    "C": "NOTA FÁ"
}


texto1 = LeitorTexto("AB0CABA0BACB0AB0ACBA")

transformada = TransformaMusica(texto1.lista_caracteres, mapa)

transformada.converteCaracteres()

print(transformada.lista_saida)
