
import pygame
import pygame.midi
import tkinter as tk
from tkinter import filedialog, messagebox, ttk #abrir depois
import pygame
import pygame.midi
import random
import time

OITAVA_DEFAULT = 0
VOLUME_DEFAULT = 60
BPM_DEFAULT = 60
MAX_VOLUME = 127
MIN_VOLUME = 0
MAX_OITAVA = 9
MIN_OITAVA = -2
OITAVA_OFFSET = 12
AUMENTO_BPM = 80
MULTIPLICA_VOLUME = 2
MAX_NOTA = MAX_INSTRUMENTO = 127
MIN_NOTA = 0

INSTRUMENTOS = {
    "Piano (0)": 0,
    "Tubular Bells (14)": 14,
    "Organ (19)": 19,
    "Bandoneon (23)": 23,
    "Guitar (27)": 27,
    "Bass (32)": 32,
    "Violin (40)": 40,
    "Trumpet (56)": 56,
    "Flute (73)": 73,
    "Ocarina (79)": 79,
    "Calliope (82)": 82,
    "Goblins (101)": 101,
    "Bagpipe (109)": 109,
    "Agogo (113)": 113,
    "Woodblock (115)": 115,
    "Telephone (124)": 124,
    "Seashore (122)": 122,
}

INSTRUMENTO_BANDONEON = INSTRUMENTOS["Bandoneon (23)"]
INSTRUMENTO_AGOGO = INSTRUMENTOS["Agogo (113)"]
INSTRUMENTO_TELEFONE = INSTRUMENTOS["Telephone (124)"]
INSTRUMENTO_ONDAS = INSTRUMENTOS["Seashore (122)"]
INSTRUMENTO_PADRAO_INICIAL = INSTRUMENTOS["Piano (0)"]

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
    def __init__(self):
        self.texto = ""
        self.caminho_arquivo = None

    def receberTextoEscrito(self, texto_digitado):
        self.texto = texto_digitado

    def abrirArquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione um arquivo de texto",
            filetypes=[("Arquivos de Texto", "*.txt")]
        )

        if caminho:
            self.caminho_arquivo = caminho
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                self.texto = arquivo.read()
            return self.texto
        
        return None

    def salvarArquivo(self):
        if self.caminho_arquivo:
            with open(self.caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                arquivo.write(self.texto)
            print(f"Arquivo salvo em: {self.caminho_arquivo}")
        else:
            caminho = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Arquivos de Texto", "*.txt")]
            )
            if caminho:
                self.caminho_arquivo = caminho
                with open(caminho, 'w', encoding='utf-8') as arquivo:
                    arquivo.write(self.texto)
                print(f"Arquivo salvo em: {self.caminho_arquivo}")


class TransformaMusica:
    def __init__(self):
        self.lista_eventos = []
        self.texto_original = ""

    def processarTexto(self, texto_entrada):
        self.texto_original = texto_entrada
        self.lista_eventos = []
        
        i = 0
        tamanho = len(texto_entrada)
        ultimo_evento_foi_nota = False
        ultima_nota_tocada = None

        while i < tamanho:
            caractere_atual = texto_entrada[i]
            
            if i + 4 <= tamanho:
                trecho = texto_entrada[i:i+4]
                
                if trecho == "BPM+":
                    self.lista_eventos.append({"tipo": "BPM", "acao": "AUMENTAR"})
                    i += 4
                    ultimo_evento_foi_nota = False
                    continue
                
                if trecho == "OIT+":
                    self.lista_eventos.append({"tipo": "OITAVA", "acao": "AUMENTAR"})
                    i += 4
                    ultimo_evento_foi_nota = False
                    continue

                if trecho == "OIT-":
                    self.lista_eventos.append({"tipo": "OITAVA", "acao": "DIMINUIR"})
                    i += 4
                    ultimo_evento_foi_nota = False
                    continue


            if caractere_atual.upper() in "ABCDEFGH":
                nota = f"NOTA_{caractere_atual.upper()}"

                if caractere_atual.upper() == "A": nota = "NOTA_LA"
                elif caractere_atual.upper() == "B": nota = "NOTA_SI"
                elif caractere_atual.upper() == "C": nota = "NOTA_DO"
                elif caractere_atual.upper() == "D": nota = "NOTA_RE"
                elif caractere_atual.upper() == "E": nota = "NOTA_MI"
                elif caractere_atual.upper() == "F": nota = "NOTA_FA"
                elif caractere_atual.upper() == "G": nota = "NOTA_SOL"
                elif caractere_atual.upper() == "H": nota = "NOTA_SI_BEMOL"

                self.lista_eventos.append({"tipo": "NOTA", "valor": nota})
                ultimo_evento_foi_nota = True
                ultima_nota_tocada = nota


            elif caractere_atual == " ":
                self.lista_eventos.append({"tipo": "VOLUME", "acao": "DOBRAR"})
            
            elif caractere_atual == "?":
                notas_possiveis = ["NOTA_LA", "NOTA_SI", "NOTA_DO", "NOTA_RE", "NOTA_MI", "NOTA_FA", "NOTA_SOL"]
                nota_random = random.choice(notas_possiveis)
                self.lista_eventos.append({"tipo": "NOTA", "valor": nota_random})
                ultimo_evento_foi_nota = True
                ultima_nota_tocada = nota_random

            elif caractere_atual == "\n":
                valores_possiveis = list(INSTRUMENTOS.values())
                instrumento_aleatorio = random.choice(valores_possiveis)
                
                self.lista_eventos.append({"tipo": "INSTRUMENTO", "valor": instrumento_aleatorio})
                ultimo_evento_foi_nota = False

            elif caractere_atual == "!":
                self.lista_eventos.append({"tipo": "INSTRUMENTO", "valor": INSTRUMENTO_BANDONEON}) 
                ultimo_evento_foi_nota = False

            elif caractere_atual == ";":
                self.lista_eventos.append({"tipo": "PAUSA"})
                ultimo_evento_foi_nota = False
            
            elif caractere_atual == ",":
                self.lista_eventos.append({"tipo": "INSTRUMENTO", "valor": INSTRUMENTO_AGOGO}) 
                ultimo_evento_foi_nota = False

            elif caractere_atual.isdigit():
                valor_digito = int(caractere_atual)
                self.lista_eventos.append({"tipo": "INSTRUMENTO_SOMA", "valor": valor_digito})
                ultimo_evento_foi_nota = False

            elif caractere_atual.upper() in "OIU":
                if ultimo_evento_foi_nota and ultima_nota_tocada:
                    self.lista_eventos.append({"tipo": "NOTA", "valor": ultima_nota_tocada})
                else:
                    self.lista_eventos.append({"tipo": "INSTRUMENTO", "valor": INSTRUMENTO_TELEFONE}) 
                
                ultimo_evento_foi_nota = False

            else:
                pass 

            i += 1

        return self.lista_eventos


