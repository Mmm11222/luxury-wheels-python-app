# Importar as librarias necessárias

import tkinter as tk
from tkinter import ttk, Scrollbar, VERTICAL, BOTH, RIGHT, Y, W, CENTER, END, messagebox, filedialog
import tkinter.font as tkFont
import customtkinter as ctk
import os
import datetime
import sqlite3
import pandas as pd # Import for Excel/CSV export


# Funções auxiliares de conversão de dados

def _convert_ativo_from_db(value):
    """Converte 1/0 (do SQLite) para 'Sim'/'Não' para exibição na GUI."""
    if value == 1:
        return 'Sim'
    elif value == 0:
        return 'Não'
    return '' 

def _convert_ativo_to_db(value_str):
    """Converte 'Sim'/'Não' (da GUI) para 1/0 (para SQLite)."""
    value_str = str(value_str).strip().lower()
    if value_str in ('sim', 'true', '1'):
        return 1
    elif value_str in ('não', 'nao', 'false', '0'):
        return 0
    messagebox.showerror("Erro de Validação", "O campo 'Ativo' deve ser 'Sim' ou 'Não'.")
    return None 


def _validate_date_input(date_str, field_name):
    """Valida se a string da data está no formato YYYY-MM-DD."""
    if not date_str:
        return None 
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' deve estar no formato YYYY-MM-DD.")
        return None


# Configuração custom tkinter

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


# Definição da janela principal customtkinter

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App Gestão Luxury Wheels")
        self.geometry("500x500")
        self.resizable(True, True)
        self.grid_columnconfigure(0, weight=1)


# Definição dos Widgets da janela principal:
     
        self.mylabel = ctk.CTkLabel(self, text="Escolha o Módulo", font=ctk.CTkFont(size=20, weight="bold"))
        self.mylabel.grid(row=0, column=0, pady=20)

        self.mylabel = ctk.CTkLabel(self, text="Escolha o Módulo", font=ctk.CTkFont(size=20, weight="bold"))
        self.mylabel.grid(row=0, column=0, pady=20)

        self.b1 = ctk.CTkButton(self, text="Dashboard", height=40)
        self.b1.grid(row=1, column=0, sticky="nsew", pady=10, padx=100)

        self.b2 = ctk.CTkButton(self, text="Reservas", height=40)
        self.b2.grid(row=2, column=0, sticky="nsew", pady=10, padx=100)

        self.b3 = ctk.CTkButton(self, text="Veículos", height=40)
        self.b3.grid(row=3, column=0, sticky="nsew", pady=10, padx=100)

        self.b4 = ctk.CTkButton(self, text="Clientes",command=self.janela_clientes, height=40)
        self.b4.grid(row=4, column=0, sticky="nsew", pady=10, padx=100)

        self.b5 = ctk.CTkButton(self, text="Formas de Pagamento", height=40)
        self.b5.grid(row=5, column=0, sticky="nsew", pady=10, padx=100)

        self.b6 = ctk.CTkButton(self, text="Utilizadores", height=40)
        self.b6.grid(row=6, column=0, sticky="nsew", pady=10, padx=100)

    
    def janela_clientes(self):
        self.clientes_window = JanelaClientes(self)
        self.clientes_window.grab_set() # Torna a janela modal
        self.iconify() # Minimiza a janela principal


# Definição da janela secundária Clientes

class JanelaClientes(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Módulo Clientes")
        self.geometry("1200x800")
        self.resizable(True, True)

# Permitir a expansão das colunas e linhas da janela  
   
        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(0, weight=1) # para o  tree_frame 
        self.grid_rowconfigure(1, weight=0) # para o search_frame
        self.grid_rowconfigure(2, weight=0) # para o data_frame
        self.grid_rowconfigure(3, weight=0) # para o  button_frame
        self.grid_rowconfigure(4, weight=0) # para o  export_frame

        self.protocol("WM_DELETE_WINDOW", self.sair)


# Configuração  do estilo da janela clientes

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Treeview",
                             background="#D3D3D3",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#D3D3D3",
                             font=("Arial", 10, "normal"))
        self.style.configure("Treeview.Heading",
                             font=('Arial', 10, 'bold'),
                             background='#f0f0f0',
                             foreground='black')
        self.style.map("Treeview", background=[("selected", "#347083")])


# Definição dos Widgets da janela clientes:

# Definição da Treeview -  Frame

        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        self.tree_scrollbar = Scrollbar(self.tree_frame, orient=VERTICAL)
        self.tree_scrollbar.pack(side=RIGHT, fill=Y)

        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scrollbar.set, show="headings")
        self.my_tree.pack(pady=10, fill=BOTH, expand=True)
        self.tree_scrollbar.config(command=self.my_tree.yview)

        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="#D9F3FB")

        
# Definição das colunas da Treeview para clientes

        self.my_tree["columns"] = ("ID_Cliente", "Nome", "Email", "Telefone", "Nif", "Morada", "Codigo_Postal", "Localidade", "Data_Nascimento", "Ativo", "Data Registo")
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.heading("#0", text="")
        self.my_tree.column("ID_Cliente", anchor=CENTER, width=80)
        self.my_tree.heading("ID_Cliente", text="ID")
        self.my_tree.column("Nome", anchor=CENTER, width=120)
        self.my_tree.heading("Nome", text="Nome")
        self.my_tree.column("Email", anchor=CENTER, width=120)
        self.my_tree.heading("Email", text="Email")
        self.my_tree.column("Telefone", anchor=CENTER, width=80)
        self.my_tree.heading("Telefone", text="Telefone")
        self.my_tree.column("Nif", anchor=CENTER, width=100)
        self.my_tree.heading("Nif", text="Nif")
        self.my_tree.column("Morada", anchor=CENTER, width=100)
        self.my_tree.heading("Morada", text="Morada")
        self.my_tree.column("Codigo_Postal", anchor=CENTER, width=80)
        self.my_tree.heading("Codigo_Postal", text="Cód. Postal")
        self.my_tree.column("Localidade", anchor=CENTER, width=120)
        self.my_tree.heading("Localidade", text="Localidade")
        self.my_tree.column("Data_Nascimento", anchor=CENTER, width=120)
        self.my_tree.heading("Data_Nascimento", text="Nascimento")
        self.my_tree.column("Ativo", anchor=CENTER, width=80)
        self.my_tree.heading("Ativo", text="Ativo")
        self.my_tree.column("Data Registo", anchor=CENTER, width=80)
        self.my_tree.heading("Data Registo", text="Data Registo")

