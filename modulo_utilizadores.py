# Importar as librarias

import tkinter as tk
from tkinter import ttk, Scrollbar, VERTICAL, BOTH, RIGHT, Y, W, CENTER, END, messagebox, filedialog
import tkinter.font as tkFont
import customtkinter as ctk
import os
import re
import datetime
import sqlite3
import pandas as pd 


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
        return None # Allow empty date for non-mandatory fields, or handle as required
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' deve estar no formato YYYY-MM-DD.")
        return None
    
    
def _validate_email_input(email_str, field_name):
    """Valida se a string do email tem um formato básico válido."""
    if not email_str:
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' não pode estar vazio.")
        return None
    # Regex simples para verificar o formato do email
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email_str):
        return email_str
    else:
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' deve ser um email válido.")
        return None

def _validate_int_input(value_str, field_name):
    """Valida se a string pode ser convertida para um inteiro."""
    if not value_str:
        return None # Permitir vazio se não for obrigatório, ou exigir conforme o contexto
    try:
        return int(value_str)
    except ValueError:
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' deve ser um número inteiro válido.")
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

        self.b4 = ctk.CTkButton(self, text="Clientes", height=40)
        self.b4.grid(row=4, column=0, sticky="nsew", pady=10, padx=100)

        self.b5 = ctk.CTkButton(self, text="Formas de Pagamento", height=40)
        self.b5.grid(row=5, column=0, sticky="nsew", pady=10, padx=100)

        self.b6 = ctk.CTkButton(self, text="Utilizadores",command=self.janela_utilizadores, height=40)
        self.b6.grid(row=6, column=0, sticky="nsew", pady=10, padx=100)

    
    def janela_utilizadores(self):
        self.utilizadores_window = JanelaUtilizadores(self)
        self.utilizadores_window.grab_set() 
        self.iconify() 


# Definição da janela secundária utlizadores

