import tkinter as tk
from tkinter import filedialog, Listbox
import requests
import fitz
import re
from collections import defaultdict
import datetime

class AppFeriados:
    def __init__(self, root):
        self.root = root
        self.root.title("Conferindo Feriados")
        self.root.geometry("500x400")
        
        self.caminho_pdf = ""

        self.label = tk.Label(root, text="Selecione um arquivo PDF.")
        self.label.pack(pady=10)

        self.btn_selecionar = tk.Button(root, text="Selecionar PDF", command=self.selecionar_pdf)
        self.btn_selecionar.pack(pady=5)
        
        self.label_arquivo = tk.Label(root, text="Nenhum arquivo selecionado")
        self.label_arquivo.pack(pady=5)
        
        self.btn_verificar = tk.Button(root, text="Verificar Feriados", command=self.iniciar_verificacao)
        self.btn_verificar.pack(pady=20)
        
        self.listbox_resultados = Listbox(root, width=50, height=10)
        self.listbox_resultados.pack(pady=10, padx=20)

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

    def extrair_datas_do_pdf(self):
        if not self.caminho_pdf:
            print("Caminho do PDF não definido.")
            return set()

        print(f"Lendo PDF: {self.caminho_pdf}")
        texto_completo = ""
        
        try:
            doc = fitz.open(self.caminho_pdf)
            for pagina in doc:
                texto_completo += pagina.get_text()
            doc.close()
            
        except Exception as e:
            self.listbox_resultados.delete(0, tk.END) 
            self.listbox_resultados.insert(tk.END, f"Erro ao ler PDF: {e}")
            return set()

        regex_data = r"\b(\d{4}-\d{2}-\d{2})\b"
        datas_encontradas = re.findall(regex_data, texto_completo)
        
        print(f"Datas encontradas no PDF: {set(datas_encontradas)}")
        return set(datas_encontradas)

    def verificar_feriados_api(self, datas_pdf):
        if not datas_pdf:
            return [] 

        datas_por_ano = defaultdict(list)
        for data_str in datas_pdf: 
            ano = data_str.split('-')[0] 
            datas_por_ano[ano].append(data_str)
            
        feriados_confirmados = []
        
        for ano, datas in datas_por_ano.items():
            
            log_msg = f"Verificando feriados para o ano {ano}..."
            print(log_msg) 
            
            url_api = f"https://date.nager.at/api/v3/PublicHolidays/{ano}/BR"
            
            try:
                response = requests.get(url_api) 
                if response.status_code == 200:
                    feriados_do_ano = response.json()
                    datas_api_set = {f["date"] for f in feriados_do_ano}
                    
                    for data_pdf_str in datas: 
                        if data_pdf_str in datas_api_set: 
                            feriados_confirmados.append(data_pdf_str)
                else:
                    print(f"Erro na API para o ano {ano}: {response.status_code}")
                    self.listbox_resultados.insert(tk.END, f"Erro na API (Ano {ano}): {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Erro de conexão com a API: {e}")
                self.listbox_resultados.insert(tk.END, f"Erro de conexão: {e}")
        
        print(f"Feriados confirmados (da API): {feriados_confirmados}")
        
        return feriados_confirmados

    def iniciar_verificacao(self):
        
        self.listbox_resultados.delete(0, tk.END) 
        
        if not self.caminho_pdf:
            self.listbox_resultados.insert(tk.END, "Erro: Selecione um PDF primeiro.")
            return
        
        self.listbox_resultados.insert(tk.END, "Lendo PDF e extraindo datas...")
        self.root.update_idletasks() 
        
        datas_do_pdf = self.extrair_datas_do_pdf()
        
        if not datas_do_pdf:
            self.listbox_resultados.delete(0, tk.END) 
            self.listbox_resultados.insert(tk.END, "Nenhuma data (aaaa-mm-dd) encontrada no PDF.")
            return

        self.listbox_resultados.delete(0, tk.END) 
        self.listbox_resultados.insert(tk.END, f"Verificando {len(datas_do_pdf)} datas na API...")
        self.root.update_idletasks()
        
        feriados_encontrados = self.verificar_feriados_api(datas_do_pdf)
        
        self.listbox_resultados.delete(0, tk.END)
        
        if not feriados_encontrados:
            self.listbox_resultados.insert(tk.END, "Nenhum feriado encontrado.")
        else:
            self.listbox_resultados.insert(tk.END, "Feriados Encontrados:")
            for data in sorted(feriados_encontrados): 
                self.listbox_resultados.insert(tk.END, f"  {data}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppFeriados(root)
    root.mainloop()