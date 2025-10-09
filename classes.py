import numpy as np


class GeradorMusica:
    def __init__(self, texto_entrada: str):
        self.texto_entrada = texto_entrada
        self.texto_convertido = None  # texto convertido sera recebido posteriormente
        self.estador_leitor = 0  # 1 para leitor em execução, 0 para leitor fora de execução
        self.estado_execucao = 0 # 1 para programa em execução, 0 para programa fora de execução

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
        #recebe os estados dos métodos das outras classes, verifica se é possivel a execução e atualiza os estados
        ...

    def tratarErros(self):
        #verifica se foi recebido alguma flag indicando erros e, em caso positivo, toma as medidas para corrigir esses erros
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



class MapaCaracteres:
    def __init__(self, lista_caracteres=None, lista_eventos=None, caractere=None, evento=None):
        self.dicionario_mapeamento = {}

        if lista_caracteres is not None and lista_eventos is not None:
            
            if len(lista_caracteres) == len(lista_eventos):
                self.mapeiaCaracteres(lista_caracteres, lista_eventos)
            else:
                print('As listas de caracteres e eventos devem ter o mesmo tamanho.')

        if caractere is not None and evento is not None:
            self.adicionaCaractere(caractere, evento)

    def mapeiaCaracteres(self, lista_caracteres, lista_eventos):
        if len(lista_caracteres) == len(lista_eventos):
            for i in range(len(lista_caracteres)):
                caractere = lista_caracteres[i]
                evento = lista_eventos[i]
                self.dicionario_mapeamento[caractere] = evento

        else:
            print('As listas devem ter o mesmo tamanho.')

    def adicionaCaractere(self, caractere, evento):
        if caractere is None or evento is None:
            print('Caractere e evento não podem ser nulos.')
        else:
            self.dicionario_mapeamento[caractere] = evento
            print(f'Caractere "{caractere}" adicionado.')

    def excluiCaractere(self, caractere):
        if caractere in self.dicionario_mapeamento:
            self.dicionario_mapeamento.pop(caractere)
            print(f'Caractere "{caractere}" excluído.')
        else:
            print(f'Caractere "{caractere}" não encontrado.')

    def mostraMapa(self):
        if not self.dicionario_mapeamento:
            print('O mapa está vazio.')
        else:
            for chave, valor in self.dicionario_mapeamento.items():
                print(f'{chave} --> {valor}')



class ControleMusica:
    def __init__(self, instrumento_atual, volume_atual, oitava_atual):
        self.instrumento_atual = instrumento_atual
        self.volume_atual = volume_atual
        self.oitava_atual = oitava_atual
        self.max_oitava = 7
        self.oitava_default = 1
        self.max_volume = 100

    def alterarInstrumento(self, instrumento):
        if instrumento == self.instrumento_atual:
            print(f'O instrumento "{instrumento}" já esta em uso.')

        else:
            self.instrumento_atual = instrumento

    def alterarVolume(self):
        if self.volume_atual * 2 > self.volume_atual:
            self.volume_atual = self.max_volume
            print('O volume foi aumentado para o máximo')

        else:
            self.volume_atual = self.volume_atual * 2
            print('O volume foi dobrado')

    def alterarOitava(self):
        if self.oitava_atual == self.max_oitava:
            self.oitava_atual = self.oitava_default

        else:
            self.oitava_atual += 1



class TocadorNotas:
    def __init__(self, estado_player, nota, instrumento, volume, oitava):
        self.estado_player = estado_player
        self.nota = nota
        self.instrumento = instrumento
        self.volume = volume
        self.oitava = oitava

    def tocaSom(self, instrumento, volume, oitava):
        # executa comando da biblioteca para tocar uma NOTA com o INSTRUMENTO, com as configurações de VOLUME X e OITAVA Y
        ...



    