class JanelaUtilizadores(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Módulo Utilizadores")
        self.geometry("1000x800")
        self.resizable(True, True)

# Permitir a expansão das colunas e linhas da janela  

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Treeview frame
        self.grid_rowconfigure(1, weight=0) # Search frame
        self.grid_rowconfigure(2, weight=0) # Data entry frame
        self.grid_rowconfigure(3, weight=0) # Action buttons frame
        self.grid_rowconfigure(4, weight=0) # Export buttons frame

        self.protocol("WM_DELETE_WINDOW", self.sair)


# Configuração  do estilo da janela utilizadores

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


# Definição dos Widgets da janela utilizadores:

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


# Definição das colunas da Treeview para utilizadores

        self.my_tree["columns"] = ("id_utilizador", "nome", "email", "password", "telefone","data_criacao","ativo")
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.heading("#0", text="" )
        self.my_tree.column("id_utilizador", anchor=CENTER, width=100)
        self.my_tree.heading("id_utilizador", text="ID_Utilizador")
        self.my_tree.column("nome", anchor=CENTER, width=100)
        self.my_tree.heading("nome", text="Nome")
        self.my_tree.column("email", anchor=CENTER, width=100)
        self.my_tree.heading("email", text="Email")
        self.my_tree.column("password", anchor=CENTER, width=120)
        self.my_tree.heading("password",text="Password")
        self.my_tree.column("telefone", anchor=CENTER, width=120)
        self.my_tree.heading("telefone", text="Telefone")
        self.my_tree.column("data_criacao", anchor=CENTER, width=120)
        self.my_tree.heading("data_criacao", text="Data Criação")
        self.my_tree.column("ativo", anchor=CENTER, width=120)
        self.my_tree.heading("ativo", text="Ativo")


# Definição do campo pesquisar 

        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(fill='x', expand='yes', padx=20, pady=10)
       
        for i in range(8): # Adjusted for the number of columns in radio buttons
            self.search_frame.grid_columnconfigure(i, weight=1)

        self.search_label = ctk.CTkLabel(self.search_frame, text="Pesquisar por:", font=ctk.CTkFont(weight="bold"))
        self.search_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.search_var = ctk.StringVar()

        self.search_entry = ctk.CTkEntry(self.search_frame, textvariable=self.search_var, width=200)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.search_button = ctk.CTkButton(self.search_frame, text="Pesquisar", command=self.search_database,
                                           fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        self.search_options_label = ctk.CTkLabel(self.search_frame, text="Opções de Pesquisa:", font=ctk.CTkFont(weight="bold"))
        self.search_options_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        self.search_option_var = ctk.StringVar(value="id_utilizador")

        self.search_option_id_utilizador = ctk.CTkRadioButton(self.search_frame, text="Id_Utilizador", variable=self.search_option_var, value="id_utilizador") # Using CustomTkinter Radiobutton
        self.search_option_id_utilizador.grid(row=1, column=1, padx=10, pady=2, sticky="ew")
        self.search_option_nome = ctk.CTkRadioButton(self.search_frame, text="Nome", variable=self.search_option_var, value="nome") # Using CustomTkinter Radiobutton
        self.search_option_nome.grid(row=1, column=2, padx=10, pady=2, sticky="ew")
        self.search_option_email = ctk.CTkRadioButton(self.search_frame, text="Email", variable=self.search_option_var, value="email") # Using CustomTkinter Radiobutton
        self.search_option_email.grid(row=1, column=3, padx=10, pady=2, sticky="ew")
        self.search_option_password = ctk.CTkRadioButton(self.search_frame, text="Password", variable=self.search_option_var, value="password") # Using CustomTkinter Radiobutton
        self.search_option_password.grid(row=1, column=4, padx=10, pady=2, sticky="ew")
        self.search_option_telefone = ctk.CTkRadioButton(self.search_frame, text="Telefone", variable=self.search_option_var, value="telefone") # Using CustomTkinter Radiobutton
        self.search_option_telefone.grid(row=1, column=5, padx=10, pady=2, sticky="ew")
        self.search_option_data_criacao = ctk.CTkRadioButton(self.search_frame, text="Data Criação", variable=self.search_option_var, value="data_criacao") # Using CustomTkinter Radiobutton
        self.search_option_data_criacao.grid(row=1, column=6, padx=10, pady=2, sticky="ew")
        self.search_option_ativo = ctk.CTkRadioButton(self.search_frame, text="Ativo", variable=self.search_option_var, value="ativo") # Using CustomTkinter Radiobutton
        self.search_option_ativo.grid(row=2, column=1, padx=10, pady=2, sticky="ew")


# Definição do campo dados

        self.data_frame=ctk.CTkFrame(self, corner_radius=10) 
        self.data_frame.pack(fill='x', expand='yes', padx=20)

        # Linha 0 de entradas
        self.label1=ctk.CTkLabel(self.data_frame, text="Id_Utilizador") 
        self.label1.grid(row=0, column=0, padx=10, pady=10)
        self.entry1=ctk.CTkEntry(self.data_frame, state='readonly') 
        self.entry1.grid(row=0, column=1, padx=10, pady=10)

        self.label2=ctk.CTkLabel(self.data_frame, text="Nome") 
        self.label2.grid(row=0, column=2, padx=10, pady=10)
        self.entry2=ctk.CTkEntry(self.data_frame) 
        self.entry2.grid(row=0, column=3, padx=10, pady=10)

        self.label3=ctk.CTkLabel(self.data_frame, text="Email") 
        self.label3.grid(row=0, column=4, padx=10, pady=10)
        self.entry3=ctk.CTkEntry(self.data_frame) 
        self.entry3.grid(row=0, column=5, padx=10, pady=10)

        self.label4=ctk.CTkLabel(self.data_frame, text="Password") 
        self.label4.grid(row=0, column=6, padx=10, pady=10)
        self.entry4=ctk.CTkEntry(self.data_frame, show="*") 
        self.entry4.grid(row=0, column=7, padx=10, pady=10)

        # Linha 1 de entradas
        self.label5=ctk.CTkLabel(self.data_frame, text="Telefone") 
        self.label5.grid(row=1, column=0, padx=10, pady=10)
        self.entry5=ctk.CTkEntry(self.data_frame) 
        self.entry5.grid(row=1, column=1, padx=10, pady=10)

        self.label6=ctk.CTkLabel(self.data_frame, text="Data Criação") 
        self.label6.grid(row=1, column=2, padx=10, pady=10)
        self.entry6=ctk.CTkEntry(self.data_frame, state='readonly') 
        self.entry6.grid(row=1, column=3, padx=10, pady=10)

        self.label7=ctk.CTkLabel(self.data_frame, text="Ativo") 
        self.label7.grid(row=1, column=4, padx=10, pady=10)
        self.ativo_options = ["Sim", "Não"]
        self.entry7_var = ctk.StringVar(value=self.ativo_options[0])
        self.entry7=ctk.CTkComboBox(self.data_frame, values=self.ativo_options, variable=self.entry7_var) 
        self.entry7.grid(row=1, column=5, padx=10, pady=10)



# Definição do campo registos (botões) 

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill='x', expand='yes', padx=20, pady=10)
       
        for i in range(11):
            self.button_frame.grid_columnconfigure(i, weight=1)

        self.button1 = ctk.CTkButton(self.button_frame, text="Listar", command=self.listar,font=ctk.CTkFont(weight="bold"),
                                     fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.button2 = ctk.CTkButton(self.button_frame, text="Adicionar", command=self.adicionar,font=ctk.CTkFont(weight="bold"),
                                     fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button2.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.button3 = ctk.CTkButton(self.button_frame, text="Remover", command=self.remover,font=ctk.CTkFont(weight="bold"),
                                     fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button3.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

        self.button4 = ctk.CTkButton(self.button_frame, text="Editar", command=self.editar,font=ctk.CTkFont(weight="bold"),
                                     fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button4.grid(row=0, column=6, padx=10, pady=10, sticky="ew")

        self.button5 = ctk.CTkButton(self.button_frame, text="Menu", command=self.menu,font=ctk.CTkFont(weight="bold"),
                                     fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button5.grid(row=0, column=8, padx=10, pady=10, sticky="ew")

        self.button6 = ctk.CTkButton(self.button_frame, text="Sair", command=self.sair,font=ctk.CTkFont(weight="bold"),
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
            cur.execute("SELECT * FROM utilizador")
            rows = cur.fetchall()

            for i, row in enumerate(rows):
               
                display_row = list(row)
                display_row[6] = "Sim" if row[6] == 1 else "Não"
                if i % 2 == 0:
                    self.my_tree.insert("", END, values=display_row, tags=('evenrow',))
                else:
                    self.my_tree.insert("", END, values=display_row, tags=('oddrow',))

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao aceder à base de dados: {e}")

        finally:
            if conn:
                conn.close()


# Definição da função search_database que permite a pesquisa por opção nas tabelas da base de dados

    def search_database(self):
        search_term = self.search_var.get()
        search_option = self.search_option_var.get()

        for item in self.my_tree.get_children():
            self.my_tree.delete(item)

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()

            query = ""
            search_param = ()

            if search_option == "id_utilizador":
                query = "SELECT * FROM utilizador WHERE id_utilizador LIKE ?"
                search_param = (f"%{search_term}%",)
            elif search_option == "nome":
                query = "SELECT * FROM utilizador WHERE nome LIKE ?"
                search_param = (f"%{search_term}%",)
            elif search_option == "email":
                query = "SELECT * FROM utilizador WHERE email LIKE ?"
                search_param = (f"%{search_term}%",)
            elif search_option == "password":
                query = "SELECT * FROM utilizador WHERE password LIKE ?"
                search_param = (f"%{search_term}%",)
            elif search_option == "telefone":
                query = "SELECT * FROM utilizador WHERE telefone LIKE ?"
                search_param = (f"%{search_term}%",)
            elif search_option == "data_criacao":
                query = "SELECT * FROM utilizador WHERE data_criacao LIKE ?"
                search_param = (f"%{search_term}%",)
            elif search_option == "ativo":
                # Convert "Sim"/"Não" to 1/0 for database search
                search_value = 1 if search_term.lower() == "sim" else (0 if search_term.lower() == "não" else None)
                if search_value is not None:
                    query = "SELECT * FROM utilizador WHERE ativo = ?"
                    search_param = (search_value,)
                else:
                    messagebox.showinfo("Informação", "Para 'Ativo', pesquise por 'Sim' ou 'Não'.")
                    return
            else:
                messagebox.showinfo("Informação", "Selecione uma opção de pesquisa válida.")
                return

            cur.execute(query, search_param)
            rows = cur.fetchall()

            for i, row in enumerate(rows):
                
                display_row = list(row)
                display_row[6] = "Sim" if row[6] == 1 else "Não"
                if i % 2 == 0:
                    self.my_tree.insert("", END, values=display_row, tags=('evenrow',))
                else:
                    self.my_tree.insert("", END, values=display_row, tags=('oddrow',))

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao pesquisar: {e}")
        finally:
            if conn:
                conn.close()


# Definição da função aceder_registo que permite escolher um registo da tabela 

    def aceder_registo(self, event):
        try:
            selected = self.my_tree.focus()
            if not selected:
                return

            values = self.my_tree.item(selected, 'values')
            if not values:
                return

            
            self.entry1.configure(state='normal')
            self.entry6.configure(state='normal') 

            self.entry1.delete(0, tk.END)
            self.entry2.delete(0, tk.END)
            self.entry3.delete(0, tk.END)
            self.entry4.delete(0, tk.END)
            self.entry5.delete(0, tk.END)
            self.entry6.delete(0, tk.END)
           

            self.entry1.insert(0, values[0])  # Id_utilizador
            self.entry2.insert(0, values[1])  # nome
            self.entry3.insert(0, values[2])  # email
            self.entry4.insert(0, values[3])  # password
            self.entry5.insert(0, values[4])  # telefone
            self.entry6.insert(0, values[5])  # data_criacao
            self.entry7_var.set(values[6])    # ativo (será "Sim" or "Não")

            self.entry1.configure(state='readonly') 
            self.entry6.configure(state='readonly') 

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao aceder ao registo: {e}")


# Definição da função editar que permite alterar os registos à base de dados 

    def editar(self):
        id_utilizador = self.entry1.get()
        if not id_utilizador:
            messagebox.showerror("Erro", "Selecione um utilizador para editar.")
            return

        confirmation = messagebox.askyesno("Confirmação", f"Tem a certeza que deseja editar o registo do utilizador com o id '{id_utilizador}'?")
        if not confirmation:
            return

        # Get and validate inputs
        nome = self.entry2.get()
        email = _validate_email_input(self.entry3.get(), "Email")
        password = self.entry4.get()
        telefone = _validate_int_input(self.entry5.get(), "Telefone")
        data_criacao = self.entry6.get()
        ativo_str = self.entry7_var.get()
        ativo = 1 if ativo_str == "Sim" else 0

        if not (nome and email and password and telefone is not None and data_criacao is not None):
            messagebox.showerror("Erro de Validação", "Por favor, preencha todos os campos obrigatórios e verifique os formatos.")
            return

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            cur.execute("""
                UPDATE utilizador
                SET
                    nome = ?,
                    email = ?,
                    password = ?,
                    telefone = ?,
                    data_criacao = ?,
                    ativo = ?
                WHERE id_utilizador = ?
            """, (
                nome,
                email,
                password,
                telefone,
                data_criacao,
                ativo,
                id_utilizador,
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", f"O registo de utilizador com o id '{id_utilizador}' foi editado com sucesso!")
            self.listar()

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao editar o registo de utilizador: {e}")
            if conn:
                conn.rollback()

        finally:
            if conn:
                conn.close()


# Definição da função adicionar registos à base de dados 

    def adicionar(self):
       
        nome = self.entry2.get()
        email = _validate_email_input(self.entry3.get(), "Email")
        password = self.entry4.get()
        telefone = _validate_int_input(self.entry5.get(), "Telefone")
        ativo_str = self.entry7_var.get()
        ativo = 1 if ativo_str == "Sim" else 0

        if not (nome and email and password and telefone is not None):
            messagebox.showerror("Erro de Validação", "Por favor, preencha Nome, Email, Password e Telefone.")
            return

        confirmation = messagebox.askyesno("Confirmação", f"Tem a certeza que deseja adicionar o utilizador com o nome '{nome}'?")
        if not confirmation:
            return

        # Obter a data e hora atual
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO utilizador (nome, email, password, telefone, data_criacao, ativo)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                nome,
                email,
                password,
                telefone,
                data_atual,
                ativo,
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", f"O utilizador com o nome '{nome}' foi adicionado com sucesso!")
            self.listar()
            
            self.entry1.configure(state='normal')
            self.entry6.configure(state='normal')
            self.entry1.delete(0, tk.END)
            self.entry2.delete(0, tk.END)
            self.entry3.delete(0, tk.END)
            self.entry4.delete(0, tk.END)
            self.entry5.delete(0, tk.END)
            self.entry6.delete(0, tk.END)
            self.entry7_var.set(self.ativo_options[0]) 
            self.entry1.configure(state='readonly')
            self.entry6.configure(state='readonly')

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: utilizador.email" in str(e):
                messagebox.showerror("Erro", "O email fornecido já está registado. Por favor, use um email diferente.")
            else:
                messagebox.showerror("Erro", f"Ocorreu um erro de integridade ao adicionar o utilizador: {e}")
            if conn:
                conn.rollback()
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar o utilizador: {e}")
            if conn:
                conn.rollback()

        finally:
            if conn:
                conn.close()


# Definição da função remover registos da base de dados

    def remover(self):
        id_to_delete = self.entry1.get()
        if not id_to_delete:
            messagebox.showerror("Erro", "Por favor, selecione o utilizador a remover na tabela.")
            return

        confirmation = messagebox.askyesno("Confirmação", f"Tem a certeza que deseja remover o utilizador com o id '{id_to_delete}'?")
        if not confirmation:
            return

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            cur.execute("DELETE FROM utilizador WHERE id_utilizador = ?", (id_to_delete,))
            if cur.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Sucesso", f"Utilizador com o id '{id_to_delete}' removido com sucesso!")
                self.listar()
                # Clear entries after successful removal
                self.entry1.configure(state='normal')
                self.entry6.configure(state='normal')
                self.entry1.delete(0, tk.END)
                self.entry2.delete(0, tk.END)
                self.entry3.delete(0, tk.END)
                self.entry4.delete(0, tk.END)
                self.entry5.delete(0, tk.END)
                self.entry6.delete(0, tk.END)
                self.entry7_var.set(self.ativo_options[0]) # Reset ComboBox
                self.entry1.configure(state='readonly')
                self.entry6.configure(state='readonly')

            else:
                messagebox.showinfo("Informação", f"Nenhum utilizador com o id '{id_to_delete}' foi encontrado.")

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao remover o utilizador: {e}")
            if conn:
                conn.rollback()

        finally:
            if conn:
                conn.close()


 # Função para exportar dados para Excel 

    def export_to_excel(self):
        """Exports payment method data to an Excel file."""
        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            df = pd.read_sql_query("SELECT id_forma_pagamento AS 'ID Forma Pagamento', tipo AS 'Tipo', detalhes AS 'Detalhes' FROM formas_pagamento ORDER BY id_forma_pagamento ASC", conn)

            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Guardar Formas de Pagamento como Excel"
            )
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Exportar para Excel", "Dados de formas de pagamento exportados para Excel com sucesso!")

        except sqlite3.Error as e:
            messagebox.showerror("Erro de Exportação", f"Ocorreu um erro ao exportar para Excel: {e}")
        except Exception as e:
            messagebox.showerror("Erro de Exportação", f"Ocorreu um erro inesperado ao exportar: {e}")
        finally:
            if conn:
                conn.close()


 # Função para exportar dados para CSV 

    def export_to_csv(self):
        """Exports payment method data to a CSV file."""
        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            df = pd.read_sql_query("SELECT id_forma_pagamento AS 'ID Forma Pagamento', tipo AS 'Tipo', detalhes AS 'Detalhes' FROM formas_pagamento ORDER BY id_forma_pagamento ASC", conn)

            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Guardar Formas de Pagamento como CSV"
            )
            if file_path:
                df.to_csv(file_path, index=False, encoding='utf-8-sig') 
                messagebox.showinfo("Exportar para CSV", "Dados de formas de pagamento exportados para CSV com sucesso!")

        except sqlite3.Error as e:
            messagebox.showerror("Erro de Exportação", f"Ocorreu um erro ao exportar para CSV: {e}")
        except Exception as e:
            messagebox.showerror("Erro de Exportação", f"Ocorreu um erro inesperado ao exportar: {e}")
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
        confirmation = messagebox.askyesno("Confirmação", f"Deseja terminar a aplicação?")
        if not confirmation:
            return

        self.destroy()
        self.grab_release()
        self.master.destroy()


# Iniciar a aplicação

if __name__ == "__main__":
    
    app = MainWindow()
    app.mainloop()
