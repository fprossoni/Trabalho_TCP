import pygame
import pygame.midi
from tkinter import filedialog
import random
import time
import threading

try:
    from midiutil import MIDIFile
    HAS_MIDIUTIL = True
except ImportError:
    HAS_MIDIUTIL = False

VOLUME_DEFAULT = 60
BPM_DEFAULT = 60

OITAVA_OFFSET = 12
AUMENTO_BPM = 80

MULTIPLICA_VOLUME = 2
MAX_NOTA = MAX_INSTRUMENTO = MAX_VOLUME = 127
MAX_OITAVA = 9

MIN_NOTA = MIN_INSTRUMENTO = OITAVA_DEFAULT = MIN_VOLUME = INSTRUMENTO_DEFAULT = 0
MIN_OITAVA = -2

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

MAPA_NOTAS_MIDI = {
    "NOTA_DO": 60, 
    "NOTA_RE": 62, 
    "NOTA_MI": 64, 
    "NOTA_FA": 65,
    "NOTA_SOL": 67, 
    "NOTA_LA": 69, 
    "NOTA_SI": 71, 
    "NOTA_SI_BEMOL": 70
}



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

            try:
                with open(caminho, 'r', encoding='utf-8') as arquivo:
                    self.texto = arquivo.read()
                return self.texto
            
            except Exception as e:
                print(f"Erro ao ler arquivo: {e}")
                return None
            
        return None

    def salvarArquivo(self):
        return self.salvarComo()

    def salvarComo(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt")]
        )
        if caminho:
            self.caminho_arquivo = caminho
            try:
                with open(caminho, 'w', encoding='utf-8') as arquivo:
                    arquivo.write(self.texto)
                return True, f"Salvo em: {self.caminho_arquivo}"
            except Exception as e:
                return False, str(e)
        return False, "Salvamento cancelado."



