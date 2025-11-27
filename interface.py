from classes import GeradorMusica
from tkinter import messagebox, scrolledtext, ttk
import tkinter as tk

VOLUME_DEFAULT = 60
BPM_DEFAULT = 60

OITAVA_DEFAULT = 0
MIN_OITAVA = -2
MAX_OITAVA = 9

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

COLOR_BG = "#1e1e1e"
COLOR_FG = "#d4d4d4"
COLOR_BG_SEC = "#252526"
COLOR_BTN_BG = "#3c3c3c"
COLOR_BTN_FG = "#ffffff"
COLOR_START = "#28a745"
COLOR_START_HOVER = "#218838"
COLOR_PAUSE = "#ffc107"
COLOR_INPUT_BG = "#3c3c3c"
COLOR_INPUT_FG = "#cccccc"
FONTE = "Comic Sans MS"

class AppGUI:
    def __init__(self, root, controlador: GeradorMusica):
        self.root = root
        self.controlador = controlador
        self.estado_player = "PARADO"
        self.setup_janela()
        self.criar_componentes()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_janela(self):
        self.root.title("TCP - Gerador de Música")
        self.root.geometry("750x650")
        self.root.configure(bg=COLOR_BG)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=COLOR_INPUT_BG, background=COLOR_BTN_BG, foreground=COLOR_FG, arrowcolor=COLOR_FG)
        style.map("TCombobox", fieldbackground=[('readonly', COLOR_INPUT_BG)])
        style.configure("Horizontal.TScale", background=COLOR_BG_SEC, troughcolor=COLOR_BTN_BG)

    def criar_componentes(self):

        # EDITOR DE TEXTO
        frame_texto = tk.Frame(self.root, bg=COLOR_BG)
        frame_texto.pack(fill="both", expand=True, padx=20, pady=(15, 5))
        tk.Label(frame_texto, text="Editor de Texto:", bg=COLOR_BG, fg=COLOR_FG).pack(anchor="w")
        self.area_texto = scrolledtext.ScrolledText(
            frame_texto, bg=COLOR_INPUT_BG, fg=COLOR_INPUT_FG, height=10,
            insertbackground="white", font=(FONTE, 11), borderwidth=0
        )
        self.area_texto.pack(fill="both", expand=True)

        # BARRA DE AÇÕES
        frame_acoes = tk.Frame(self.root, bg=COLOR_BG)
        frame_acoes.pack(fill="x", padx=20, pady=5)
        self.criar_botao(frame_acoes, "Abrir TXT", self.acao_abrir).pack(side="left", padx=5)
        self.criar_botao(frame_acoes, "Salvar TXT", self.acao_salvar_texto).pack(side="left", padx=5)
        self.criar_botao(frame_acoes, "Salvar MIDI", self.acao_salvar_midi).pack(side="left", padx=5)
        self.criar_botao(frame_acoes, "Ajuda", self.acao_ajuda).pack(side="right", padx=5)

        # PLAYER DE MUSICA
        frame_player = tk.Frame(self.root, bg=COLOR_BG_SEC, pady=15)
        frame_player.pack(fill="x", pady=10)
        frame_botoes_centro = tk.Frame(frame_player, bg=COLOR_BG_SEC)
        frame_botoes_centro.pack(anchor="center")

        self.btn_reiniciar = tk.Button(
            frame_botoes_centro, text="REINICIAR", command=self.acao_reiniciar,
            bg=COLOR_BTN_BG, fg=COLOR_FG, font=(FONTE, 10, "bold"),
            relief="flat", padx=15, pady=5
        )
        self.btn_reiniciar.pack(side="left", padx=10)

        self.btn_principal = tk.Button(
            frame_botoes_centro, text="INICIAR", command=self.acao_botao_principal,
            bg=COLOR_START, fg="white", font=(FONTE, 11, "bold"),
            activebackground=COLOR_START_HOVER, relief="flat", padx=25, pady=8
        )
        self.btn_principal.pack(side="left", padx=10)
        self.lbl_status = tk.Label(frame_player, text="Pronto", bg=COLOR_BG_SEC, fg=COLOR_FG)
        self.lbl_status.pack(pady=(5,0))

        # CONFIGURAÇÕES INICIAIS
        frame_config = tk.Frame(self.root, bg=COLOR_BG_SEC, padx=10, pady=10)
        frame_config.pack(side="bottom", fill="x")
        tk.Label(frame_config, text="Configurações Iniciais:", bg=COLOR_BG_SEC, fg=COLOR_FG).pack(anchor="w")
        grid_frame = tk.Frame(frame_config, bg=COLOR_BG_SEC)
        grid_frame.pack(fill="x", pady=5)

        tk.Label(grid_frame, text="Volume:", bg=COLOR_BG_SEC, fg=COLOR_FG).grid(row=0, column=0, padx=5)
        self.scale_vol = tk.Scale(grid_frame, from_=0, to=127, orient="horizontal", 
                                  bg=COLOR_BG_SEC, fg=COLOR_FG, highlightthickness=0, length=120)
        self.scale_vol.set(VOLUME_DEFAULT)
        self.scale_vol.grid(row=0, column=1, padx=5)

        self.spin_bpm = self.criar_input_config(grid_frame, "BPM:", 2, BPM_DEFAULT, 40, 300)
        self.spin_oit = self.criar_input_config(grid_frame, "Oitava:", 4, OITAVA_DEFAULT, MIN_OITAVA, MAX_OITAVA)

        tk.Label(grid_frame, text="Instrumento:", bg=COLOR_BG_SEC, fg=COLOR_FG).grid(row=0, column=6, padx=5)
        self.combo_inst = ttk.Combobox(grid_frame, values=list(INSTRUMENTOS.keys()), width=20, state="readonly")
        self.combo_inst.current(0)
        self.combo_inst.grid(row=0, column=7, padx=5)

    def criar_botao(self, parent, texto, comando):
        return tk.Button(parent, text=texto, command=comando, bg=COLOR_BTN_BG, fg=COLOR_BTN_FG, relief="flat", padx=8, pady=2)

    def criar_input_config(self, parent, label, col, valor_padrao, v_min, v_max):
        tk.Label(parent, text=label, bg=COLOR_BG_SEC, fg=COLOR_FG).grid(row=0, column=col, padx=5)
        spin = tk.Spinbox(parent, from_=v_min, to=v_max, width=5, bg=COLOR_INPUT_BG, fg=COLOR_FG, buttonbackground=COLOR_BTN_BG)
        spin.delete(0, "end")
        spin.insert(0, valor_padrao)
        spin.grid(row=0, column=col+1, padx=5)
        return spin

    def acao_botao_principal(self):
        if self.estado_player == "PARADO":
            self.iniciar_musica()
        elif self.estado_player == "TOCANDO":
            self.pausar_musica()
        elif self.estado_player == "PAUSADO":
            self.continuar_musica()

    def iniciar_musica(self):
        texto = self.area_texto.get("1.0", tk.END)
        config = self.get_configs()
        sucesso, msg = self.controlador.tocar_musica(texto, config, self.callback_fim_musica)
        if sucesso:
            self.estado_player = "TOCANDO"
            self.btn_principal.config(text="PAUSE", bg=COLOR_PAUSE, fg="black")
            self.lbl_status.config(text="Tocando...")
        else:
            messagebox.showwarning("Aviso", msg)

    def pausar_musica(self):
        self.controlador.pausar_musica()
        self.estado_player = "PAUSADO"
        self.btn_principal.config(text="CONTINUAR", bg=COLOR_START, fg="white")
        self.lbl_status.config(text="Pausado")

    def continuar_musica(self):
        self.controlador.despausar_musica()
        self.estado_player = "TOCANDO"
        self.btn_principal.config(text="PAUSE", bg=COLOR_PAUSE, fg="black")
        self.lbl_status.config(text="Tocando...")

    def acao_reiniciar(self):
        if self.estado_player == "PARADO": return
        self.controlador.parar_e_resetar_musica()
        self.resetar_interface()
        self.lbl_status.config(text="Reiniciado (Pronto)")

    def callback_fim_musica(self):
        self.root.after(0, self.resetar_interface)

    def resetar_interface(self):
        self.estado_player = "PARADO"
        self.btn_principal.config(text="INICIAR", bg=COLOR_START, fg="white")
        self.lbl_status.config(text="Parado")

    def acao_abrir(self):
        texto = self.controlador.carregar_arquivo_texto()
        if texto is not None:
            self.area_texto.delete("1.0", tk.END)
            self.area_texto.insert("1.0", texto)

    def acao_salvar_texto(self):
        txt = self.area_texto.get("1.0", tk.END)
        msg = self.controlador.salvar_arquivo_texto(txt)
        messagebox.showinfo("Salvar", msg)

    def acao_salvar_midi(self):
        texto = self.area_texto.get("1.0", tk.END)
        config = self.get_configs()
        sucesso, msg = self.controlador.gerar_midi(texto, config)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
        else:
            messagebox.showerror("Erro", msg)

    def acao_ajuda(self):
        janela_ajuda = tk.Toplevel(self.root)
        janela_ajuda.title("Ajuda - Mapa de Caracteres")
        janela_ajuda.geometry("400x400")
        janela_ajuda.configure(bg=COLOR_BG)
        txt_ajuda = scrolledtext.ScrolledText(janela_ajuda, bg=COLOR_INPUT_BG, fg=COLOR_FG, font=(FONTE, 10))
        txt_ajuda.pack(fill="both", expand=True, padx=10, pady=10) 

        msg = """ 
        MAPEAMENTO FASE 3:
        [A-G, a-g]: Notas (Lá à Sol)
        [Espaço]: Dobra Volume (Max 127)
        [!]: Troca Instrumento (Bandoneon)
        [Nova Linha]: Instrumento Aleatório
        [Digito]: Soma ao Instrumento Atual
        [O, I, U]: Repete nota anterior ou toca Telefone
        [?]: Nota Aleatória
        [BPM+]: Aumenta Velocidade em 80
        [OIT+]: Aumenta uma Oitava
        [OIT-]: Diminui uma Oitava
        [,]: Troca Instrumento (Agogo)
        [;]: Pausa
        """

        txt_ajuda.insert("1.0", msg)
        txt_ajuda.config(state="disabled")

    def get_configs(self):

        return {
            "bpm": self.spin_bpm.get(),
            "volume": self.scale_vol.get(),
            "oitava": self.spin_oit.get(),
            "instrumento": self.combo_inst.get()
        }
    
    def on_closing(self):
        self.controlador.fechar_programa()
        self.root.destroy()