class TocadorNotas:
    def __init__(self, bpm_inicial=BPM_DEFAULT, volume_inicial=VOLUME_DEFAULT, oitava_inicial=OITAVA_DEFAULT, instrumento_inicial=INSTRUMENTO_PADRAO_INICIAL):
        self.bpm_atual = bpm_inicial
        self.volume_atual = volume_inicial
        self.oitava_atual = oitava_inicial
        self.instrumento_atual_id = instrumento_inicial
        self.player = None

        self.mapa_notas_midi = {
            "NOTA_DO": 60,
            "NOTA_RE": 62,
            "NOTA_MI": 64,
            "NOTA_FA": 65,
            "NOTA_SOL": 67,
            "NOTA_LA": 69,
            "NOTA_SI": 71,
            "NOTA_SI_BEMOL": 70
        }
        
        pygame.init()
        pygame.midi.init()
        default_id = pygame.midi.get_default_output_id()
        self.player = pygame.midi.Output(default_id)
        self.player.set_instrument(self.instrumento_atual_id)
        print("[MIDI] Player inicializado.")


    def calcularBPM(self):
        return 60.0 / self.bpm_atual

    def tocarNota(self, nome_nota: str, duracao: float):
        if not self.player: 
            return
        
        nota_base = self.mapa_notas_midi.get(nome_nota)
        if nota_base is None:
            return
            
        nota_final = nota_base + (OITAVA_OFFSET * self.oitava_atual)
        nota_final = max(MIN_NOTA, min(MAX_NOTA, nota_final))

        self.player.note_on(nota_final, self.volume_atual)
        time.sleep(duracao)
        self.player.note_off(nota_final, self.volume_atual)
        
    def pausar(self, duracao: float):
        if not self.player: return
        time.sleep(duracao)

    def ajustarBPM(self, acao: str):
        if acao == "AUMENTAR":
            self.bpm_atual += AUMENTO_BPM 
        
    def ajustarVolume(self, acao: str):
        if acao == "DOBRAR":
            self.volume_atual *= MULTIPLICA_VOLUME
            self.volume_atual = min(self.volume_atual, MAX_VOLUME) 
        
    def ajustarOitava(self, acao: str):
        if acao == "AUMENTAR":
            self.oitava_atual = min(self.oitava_atual + 1, MAX_OITAVA)
        elif acao == "DIMINUIR":
            self.oitava_atual = max(self.oitava_atual - 1, MIN_OITAVA)

    def trocarInstrumento(self, valor_instrumento: int):
        if not self.player: 
            return
        
        novo_instrumento = max(MIN_NOTA, min(MAX_NOTA, valor_instrumento))
        self.instrumento_atual_id = novo_instrumento
        self.player.set_instrument(self.instrumento_atual_id)
        
    def somarInstrumento(self, valor_soma: int):
        if not self.player: 
            return
        
        novo_id = self.instrumento_atual_id + valor_soma
        novo_id = novo_id % (MAX_INSTRUMENTO + 1)
        
        self.trocarInstrumento(novo_id)

    def tocarEventos(self, lista_eventos: list):

        if not self.player:
            print("Erro: Tocador MIDI não está ativo.")
            return

        for evento in lista_eventos:
            duracao = self.calcularBPM()
            tipo = evento.get('tipo')
            
            if tipo == "NOTA":
                self.tocarNota(evento.get('valor'), duracao)
                
            elif tipo == "PAUSA":
                self.pausar(duracao)
                
            elif tipo == "BPM":
                self.ajustarBPM(evento.get('acao'))
                
            elif tipo == "VOLUME":
                self.ajustarVolume(evento.get('acao'))
                
            elif tipo == "OITAVA":
                self.ajustarOitava(evento.get('acao'))
                
            elif tipo == "INSTRUMENTO":
                self.trocarInstrumento(evento.get('valor'))
                
            elif tipo == "INSTRUMENTO_SOMA":
                self.somarInstrumento(evento.get('valor'))


def main():

    root = tk.Tk()
    root.withdraw()

    

if __name__ == "__main__":
    main()