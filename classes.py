import numpy as np
import time
import pygame
import pygame.midi

OITAVA_DEFAULT = 0
VOLUME_DEFAULT = 20
BPM_DEFAULT = 60
MAX_VOLUME = 100
MAX_OITAVA = 9
OITAVA_OFFSET = 12
VALOR_NAO_ENCONTRADO = None

class GeradorMusica:
    def __init__(self):
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
            
    def exibirTexto(self):
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

    def converteCaracteres(self):
        self.lista_saida = []
        i = 0

        while i < len(self.lista_entrada):

            string4 = self.lista_entrada[i:i+4]
            if string4 in ("BPM+", "OIT+", "OIT-"):
                self.lista_saida.append(self.mapa_transformacao[string4])
                i += 4
                continue

            caractere = self.lista_entrada[i]
            self.lista_saida.append(self.mapa_transformacao.get(caractere, VALOR_NAO_ENCONTRADO))
            i += 1


class MapaCaracteres:
    def __init__(self):
        self.dicionario_mapeamento = {}

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
    def __init__(self, instrumento_atual_id, volume_atual, oitava_atual, bpm_atual):
        self.instrumento_atual_id = instrumento_atual_id
        self.volume_atual = volume_atual
        self.oitava_atual = oitava_atual
        self.bpm_atual = bpm_atual

        self.oitava_default = OITAVA_DEFAULT
        self.max_oitava = MAX_OITAVA
        self.max_volume = MAX_VOLUME

        self.dicionario_instrumentos = {
            "PIANO": 0,
            "MUSICBOX": 10,
            "ORGAO_TUBOS": 19,
            "TROMPETE": 56,
            "FLAUTA": 73,
            "GOBLINS": 101,
            "TELEFONE": 124,
            "TIRO": 127,
        }


        self.dicionario_notas = {
            "NOTA_LA": 21,         # A0
            "NOTA_SI": 23,         # B0
            "NOTA_DO": 12,         # C0
            "NOTA_RE": 14,         # D0
            "NOTA_MI": 16,         # E0
            "NOTA_FA": 17,         # F0
            "NOTA_SOL": 19,        # G0
            "NOTA_SI_BEMOL": 22,   # Bb0 (H0)
        }




    def alterarInstrumento(self, instrumento: str):

        instrumento_id = self.dicionario_instrumentos.get(instrumento.upper().strip(), VALOR_NAO_ENCONTRADO)

        if instrumento_id != None:
            if instrumento_id == self.instrumento_atual_id:
                print(f'O instrumento "{instrumento}" já esta em uso.')
            
            else:
                self.instrumento_atual_id = instrumento_id

        else:
            print('Instrumento nao encontrado')

    def alterarVolume(self, MULTIPLICAR_VOLUME):

        if self.volume_atual * MULTIPLICAR_VOLUME > self.max_volume:
            self.volume_atual = self.max_volume
            print('O volume foi aumentado para o máximo')

        else:
            self.volume_atual = self.volume_atual * MULTIPLICAR_VOLUME
            print('O volume foi aumentado')

    def alterarOitava(self):
        if self.oitava_atual == self.max_oitava:
            self.oitava_atual = self.oitava_default

        else:
            self.oitava_atual += 1



class TocadorNotas():
        def __init__(self, controle: ControleMusica):
            self.controle = controle

            pygame.init()
            pygame.midi.init()

            self.player = pygame.midi.Output(
                pygame.midi.get_default_output_id()
            )
            # define o instrumento atual
            self.player.set_instrument(self.controle.instrumento_atual_id)


        def tocarNota(self, nome_nota_base: str):

            nota_base = self.controle.dicionario_notas.get(nome_nota_base)

            if nota_base is None:
                print(f"Nota '{nome_nota_base}' não existe.")
                return
            
            nota_final = nota_base + (OITAVA_OFFSET * self.controle.oitava_atual)

            self.player.set_instrument(self.controle.instrumento_atual_id)

            self.player.note_on(nota_final, self.controle.volume_atual)

        def pararNota(self, nome_nota_base: str):
            nota_base = self.controle.dicionario_notas.get(nome_nota_base)
            if nota_base is None:
                return
            
            nota_final = nota_base + (OITAVA_OFFSET * self.controle.oitava_atual)
            self.player.note_off(nota_final, self.controle.volume_atual)

        #definir metodo para tocar as notas em sequencia, parando nota que estava tocando antes de tocar a proxima (considerar BPM)