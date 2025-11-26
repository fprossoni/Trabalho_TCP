from classes import GeradorMusica
from interface import AppGUI
import tkinter as tk

def main():
    root = tk.Tk()
    AppGUI(root, GeradorMusica())
    root.mainloop()

if __name__ == "__main__":
    main()