# Definição do campo pesquisar 

        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(fill='x', expand='yes', padx=20, pady=10)
        
        for i in range(8): 
            self.search_frame.grid_columnconfigure(i, weight=1)

        self.search_label = ctk.CTkLabel(self.search_frame, text="Pesquisar por:", font=ctk.CTkFont(weight="bold"))
        self.search_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self.search_frame, textvariable=self.search_var, width=200)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.search_button = ctk.CTkButton(self.search_frame, text="Pesquisar", command=self.search_database, font=ctk.CTkFont(weight="bold"),
                                           fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        self.search_options_label = ctk.CTkLabel(self.search_frame, text="Opções de Pesquisa:", font=ctk.CTkFont(weight="bold"))
        self.search_options_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        self.search_option_var = ctk.StringVar(value="Nome") # Valor Valor padrão para clientes

        self.search_option_nome = ctk.CTkRadioButton(self.search_frame, text="Nome", variable=self.search_option_var, value="Nome")
        self.search_option_nome.grid(row=1, column=1, padx=10, pady=2, sticky=W)
        self.search_option_email = ctk.CTkRadioButton(self.search_frame, text="Email", variable=self.search_option_var, value="Email")
        self.search_option_email.grid(row=1, column=2, padx=10, pady=2, sticky=W)
        self.search_option_telefone = ctk.CTkRadioButton(self.search_frame, text="Telefone", variable=self.search_option_var, value="Telefone")
        self.search_option_telefone.grid(row=1, column=3, padx=10, pady=2, sticky=W)
        self.search_option_nif = ctk.CTkRadioButton(self.search_frame, text="Nif", variable=self.search_option_var, value="Nif")
        self.search_option_nif.grid(row=1, column=4, padx=10, pady=2, sticky=W)
        self.search_option_morada = ctk.CTkRadioButton(self.search_frame, text="Morada", variable=self.search_option_var, value="Morada")
        self.search_option_morada.grid(row=1, column=5, padx=10, pady=2, sticky=W)
        self.search_option_codigo_postal = ctk.CTkRadioButton(self.search_frame, text="Código Postal", variable=self.search_option_var, value="Codigo_Postal")
        self.search_option_codigo_postal.grid(row=1, column=6, padx=10, pady=2, sticky=W)
        self.search_option_localidade = ctk.CTkRadioButton(self.search_frame, text="Localidade", variable=self.search_option_var, value="Localidade")
        self.search_option_localidade.grid(row=1, column=7, padx=10, pady=2, sticky=W)
        self.search_option_data_nascimento = ctk.CTkRadioButton(self.search_frame, text="Data Nascimento", variable=self.search_option_var, value="Data_Nascimento")
        self.search_option_data_nascimento.grid(row=2, column=1, padx=10, pady=2, sticky=W)
        self.search_option_ativo = ctk.CTkRadioButton(self.search_frame, text="Ativo", variable=self.search_option_var, value="Ativo")
        self.search_option_ativo.grid(row=2, column=2, padx=10, pady=2, sticky=W)
        self.search_option_registo = ctk.CTkRadioButton(self.search_frame, text="Data Registo", variable=self.search_option_var, value="Data Registo")
        self.search_option_registo.grid(row=2, column=3, padx=10, pady=2, sticky=W)



# Definição do campo dados

        self.data_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.data_frame.pack(fill='x', expand='yes', padx=20, pady=10)
        
# Configuração da expansão de colunas para os campos de entrada 

        for i in range(11): 
            self.data_frame.grid_columnconfigure(i, weight=1)

        # Linha 0 de entradas
        self.label1=ctk.CTkLabel(self.data_frame, text="ID_Cliente")
        self.label1.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.entry1=ctk.CTkEntry(self.data_frame, width=80, state='readonly') 
        self.entry1.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.label2=ctk.CTkLabel(self.data_frame, text="Nome")
        self.label2.grid(row=0, column=2, padx=5, pady=5, sticky=W)
        self.entry2=ctk.CTkEntry(self.data_frame, width=80)
        self.entry2.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.label3=ctk.CTkLabel(self.data_frame, text="Email")
        self.label3.grid(row=0, column=4, padx=5, pady=5, sticky=W)
        self.entry3=ctk.CTkEntry(self.data_frame, width=80)
        self.entry3.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        self.label4=ctk.CTkLabel(self.data_frame, text="Telefone")
        self.label4.grid(row=0, column=6, padx=5, pady=5, sticky=W)
        self.entry4=ctk.CTkEntry(self.data_frame, width=80)
        self.entry4.grid(row=0, column=7, padx=5, pady=5, sticky="ew")

        self.label5=ctk.CTkLabel(self.data_frame, text="Nif")
        self.label5.grid(row=0, column=8, padx=5, pady=5, sticky=W)
        self.entry5=ctk.CTkEntry(self.data_frame, width=80)
        self.entry5.grid(row=0, column=9, padx=5, pady=5, sticky="ew")

        # Linha 1 de entradas
        self.label6=ctk.CTkLabel(self.data_frame, text="Morada")
        self.label6.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.entry6=ctk.CTkEntry(self.data_frame, width=80)
        self.entry6.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.label7=ctk.CTkLabel(self.data_frame, text="Código Postal")
        self.label7.grid(row=1, column=2, padx=5, pady=5, sticky=W)
        self.entry7=ctk.CTkEntry(self.data_frame, width=80)
        self.entry7.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        self.label8=ctk.CTkLabel(self.data_frame, text="Localidade")
        self.label8.grid(row=1, column=4, padx=5, pady=5, sticky=W)
        self.entry8=ctk.CTkEntry(self.data_frame, width=80)
        self.entry8.grid(row=1, column=5, padx=5, pady=5, sticky="ew")

        self.label9=ctk.CTkLabel(self.data_frame, text="Data Nascimento")
        self.label9.grid(row=1, column=6, padx=5, pady=5, sticky=W)
        self.entry9=ctk.CTkEntry(self.data_frame, width=80)
        self.entry9.grid(row=1, column=7, padx=5, pady=5, sticky="ew")

        self.label10=ctk.CTkLabel(self.data_frame, text="Ativo")
        self.label10.grid(row=1, column=8, padx=5, pady=5, sticky=W)
        self.entry10=ctk.CTkEntry(self.data_frame, width=80)
        self.entry10.grid(row=1, column=9, padx=5, pady=5, sticky="ew")

        # Linha 2 de entradas
        self.label11=ctk.CTkLabel(self.data_frame, text="Data Registo")
        self.label11.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.entry11=ctk.CTkEntry(self.data_frame, width=80)
        self.entry11.grid(row=2, column=1, padx=5, pady=5, sticky="ew")


# Definição do campo registos (botões)         

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill='x', expand='yes', padx=20, pady=10)
     
        for i in range(11):
            self.button_frame.grid_columnconfigure(i, weight=1)

        self.button1 = ctk.CTkButton(self.button_frame, text="Listar", command=self.listar, font=ctk.CTkFont(weight="bold"),
                                     fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.button2 = ctk.CTkButton(self.button_frame, text="Adicionar", command=self.adicionar,font=ctk.CTkFont(weight="bold"),
                                     fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button2.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.button3 = ctk.CTkButton(self.button_frame, text="Remover", command=self.remover, font=ctk.CTkFont(weight="bold"),
                                     fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button3.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

        self.button4 = ctk.CTkButton(self.button_frame, text="Editar", command=self.editar,font=ctk.CTkFont(weight="bold"),
                                     fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button4.grid(row=0, column=6, padx=10, pady=10, sticky="ew")

        self.button5 = ctk.CTkButton(self.button_frame, text="Menu", command=self.menu, font=ctk.CTkFont(weight="bold"),
                                     fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button5.grid(row=0, column=8, padx=10, pady=10, sticky="ew")

        self.button6 = ctk.CTkButton(self.button_frame, text="Sair", command=self.sair, font=ctk.CTkFont(weight="bold"),
                                     fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button6.grid(row=0, column=10, padx=10, pady=10, sticky="ew")

 # Configuração dos botões de exportação       

        self.export_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.export_frame.pack(fill='x', expand='yes', padx=20, pady=10)
        self.export_frame.grid_columnconfigure(0, weight=1)
        self.export_frame.grid_columnconfigure(1, weight=1)

        self.export_excel_button = ctk.CTkButton(self.export_frame, text="Exportar para Excel", command=self.export_to_excel,
                                                 fg_color="#488cc4", text_color="white", hover_color="#6fabdc")
        self.export_excel_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.export_csv_button = ctk.CTkButton(self.export_frame, text="Exportar para CSV", command=self.export_to_csv,
                                               fg_color="#488cc4", text_color="white", hover_color="#6fabdc")
        self.export_csv_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Iniciar e popular a Treeview

        self.my_tree.bind("<ButtonRelease-1>", self.aceder_registo)
        self.listar() 


# Definição da função listar que vai buscar as tabelas à base de dados e insere-a na treeview 

    def listar(self):
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)

        conn = None 
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM clientes")
            rows = cur.fetchall()

            for i, row in enumerate(rows):
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                
                display_row = list(row)
                display_row[9] = _convert_ativo_from_db(row[9]) 

                self.my_tree.insert("", END, values=display_row, tags=tags)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao aceder à base de dados: {e}")
        finally:
            if conn:
                conn.close()


# Definição da função search_database que permite a pesquisa por opção nas tabelas da base de dados 

    def search_database(self):
        search_term = self.search_var.get().strip() # Remover espaços em branco
        search_option = self.search_option_var.get()

        for item in self.my_tree.get_children():
            self.my_tree.delete(item)

        conn = None 
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            query = ""
            search_param = ()

            if not search_term:
                self.listar()
                return

# Opções mapping search para as colunas
            column_map = {
                "Nome": "nome",
                "Email": "email",
                "Telefone": "telefone",
                "Nif": "nif",
                "Morada": "morada",
                "Codigo_Postal": "codigo_postal",
                "Localidade": "localidade",
                "Data_Nascimento": "data_nascimento",
                "Ativo": "ativo",
                "Data Registo": "data_registo"
            }

            db_column = column_map.get(search_option) # mapping para pesquisa 'Disponivel' search
            if db_column:
               
                if db_column == "ativo":
                    search_value = _convert_ativo_to_db(search_term)
                    if search_value is None and search_term.lower() not in ('sim', 'não', 'nao', 'true', 'false', '0', '1'):
                        messagebox.showinfo("Pesquisa", "Para 'Ativo', use 'Sim' ou 'Não'.")
                        self.listar()
                        return
                    if search_value is not None:
                        query = f"SELECT * FROM clientes WHERE {db_column} = ?"
                        search_param = (search_value,)
                    else: 
                        self.listar()
                        return
                else:
                    query = f"SELECT * FROM clientes WHERE {db_column} LIKE ?"
                    search_param = (f"%{search_term}%",)
            else:
                messagebox.showinfo("Informação", "Selecione uma opção de pesquisa válida.")
                return

            cur.execute(query, search_param)
            rows = cur.fetchall()

            if not rows:
                messagebox.showinfo("Pesquisa", "Nenhum registo encontrado com os critérios fornecidos.")

            for i, row in enumerate(rows):
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                
               
                display_row = list(row)
                display_row[9] = _convert_ativo_from_db(row[9]) 
                
                self.my_tree.insert("", END, values=display_row, tags=tags)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao pesquisar: {e}")
           
        finally:
            if conn:
                conn.close()


# Definição da função aceder_registo que permite escolher um registo da tabela 

    def aceder_registo(self, event):
        try:
            selected_item = self.my_tree.focus()
            if not selected_item:
                return

            values = self.my_tree.item(selected_item, 'values')
            if not values:
                return

            self.limpar_campos() 
                                  
            self.current_client_id = values[0] # Armazena o ID do cliente selecionado numa variável de instância

            self.entry1.insert(0, self.current_client_id)   
            self.entry1.configure(state='readonly')
              
            self.entry2.insert(0, values[1])    # Nome
            self.entry3.insert(0, values[2])    # Email
            self.entry4.insert(0, values[3])    # Telefone
            self.entry5.insert(0, values[4])    # Nif
            self.entry6.insert(0, values[5])    # Morada
            self.entry7.insert(0, values[6])    # Código Postal
            self.entry8.insert(0, values[7])    # Localidade
            self.entry9.insert(0, values[8])    # Data Nascimento
            self.entry10.insert(0, values[9])   # Ativo 
            self.entry11.insert(0, values[10])  # Data Registo
           

            self.entry1.configure(state='readonly')
            
        except Exception as e:
            messagebox.showerror("Erro ao Aceder Registo", f"Ocorreu um erro ao aceder ao registo: {e}")


# Definição da função editar que permite alterar os registos à base de dados 

    def editar(self):
        
        if self.current_client_id is None:
            messagebox.showerror("Erro", "Selecione um registo para editar.")
            return
        
        nif = self.entry5.get().strip()
        confirmation = messagebox.askyesno("Confirmação", f"Tem a certeza que deseja editar o registo do Cliente com o Nif '{nif}'?")
        if not confirmation:
            return

        id_cliente = self.current_client_id
        nome = self.entry2.get().strip()
        email = self.entry3.get().strip()
        telefone = self.entry4.get().strip()
        morada = self.entry6.get().strip()
        codigo_postal = self.entry7.get().strip()
        localidade = self.entry8.get().strip()
        data_nascimento = _validate_date_input(self.entry9.get().strip(), "Data Nascimento")
        ativo = _convert_ativo_to_db(self.entry10.get().strip()) 
        data_registo = _validate_date_input(self.entry11.get().strip(), "Data Registo")

       
        if not all([nome, nif]):
            messagebox.showerror("Erro de Validação", "Nome e Nif são campos obrigatórios.")
            return
        
        if data_nascimento is None or ativo is None:
            return 

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            cur.execute("""
                UPDATE clientes
                SET
                    nome = ?,
                    email = ?,
                    telefone = ?,
                    nif = ?,
                    morada = ?,
                    codigo_postal = ?,
                    localidade = ?,
                    data_nascimento = ?,
                    ativo = ?,
                    data_registo=?
                WHERE id_cliente = ?
            """, (
                nome, email, telefone, nif, morada, codigo_postal, localidade, data_nascimento, ativo, data_registo,
                id_cliente 
            ))
            conn.commit()
            if cur.rowcount > 0:
                messagebox.showinfo("Sucesso", f"O registo do Cliente com o Nif '{nif}' foi editado com sucesso!")
                self.listar() 
                self.limpar_campos() 
            else:
                messagebox.showinfo("Informação", f"Nenhum registo foi atualizado. Verifique se o ID do Cliente existe.")

        except sqlite3.IntegrityError: 
            messagebox.showerror("Erro", f"Já existe um Cliente com o Nif '{nif}' na base de dados. O Nif deve ser único.")
            if conn:
                conn.rollback()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao editar o registo do Cliente: {e}")
            if conn:
                conn.rollback() 
        finally:
            if conn:
                conn.close()


  # Definição da função adicionar registos à base de dados  

    def adicionar(self):
        
        nome = self.entry2.get().strip()
        nif = self.entry5.get().strip()

        if not nome or not nif:
            messagebox.showerror("Erro", "Os campos 'Nome' e 'Nif' são obrigatórios.")
            return

        confirmation = messagebox.askyesno("Confirmação", f"Tem a certeza que deseja adicionar o Cliente com o Nif '{nif}'?")
        if not confirmation:
            return
        
        email = self.entry3.get().strip()
        telefone = self.entry4.get().strip()
        morada = self.entry6.get().strip()
        codigo_postal = self.entry7.get().strip()
        localidade = self.entry8.get().strip()
        data_nascimento = _validate_date_input(self.entry9.get().strip(), "Data Nascimento")
        ativo = _convert_ativo_to_db(self.entry10.get().strip()) 
        data_registo = _validate_date_input(self.entry11.get().strip(), "Data Registo")

        if data_nascimento is None or ativo is None:
            return 


        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO clientes (nome, email, telefone, nif, morada, codigo_postal, localidade, data_nascimento, ativo, data_registo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                nome, email, telefone, nif, morada, codigo_postal, localidade, data_nascimento, ativo, data_registo
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", f"O Cliente com o Nif '{nif}' foi adicionado com sucesso!")
            self.listar() 
            self.limpar_campos() 

        except sqlite3.IntegrityError: 
            messagebox.showerror("Erro", f"Já existe um Cliente com o Nif '{nif}' na base de dados. O Nif deve ser único.")
            if conn:
                conn.rollback()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar o Cliente: {e}")
            if conn:
                conn.rollback() 
        finally:
            if conn:
                conn.close()


  # Definição da função remover registos da base de dados

    def remover(self):
        selected_item = self.my_tree.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione um registo na tabela para remover.")
            return

        values = self.my_tree.item(selected_item, 'values')
        id_cliente_to_delete = values[0] 
        nif_to_delete = values[4] 

        confirmation = messagebox.askyesno("Confirmação", f"Tem a certeza que deseja remover o Cliente com o Nif '{nif_to_delete}' (ID: {id_cliente_to_delete})?")
        if not confirmation:
            return

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            cur.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente_to_delete,))
            if cur.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Sucesso", f"Cliente com o Nif '{nif_to_delete}' removido com sucesso!")
                self.listar() 
                self.limpar_campos() 
            else:
                messagebox.showinfo("Informação", f"Nenhum Cliente com o ID '{id_cliente_to_delete}' foi encontrado.")

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao remover o Cliente: {e}")
            if conn:
                conn.rollback() 
        finally:
            if conn:
                conn.close()


    def limpar_campos(self):
        self.entry1.configure(state='normal') 
        self.entry1.delete(0, tk.END)
        self.entry1.configure(state='readonly') 
        self.entry2.delete(0, tk.END)
        self.entry3.delete(0, tk.END)
        self.entry4.delete(0, tk.END)
        self.entry5.delete(0, tk.END)
        self.entry6.delete(0, tk.END)
        self.entry7.delete(0, tk.END)
        self.entry8.delete(0, tk.END)
        self.entry9.delete(0, tk.END)
        self.entry10.delete(0, tk.END)
        self.entry11.delete(0, tk.END)
        self.search_var.set("") 


 # Função para exportar dados para Excel 

    def export_to_excel(self):
        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            df = pd.read_sql_query("SELECT * FROM clientes", conn)
            
            
            df['ativo'] = df['ativo'].apply(lambda x: 'Sim' if x == 1 else 'Não')

            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Salvar Clientes como Excel"
            )
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Exportar Sucesso", f"Dados de Clientes exportados para '{file_path}' com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro de Exportação", f"Ocorreu um erro ao exportar para Excel: {e}")
        finally:
            if conn:
                conn.close()


  # Função para exportar dados para CSV 

    def export_to_csv(self):
        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            df = pd.read_sql_query("SELECT * FROM clientes", conn)

            # Convert 'ativo' column for better readability in CSV
            df['ativo'] = df['ativo'].apply(lambda x: 'Sim' if x == 1 else 'Não')
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Salvar Clientes como CSV"
            )
            if file_path:
                df.to_csv(file_path, index=False, encoding='utf-8-sig') # Use utf-8-sig for proper Excel opening with Portuguese chars
                messagebox.showinfo("Exportar Sucesso", f"Dados de Clientes exportados para '{file_path}' com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro de Exportação", f"Ocorreu um erro ao exportar para CSV: {e}")
        finally:
            if conn:
                conn.close()


# Função para retornar ao menu principal 

    def menu(self):
        confirmation = messagebox.askyesno("Confirmação", f"Deseja voltar ao Menu Principal?")
        if not confirmation:
            return
        
        self.destroy() 
        self.master.deiconify() 

  # Função para sair da aplicação

    def sair(self):
        if messagebox.askokcancel("Sair", "Tem a certeza que deseja sair?"):
            self.master.destroy() 


# Iniciar a aplicação

if __name__ == "__main__":
    
    app = MainWindow()
    app.mainloop()