import tkinter as tk
from tkinter import filedialog

class AppFeriados:
    def __init__(self, root):
        self.root = root
        self.root.title("Conferindo Feriados")
        self.root.geometry("500x250") 
        
        self.caminho_pdf = "" 

        self.label = tk.Label(root, text="Selecione um arquivo PDF.")
        self.label.pack(pady=10)

        self.btn_selecionar = tk.Button(root, text="Selecionar PDF", command=self.selecionar_pdf)
        self.btn_selecionar.pack(pady=5)
        
        self.label_arquivo = tk.Label(root, text="Nenhum arquivo selecionado")
        self.label_arquivo.pack(pady=10)
        
        self.btn_verificar = tk.Button(root, text="Verificar PDF", command=self.iniciar_verificacao)
        self.btn_verificar.pack(pady=20)

    def selecionar_pdf(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o PDF",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        
        if caminho:
            self.caminho_pdf = caminho
            nome_arquivo = caminho.split('/')[-1] 
            self.label_arquivo.config(text=nome_arquivo)
            print(f"Arquivo selecionado: {self.caminho_pdf}")

    def iniciar_verificacao(self):
        if self.caminho_pdf:
            print(f"Iniciando verificação do arquivo: {self.caminho_pdf}")
        else:
            print("Nenhum PDF selecionado para verificar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppFeriados(root)
    root.mainloop()