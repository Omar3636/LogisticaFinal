from src.app.gui.ventana_principal import Aplicacion
import tkinter as tk

def main():
    raiz = tk.Tk()
    app = Aplicacion(raiz)
    raiz.mainloop()

if __name__ == '__main__':
    main()