class TransformaMusica:
    def __init__(self):
        self.lista_eventos = []

    def processarTexto(self, texto_entrada):

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

                mapa = {'A':'LA', 
                        'B':'SI', 
                        'C':'DO', 
                        'D':'RE', 
                        'E':'MI', 
                        'F':'FA', 
                        'G':'SOL', 
                        'H':'SI_BEMOL'}
                
                nota = f"NOTA_{mapa.get(caractere_atual.upper(), 'LA')}"

                self.lista_eventos.append({"tipo": "NOTA", "valor": nota})
                ultimo_evento_foi_nota = True
                ultima_nota_tocada = nota

            elif caractere_atual == " ":

                self.lista_eventos.append({"tipo": "VOLUME", "acao": "DOBRAR"})
            
            elif caractere_atual == "?":

                notas = ["NOTA_LA", "NOTA_SI", "NOTA_DO", "NOTA_RE", "NOTA_MI", "NOTA_FA", "NOTA_SOL"]

                self.lista_eventos.append({"tipo": "NOTA", "valor": random.choice(notas)})
                ultimo_evento_foi_nota = True
                ultima_nota_tocada = self.lista_eventos[-1]["valor"]

            elif caractere_atual == "\n":

                inst_random = random.choice(list(INSTRUMENTOS.values()))
                self.lista_eventos.append({"tipo": "INSTRUMENTO", "valor": inst_random})
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
                self.lista_eventos.append({"tipo": "INSTRUMENTO_SOMA", "valor": int(caractere_atual)})
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
    def __init__(self):

        self.player = None
        self.inicializado = False

        try:
            pygame.init()
            pygame.midi.init()
            port = pygame.midi.get_default_output_id()
            if port == -1: port = 0
            self.player = pygame.midi.Output(port)
            self.inicializado = True

        except Exception as e:
            print(f"[ERRO MIDI] {e}")

        self.config_inicial = {
            'bpm': BPM_DEFAULT, 
            'volume': VOLUME_DEFAULT, 
            'oitava': OITAVA_DEFAULT, 
            'instrumento': INSTRUMENTO_DEFAULT
        }

        self.bpm_atual = BPM_DEFAULT
        self.volume_atual = VOLUME_DEFAULT
        self.oitava_atual = OITAVA_DEFAULT
        self.instrumento_atual_id = INSTRUMENTO_DEFAULT
        
        self.tocando = False 
        self.evento_pausa = threading.Event()
        self.evento_pausa.set() 

    def atualizarConfiguracao(self, bpm, volume, oitava, instrumento_id):

        self.config_inicial = {
            'bpm': bpm, 
            'volume': volume, 
            'oitava': oitava, 
            'instrumento': instrumento_id
        }

        self.bpm_atual = bpm
        self.volume_atual = volume
        self.oitava_atual = oitava
        self.trocarInstrumento(instrumento_id)

    def restaurarEstadoInicial(self):
        config_inicial = self.config_inicial
        self.bpm_atual = config_inicial['bpm']
        self.volume_atual = config_inicial['volume']
        self.oitava_atual = config_inicial['oitava']
        self.trocarInstrumento(config_inicial['instrumento'])

    def fechar(self):

        if self.player:
            self.player.close()
            pygame.midi.quit()
            pygame.quit()

    def pararExecucaoCompleta(self):
        self.tocando = False
        self.evento_pausa.set() 

    def pausarMusica(self):
        self.evento_pausa.clear()

    def despausarMusica(self):
        self.evento_pausa.set()

    def calcularBPM(self):
        return 60.0 / max(1, self.bpm_atual)

    def tocarNota(self, nome_nota, duracao):
        if not self.player: return
        base = MAPA_NOTAS_MIDI.get(nome_nota)
        if base:
            nota = base + (OITAVA_OFFSET * self.oitava_atual)
            nota = max(MIN_NOTA, min(MAX_NOTA, nota))
            self.player.note_on(nota, self.volume_atual)
            time.sleep(duracao)
            self.player.note_off(nota, self.volume_atual)

    def ajustarBPM(self, acao):
        if acao == "AUMENTAR": 
            self.bpm_atual += AUMENTO_BPM

    def ajustarVolume(self, acao):
        if acao == "DOBRAR": 
            self.volume_atual = min(self.volume_atual * MULTIPLICA_VOLUME, MAX_VOLUME)

    def ajustarOitava(self, acao):

        if acao == "AUMENTAR": 
            self.oitava_atual = min(self.oitava_atual + 1, MAX_OITAVA)

        elif acao == "DIMINUIR": 
            self.oitava_atual = max(self.oitava_atual - 1, MIN_OITAVA)

    def trocarInstrumento(self, valor):
        if self.player:
            self.instrumento_atual_id = max(MIN_INSTRUMENTO, min(MAX_INSTRUMENTO, valor))
            self.player.set_instrument(self.instrumento_atual_id)

    def somarInstrumento(self, valor):
        novo = (self.instrumento_atual_id + valor) % (MAX_INSTRUMENTO + 1)
        self.trocarInstrumento(novo)
        
    def pausarTempo(self, duracao):
        time.sleep(duracao)

    def tocarEventos(self, lista_eventos, callback_fim=None):
        self.tocando = True
        self.evento_pausa.set()

        if not self.inicializado or not self.player:
            if callback_fim: callback_fim()
            return

        for evento in lista_eventos:
            if not self.tocando: 
                break
            self.evento_pausa.wait()

            duracao = self.calcularBPM()
            tipo = evento.get('tipo')
            
            if tipo == "NOTA": self.tocarNota(evento['valor'], duracao)
            elif tipo == "PAUSA": self.pausarTempo(duracao)
            elif tipo == "BPM": self.ajustarBPM(evento['acao'])
            elif tipo == "VOLUME": self.ajustarVolume(evento['acao'])
            elif tipo == "OITAVA": self.ajustarOitava(evento['acao'])
            elif tipo == "INSTRUMENTO": self.trocarInstrumento(evento['valor'])
            elif tipo == "INSTRUMENTO_SOMA": self.somarInstrumento(evento['valor'])

        self.tocando = False
        if callback_fim:
            callback_fim()



class GeradorMusica:
    def __init__(self):
        self.leitor = LeitorTexto()
        self.transformador = TransformaMusica()
        self.tocador = TocadorNotas()
        self.thread = None

    def carregar_arquivo_texto(self):
        return self.leitor.abrirArquivo()

    def salvar_arquivo_texto(self, texto_atual):
        self.leitor.receberTextoEscrito(texto_atual)
        return self.leitor.salvarArquivo() 

    def tocar_musica(self, texto, config, callback_fim):
        if self.thread and self.thread.is_alive():
            self.tocador.pararExecucaoCompleta()
            self.thread.join(timeout=1.0)

        self.leitor.receberTextoEscrito(texto)
        eventos = self.transformador.processarTexto(self.leitor.texto)
        if not eventos: 
            return False, "Texto vazio."

        inst_id = INSTRUMENTOS.get(config['instrumento'], 0)
        self.tocador.atualizarConfiguracao(
            int(config['bpm']), int(config['volume']), 
            int(config['oitava']), inst_id
        )

        self.thread = threading.Thread(target=self.tocador.tocarEventos, args=(eventos, callback_fim))
        self.thread.daemon = True
        self.thread.start()
        return True, "Tocando..."

    def pausar_musica(self):
        self.tocador.pausarMusica()

    def despausar_musica(self):
        self.tocador.despausarMusica()

    def parar_musica(self):
        self.tocador.pararExecucaoCompleta()

    def parar_e_resetar_musica(self):
        self.tocador.pararExecucaoCompleta()
        self.tocador.restaurarEstadoInicial()
    
    def fechar_programa(self):
        if self.tocador:
            self.tocador.fechar()

    def gerar_midi(self, texto, config):
        if not HAS_MIDIUTIL:
            return False, "MIDIUTIL não encontrado"

        caminho = filedialog.asksaveasfilename(
            defaultextension=".mid", 
            filetypes=[("Arquivo MIDI", "*.mid")]
        )
        if not caminho:
            return False, "Salvamento cancelado."

        try:
            comandos = self.transformador.processarTexto(texto)

            bpm_atual = int(config['bpm'])
            inst_atual = INSTRUMENTOS.get(config['instrumento'], 0)
            vol_atual = int(config['volume'])
            oitava_atual = int(config['oitava'])
            
            midi = MIDIFile(1)
            track = 0
            time_cursor = 0
            
            midi.addTrackName(track, time_cursor, "Gerado pelo Gerador de música")
            midi.addTempo(track, time_cursor, bpm_atual)
            midi.addProgramChange(track, 0, time_cursor, inst_atual)
            
            channel = 0
            duration = 1

            for cmd in comandos:
                tipo = cmd['tipo']
                
                if tipo == "NOTA":

                    nota_base = MAPA_NOTAS_MIDI.get(cmd.get('valor'), 60)
                    note_num = nota_base + (OITAVA_OFFSET * oitava_atual)
                    note_num = max(MIN_NOTA, min(MAX_NOTA, note_num))

                    midi.addNote(track, channel, note_num, time_cursor, duration, vol_atual)
                    time_cursor += duration

                elif tipo == "PAUSA":
                    time_cursor += duration

                elif tipo == "BPM":
                    if cmd.get('acao') == "AUMENTAR": 
                        bpm_atual += AUMENTO_BPM
                    midi.addTempo(track, time_cursor, bpm_atual)

                elif tipo == "VOLUME":
                    if cmd.get('acao') == "DOBRAR":
                        vol_atual = min(MAX_VOLUME, vol_atual * MULTIPLICA_VOLUME)
                
                elif tipo == "OITAVA":
                    if cmd.get('acao') == "AUMENTAR": 
                        oitava_atual = min(oitava_atual + 1, MAX_OITAVA)
                    elif cmd.get('acao') == "DIMINUIR": 
                        oitava_atual = max(oitava_atual - 1, MIN_OITAVA)

                elif tipo == "INSTRUMENTO":
                    inst_atual = cmd.get('valor')
                    midi.addProgramChange(track, 0, time_cursor, inst_atual)
                
                elif tipo == "INSTRUMENTO_SOMA":
                    inst_atual = (inst_atual + cmd.get('valor')) % (MAX_INSTRUMENTO + 1)
                    midi.addProgramChange(track, 0, time_cursor, inst_atual)

            with open(caminho, "wb") as output_file:
                midi.writeFile(output_file)
            
            return True, f"Arquivo MIDI exportado com sucesso em: {caminho}"

        except Exception as e:
            return False, f"Erro ao salvar MIDI: {str(e)}"