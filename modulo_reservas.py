# Importar as librarias

import tkinter as tk
from tkinter import ttk, Scrollbar, VERTICAL, BOTH, RIGHT, Y, W, CENTER, END, messagebox, filedialog
import tkinter.font as tkFont
import customtkinter as ctk
import os
import datetime
import sqlite3
import pandas as pd # Import for Excel/CSV export


# Funções auxiliares de conversão de dados

def _validate_int_input(value_str, field_name):
    """Valida se a string pode ser convertida para um inteiro."""
    cleaned_value_str = str(value_str).strip() # Garante que é string e remove espaços
    if not cleaned_value_str:
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' não pode estar vazio.")
        return None
    try:
        return int(cleaned_value_str)
    except ValueError:
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' deve ser um número inteiro válido. Valor atual: '{cleaned_value_str}'")
        return None


def _validate_float_input(value_str, field_name):
    """Valida se a string pode ser convertida para um número decimal (float)."""
    cleaned_value_str = str(value_str).strip() # Garante que é string e remove espaços
    if not cleaned_value_str:
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' não pode estar vazio.")
        return None
    try:
        return float(cleaned_value_str)
    except ValueError:
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' deve ser um número decimal válido (ex: 123.45). Valor atual: '{cleaned_value_str}'")
        return None


def _validate_date_input(date_str, field_name):
    """Valida se a string da data está no formato YYYY-MM-DD."""
    cleaned_date_str = str(date_str).strip() # Garante que é string e remove espaços
    if not cleaned_date_str: # Se a string da data estiver vazia, retorna None
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' não pode estar vazio.")
        return None
    try:
        # Tenta converter, removendo qualquer componente de hora se presente
        datetime.datetime.strptime(cleaned_date_str.split(' ')[0], '%Y-%m-%d')
        return cleaned_date_str.split(' ')[0] # Retorna apenas a parte da data
    except ValueError:
        print(f"DEBUG: Falha na validação de data para '{field_name}'. String recebida: '{cleaned_date_str}'") # Depuração
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' deve estar no formato YYYY-MM-DD. Valor atual: '{cleaned_date_str}'")
        return None


def _validate_datetime_input(datetime_str, field_name):
    """Valida se a string da data/hora está no formato YYYY-MM-DD HH:MM:SS."""
    cleaned_datetime_str = str(datetime_str).strip() # Garante que é string e remove espaços
    if not cleaned_datetime_str:
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' não pode estar vazio.")
        return None
    try:
        # Tenta converter, removendo milissegundos se presentes (SQLite pode adicionar .000000)
        datetime.datetime.strptime(cleaned_datetime_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
        return cleaned_datetime_str.split('.')[0] # Retorna sem milissegundos
    except ValueError:
        print(f"DEBUG: Falha na validação de data/hora para '{field_name}'. String recebida: '{cleaned_datetime_str}'") # Depuração
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' deve estar no formato YYYY-MM-DD HH:MM:SS. Valor atual: '{cleaned_datetime_str}'")
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

        self.b1 = ctk.CTkButton(self, text="Dashboard", height=40)
        self.b1.grid(row=1, column=0, sticky="nsew", pady=10, padx=100)

        self.b2 = ctk.CTkButton(self, text="Reservas",command=self.janela_reservas, height=40)
        self.b2.grid(row=2, column=0, sticky="nsew", pady=10, padx=100)

        self.b3 = ctk.CTkButton(self, text="Veículos", height=40)
        self.b3.grid(row=3, column=0, sticky="nsew", pady=10, padx=100)

        self.b4 = ctk.CTkButton(self, text="Clientes", height=40)
        self.b4.grid(row=4, column=0, sticky="nsew", pady=10, padx=100)

        self.b5 = ctk.CTkButton(self, text="Formas de Pagamento", height=40)
        self.b5.grid(row=5, column=0, sticky="nsew", pady=10, padx=100)

        self.b6 = ctk.CTkButton(self, text="Utilizadores", height=40)
        self.b6.grid(row=6, column=0, sticky="nsew", pady=10, padx=100)


    def janela_reservas(self):
        self.janela_reservas_window = JanelaReservas(self)
        self.janela_reservas_window.grab_set()
        self.iconify()


# Definição da janela secundária reservas

class JanelaReservas(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent # Armazena a referência à janela principal
        self.title("Módulo Reservas")
        self.geometry("1400x900")
        self.resizable(True, True)

# Permitir a expansão das colunas e linhas da janela 

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Treeview frame
        self.grid_rowconfigure(1, weight=0) # Search frame
        self.grid_rowconfigure(2, weight=0) # Data entry frame
        self.grid_rowconfigure(3, weight=0) # Action buttons frame
        self.grid_rowconfigure(4, weight=0) # Export buttons frame

        self.protocol("WM_DELETE_WINDOW", self.sair)


# Configuração  do estilo da janela reservas

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

# Definição da Treeview -  Frame

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

        self.my_tree["columns"] = ("ID_Reserva", "ID_Cliente", "ID_Veiculo",
                                   "Data_Inicio", "Data_Fim", "Preco_Total", "ID_Forma_Pagamento", "Data_Reserva")

        self.my_tree.column("#0", width=0, stretch=tk.NO) # Hidden default column

        self.my_tree.column("ID_Reserva", anchor=CENTER, width=80)
        self.my_tree.heading("ID_Reserva", text="ID Reserva")

        self.my_tree.column("ID_Cliente", anchor=CENTER, width=80)
        self.my_tree.heading("ID_Cliente", text="ID Cliente")

        self.my_tree.column("ID_Veiculo", anchor=CENTER, width=80)
        self.my_tree.heading("ID_Veiculo", text="ID Veículo")

        self.my_tree.column("Data_Inicio", anchor=CENTER, width=120)
        self.my_tree.heading("Data_Inicio", text="Data Início")

        self.my_tree.column("Data_Fim", anchor=CENTER, width=120)
        self.my_tree.heading("Data_Fim", text="Data Fim")

        self.my_tree.column("Preco_Total", anchor=CENTER, width=100)
        self.my_tree.heading("Preco_Total", text="Preço Total")

        self.my_tree.column("ID_Forma_Pagamento", anchor=CENTER, width=100)
        self.my_tree.heading("ID_Forma_Pagamento", text="ID Pgto.")

        self.my_tree.column("Data_Reserva", anchor=CENTER, width=120)
        self.my_tree.heading("Data_Reserva", text="Data Reserva")


# Definição do campo pesquisar 

        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(fill='x', expand='yes', padx=20, pady=10)
        
        for i in range(len(self.my_tree["columns"]) + 2): 
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

    
        self.search_option_var = ctk.StringVar(value="ID_Reserva") # Default value

        self.search_option_reserva_id = ctk.CTkRadioButton(self.search_frame, text="ID Reserva", variable=self.search_option_var, value="ID_Reserva")
        self.search_option_reserva_id.grid(row=1, column=1, padx=10, pady=2, sticky=W)
        self.search_option_cliente_id = ctk.CTkRadioButton(self.search_frame, text="ID Cliente", variable=self.search_option_var, value="ID_Cliente")
        self.search_option_cliente_id.grid(row=1, column=2, padx=10, pady=2, sticky=W)
        self.search_option_veiculo_id = ctk.CTkRadioButton(self.search_frame, text="ID Veículo", variable=self.search_option_var, value="ID_Veiculo")
        self.search_option_veiculo_id.grid(row=1, column=3, padx=10, pady=2, sticky=W)
        self.search_option_data_inicio = ctk.CTkRadioButton(self.search_frame, text="Data Início", variable=self.search_option_var, value="Data_Inicio")
        self.search_option_data_inicio.grid(row=1, column=4, padx=10, pady=2, sticky=W)
        self.search_option_data_fim = ctk.CTkRadioButton(self.search_frame, text="Data Fim", variable=self.search_option_var, value="Data_Fim")
        self.search_option_data_fim.grid(row=1, column=5, padx=10, pady=2, sticky=W)
        self.search_option_preco_total = ctk.CTkRadioButton(self.search_frame, text="Preço Total", variable=self.search_option_var, value="Preco_Total")
        self.search_option_preco_total.grid(row=1, column=6, padx=10, pady=2, sticky=W)
        self.search_option_forma_pagamento_id = ctk.CTkRadioButton(self.search_frame, text="ID Forma Pgto", variable=self.search_option_var, value="ID_Forma_Pagamento")
        self.search_option_forma_pagamento_id.grid(row=1, column=7, padx=10, pady=2, sticky=W)
        self.search_option_data_reserva = ctk.CTkRadioButton(self.search_frame, text="Data Reserva", variable=self.search_option_var, value="Data_Reserva")
        self.search_option_data_reserva.grid(row=2, column=1, padx=10, pady=2, sticky=W)


# Definição do campo dados

        self.data_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.data_frame.pack(fill='x', expand='yes', padx=20, pady=10)

        self.data_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        # Linha 0 de entradas
        self.label1_r=ctk.CTkLabel(self.data_frame, text="ID_Reserva")
        self.label1_r.grid(row=0, column=0, padx=2, pady=2, sticky="ew")
        self.entry1_r=ctk.CTkEntry(self.data_frame, width=80, state='readonly')
        self.entry1_r.grid(row=0, column=1, padx=2, pady=2, sticky="ew")

        self.label2_r=ctk.CTkLabel(self.data_frame, text="ID_Cliente")
        self.label2_r.grid(row=0, column=2, padx=2, pady=2, sticky="ew")
        self.entry2_r=ctk.CTkEntry(self.data_frame, width=80)
        self.entry2_r.grid(row=0, column=3, padx=2, pady=2, sticky="ew")

        self.label3_r=ctk.CTkLabel(self.data_frame, text="ID_Veiculo")
        self.label3_r.grid(row=0, column=4, padx=2, pady=2, sticky="ew")
        self.entry3_r=ctk.CTkEntry(self.data_frame, width=80)
        self.entry3_r.grid(row=0, column=5, padx=2, pady=2, sticky="ew")

        self.label4_r=ctk.CTkLabel(self.data_frame, text="Data Início")
        self.label4_r.grid(row=0, column=6, padx=2, pady=2, sticky="ew")
        self.entry4_r=ctk.CTkEntry(self.data_frame, width=80)
        self.entry4_r.grid(row=0, column=7, padx=2, pady=2, sticky="ew")

        # Linha 1 de entradas
        self.label5_r=ctk.CTkLabel(self.data_frame, text="Data Fim")
        self.label5_r.grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        self.entry5_r=ctk.CTkEntry(self.data_frame, width=80, state='readonly') # Make it readonly here
        self.entry5_r.grid(row=1, column=1, padx=2, pady=2, sticky="ew")

        self.label6_r=ctk.CTkLabel(self.data_frame, text="Preço Total")
        self.label6_r.grid(row=1, column=2, padx=2, pady=2, sticky="ew")
        self.entry6_r=ctk.CTkEntry(self.data_frame, width=80)
        self.entry6_r.grid(row=1, column=3, padx=2, pady=2, sticky="ew")

        self.label7_r=ctk.CTkLabel(self.data_frame, text="ID_Forma_Pagamento")
        self.label7_r.grid(row=1, column=4, padx=2, pady=2, sticky="ew")
        self.entry7_r=ctk.CTkEntry(self.data_frame, width=80)
        self.entry7_r.grid(row=1, column=5, padx=2, pady=2, sticky="ew")

        self.label8_r=ctk.CTkLabel(self.data_frame, text="Data Reserva (Auto)")
        self.label8_r.grid(row=1, column=6, padx=2, pady=2, sticky="ew")
        self.entry8_r=ctk.CTkEntry(self.data_frame, width=80, state='readonly') # Should be readonly as it's auto-generated
        self.entry8_r.grid(row=1, column=7, padx=2, pady=2, sticky="ew")


# Definição do campo registos (botões)  

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill='x', expand='yes', padx=20, pady=10)
        
        self.button_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Corrigido: Botão "Listar" duplicado. Alterado para "Adicionar"
        self.button1_r = ctk.CTkButton(self.button_frame, text="Adicionar", command=self.adicionar, font=ctk.CTkFont(weight="bold"),
                                       fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button1_r.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.button2_r = ctk.CTkButton(self.button_frame, text="Listar", command=self.listar, font=ctk.CTkFont(weight="bold"),
                                       fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button2_r.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.button3_r = ctk.CTkButton(self.button_frame, text="Remover", command=self.remover,font=ctk.CTkFont(weight="bold"),
                                       fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button3_r.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.button4_r = ctk.CTkButton(self.button_frame, text="Editar", command=self.editar,font=ctk.CTkFont(weight="bold"),
                                       fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button4_r.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        self.button5_r = ctk.CTkButton(self.button_frame, text="Menu", command=self.menu,font=ctk.CTkFont(weight="bold"),
                                       fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button5_r.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

        self.button6_r = ctk.CTkButton(self.button_frame, text="Sair", command=self.sair,font=ctk.CTkFont(weight="bold"),
                                       fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button6_r.grid(row=0, column=5, padx=10, pady=10, sticky="ew")

# Configuração dos botões de exportação  

        self.export_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.export_frame.pack(fill='x', expand='yes', padx=20, pady=10)
        self.export_frame.grid_columnconfigure((0, 1), weight=1)

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
            
            cur.execute("""
                SELECT
                    id_reserva, id_cliente, id_veiculo,
                    data_inicio, data_fim, preco_total, id_forma_pagamento, data_reserva
                FROM reservas
                ORDER BY id_reserva ASC
            """)
            rows = cur.fetchall()

            for i, row in enumerate(rows):
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                row_list = list(row)
                
                # Formata data_inicio para YYYY-MM-DD
                if row_list[3]: 
                    try:
                        # Tenta converter para datetime e depois formatar
                        dt_obj = datetime.datetime.strptime(str(row_list[3]).split(' ')[0], '%Y-%m-%d')
                        row_list[3] = dt_obj.strftime('%Y-%m-%d')
                    except ValueError:
                        # Se falhar, tenta um formato mais flexível (ex: com hora e milissegundos)
                        try:
                            dt_obj = datetime.datetime.strptime(str(row_list[3]).split('.')[0], '%Y-%m-%d %H:%M:%S')
                            row_list[3] = dt_obj.strftime('%Y-%m-%d')
                        except ValueError:
                            pass # Manter o valor original se todas as conversões falharem (indica dado muito inconsistente)

                # Formata data_fim para YYYY-MM-DD
                if row_list[4]: 
                    try:
                        dt_obj = datetime.datetime.strptime(str(row_list[4]).split(' ')[0], '%Y-%m-%d')
                        row_list[4] = dt_obj.strftime('%Y-%m-%d')
                    except ValueError:
                        try:
                            dt_obj = datetime.datetime.strptime(str(row_list[4]).split('.')[0], '%Y-%m-%d %H:%M:%S')
                            row_list[4] = dt_obj.strftime('%Y-%m-%d')
                        except ValueError:
                            pass

                # Formata data_reserva para YYYY-MM-DD HH:MM:SS
                if row_list[7]: 
                    try:
                        dt_obj = datetime.datetime.strptime(str(row_list[7]).split('.')[0], '%Y-%m-%d %H:%M:%S')
                        row_list[7] = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        pass # Manter o valor original se a conversão falhar

                self.my_tree.insert("", END, values=tuple(row_list), tags=tags)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao aceder à base de dados de reservas: {e}")
        finally:
            if conn:
                conn.close()

# Definição da função search_database que permite a pesquisa por opção nas tabelas da base de dados 

    def search_database(self):
 
        search_term = self.search_var.get().strip()
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
                self.listar() # If search term is empty, list all
                return

            column_map = {
                "ID_Reserva": "id_reserva",
                "ID_Cliente": "id_cliente",
                "ID_Veiculo": "id_veiculo",
                "Data_Inicio": "data_inicio",
                "Data_Fim": "data_fim",
                "Preco_Total": "preco_total",
                "ID_Forma_Pagamento": "id_forma_pagamento",
                "Data_Reserva": "data_reserva"
            }

            db_column = column_map.get(search_option)
            if db_column:
                base_query = """
                    SELECT
                        id_reserva, id_cliente, id_veiculo,
                        data_inicio, data_fim, preco_total, id_forma_pagamento, data_reserva
                    FROM reservas
                """

                if search_option in ("ID_Reserva", "ID_Cliente", "ID_Veiculo", "ID_Forma_Pagamento"):
                    try:
                        search_value = int(search_term)
                        query = f"{base_query} WHERE {db_column} = ?"
                        search_param = (search_value,)
                    except ValueError:
                        messagebox.showerror("Erro de Pesquisa", "Por favor, insira um número inteiro válido para esta pesquisa (ID).")
                        self.listar()
                        return
                elif search_option == "Preco_Total":
                    try:
                        search_value = float(search_term)
                        query = f"{base_query} WHERE {db_column} = ?"
                        search_param = (search_value,)
                    except ValueError:
                        messagebox.showerror("Erro de Pesquisa", "Por favor, insira um número decimal válido para esta pesquisa (Preço Total).")
                        self.listar()
                        return
                elif search_option in ("Data_Inicio", "Data_Fim", "Data_Reserva"):
                    query = f"{base_query} WHERE {db_column} LIKE ?"
                    search_param = (f"%{search_term}%",)
                else: 
                    messagebox.showinfo("Informação", "Selecione uma opção de pesquisa válida.")
                    return
            else:
                messagebox.showinfo("Informação", "Selecione uma opção de pesquisa válida.")
                return

            cur.execute(query, search_param)
            rows = cur.fetchall()

            if not rows:
                messagebox.showinfo("Pesquisa", "Nenhum registo de reserva encontrado com os critérios fornecidos.")

            for i, row in enumerate(rows):
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                row_list = list(row)
                # Formata data_inicio para YYYY-MM-DD
                if row_list[3]: 
                    try:
                        dt_obj = datetime.datetime.strptime(str(row_list[3]).split(' ')[0], '%Y-%m-%d')
                        row_list[3] = dt_obj.strftime('%Y-%m-%d')
                    except ValueError:
                        try:
                            dt_obj = datetime.datetime.strptime(str(row_list[3]).split('.')[0], '%Y-%m-%d %H:%M:%S')
                            row_list[3] = dt_obj.strftime('%Y-%m-%d')
                        except ValueError:
                            pass

                # Formata data_fim para YYYY-MM-DD
                if row_list[4]: 
                    try:
                        dt_obj = datetime.datetime.strptime(str(row_list[4]).split(' ')[0], '%Y-%m-%d')
                        row_list[4] = dt_obj.strftime('%Y-%m-%d')
                    except ValueError:
                        try:
                            dt_obj = datetime.datetime.strptime(str(row_list[4]).split('.')[0], '%Y-%m-%d %H:%M:%S')
                            row_list[4] = dt_obj.strftime('%Y-%m-%d')
                        except ValueError:
                            pass

                # Formata data_reserva para YYYY-MM-DD HH:MM:SS
                if row_list[7]: 
                    try:
                        dt_obj = datetime.datetime.strptime(str(row_list[7]).split('.')[0], '%Y-%m-%d %H:%M:%S')
                        row_list[7] = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        pass
                self.my_tree.insert("", END, values=tuple(row_list), tags=tags)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao pesquisar reservas: {e}")
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

            # Habilita temporariamente os campos somente leitura para inserir valores
            self.entry1_r.configure(state='normal') 
            self.entry5_r.configure(state='normal') 
            self.entry8_r.configure(state='normal') 

            # Popula os campos com os valores da Treeview, garantindo o formato correto
            self.entry1_r.insert(0, values[0]) # ID_Reserva

            # Data Início
            if values[3]:
                try:
                    dt_obj = datetime.datetime.strptime(str(values[3]).split(' ')[0], '%Y-%m-%d')
                    self.entry4_r.insert(0, dt_obj.strftime('%Y-%m-%d'))
                except ValueError:
                    # Tenta um formato mais flexível se o primeiro falhar
                    try:
                        dt_obj = datetime.datetime.strptime(str(values[3]).split('.')[0], '%Y-%m-%d %H:%M:%S')
                        self.entry4_r.insert(0, dt_obj.strftime('%Y-%m-%d'))
                    except ValueError:
                        self.entry4_r.insert(0, values[3]) # Insere o valor bruto se tudo falhar
                        messagebox.showwarning("Aviso de Formato", f"A Data Início '{values[3]}' pode estar num formato inesperado. Por favor, verifique.")
            else:
                self.entry4_r.insert(0, "") # Campo vazio se não houver valor

            # Data Fim (readonly)
            if values[4]:
                try:
                    dt_obj = datetime.datetime.strptime(str(values[4]).split(' ')[0], '%Y-%m-%d')
                    self.entry5_r.insert(0, dt_obj.strftime('%Y-%m-%d'))
                except ValueError:
                    try:
                        dt_obj = datetime.datetime.strptime(str(values[4]).split('.')[0], '%Y-%m-%d %H:%M:%S')
                        self.entry5_r.insert(0, dt_obj.strftime('%Y-%m-%d'))
                    except ValueError:
                        self.entry5_r.insert(0, values[4])
                        messagebox.showwarning("Aviso de Formato", f"A Data Fim '{values[4]}' pode estar num formato inesperado. Por favor, verifique.")
            else:
                self.entry5_r.insert(0, "")

            self.entry2_r.insert(0, values[1]) # ID_Cliente
            self.entry3_r.insert(0, values[2]) # ID_Veiculo
            self.entry6_r.insert(0, values[5]) # Preco Total
            self.entry7_r.insert(0, values[6]) # ID_Forma_Pagamento
            
            # Data Reserva (readonly)
            if values[7]:
                try:
                    dt_obj = datetime.datetime.strptime(str(values[7]).split('.')[0], '%Y-%m-%d %H:%M:%S')
                    self.entry8_r.insert(0, dt_obj.strftime('%Y-%m-%d %H:%M:%S'))
                except ValueError:
                    self.entry8_r.insert(0, values[7])
                    messagebox.showwarning("Aviso de Formato", f"A Data Reserva '{values[7]}' pode estar num formato inesperado. Por favor, verifique.")
            else:
                self.entry8_r.insert(0, "")


            # Define o estado final dos campos somente leitura
            self.entry1_r.configure(state='readonly')
            self.entry5_r.configure(state='readonly') 
            self.entry8_r.configure(state='readonly')

        except Exception as e:
            messagebox.showerror("Erro ao Aceder Registo", f"Ocorreu um erro ao aceder ao registo de reserva: {e}")


    # Definição da função auxiliar para verificar a disponibilidade do veículo
    def _is_vehicle_available(self, id_veiculo, data_inicio, data_fim, exclude_reserva_id=None):
        """
        Verifica se um veículo está disponível para o período de tempo especificado.
        Exclui uma reserva específica (útil para edições).
        """
        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()

            query = """
                SELECT COUNT(*) FROM reservas
                WHERE id_veiculo = ?
                AND (
                    (data_inicio <= ? AND data_fim >= ?) OR -- Nova reserva começa durante uma existente
                    (data_inicio <= ? AND data_fim >= ?) OR -- Nova reserva termina durante uma existente
                    (data_inicio >= ? AND data_fim <= ?)    -- Nova reserva engloba uma existente
                )
            """
            params = [id_veiculo, data_fim, data_inicio, data_inicio, data_fim, data_inicio, data_fim]

            if exclude_reserva_id is not None:
                query += " AND id_reserva != ?"
                params.append(exclude_reserva_id)
            
            cur.execute(query, tuple(params))
            count = cur.fetchone()[0]
            return count == 0 # Retorna True se não houver reservas sobrepostas

        except sqlite3.Error as e:
            messagebox.showerror("Erro de Base de Dados", f"Erro ao verificar disponibilidade do veículo: {e}")
            return False # Assume indisponível em caso de erro
        finally:
            if conn:
                conn.close()

    # Definição da função adicionar registos à base de dados  

    def adicionar(self):
        
        id_cliente = _validate_int_input(self.entry2_r.get().strip(), "ID Cliente")
        id_veiculo = _validate_int_input(self.entry3_r.get().strip(), "ID Veículo")
        
        # Valida e obtém a data de início formatada
        data_inicio = _validate_date_input(self.entry4_r.get().strip(), "Data Início")
        if data_inicio is None: return

        # Valida e obtém a data de fim formatada
        data_fim = _validate_date_input(self.entry5_r.get().strip(), "Data Fim")
        if data_fim is None: return

        preco_total = _validate_float_input(self.entry6_r.get().strip(), "Preço Total")
        id_forma_pagamento = _validate_int_input(self.entry7_r.get().strip(), "ID Forma Pagamento")
        data_reserva = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Auto-generated

        # Check if mandatory fields are filled and valid (após as validações individuais)
        if not all([id_cliente is not None, id_veiculo is not None, preco_total is not None, id_forma_pagamento is not None]):
            # As mensagens de erro já foram exibidas pelas funções _validate_*
            return

        try:
            start_date_dt = datetime.datetime.strptime(data_inicio, '%Y-%m-%d')
            end_date_dt = datetime.datetime.strptime(data_fim, '%Y-%m-%d')
            if start_date_dt > end_date_dt:
                messagebox.showerror("Erro de Validação", "A Data de Início não pode ser posterior à Data de Fim.")
                return
        except ValueError as ve:
            messagebox.showerror("Erro de Validação", f"Formato de data inválido na Data de Início ou Data de Fim. Use YYYY-MM-DD. Detalhe: {ve}")
            return

        # Nova verificação de disponibilidade para adicionar
        if not self._is_vehicle_available(id_veiculo, data_inicio, data_fim):
            messagebox.showerror("Erro de Disponibilidade", f"O veículo com ID {id_veiculo} já tem uma reserva para o período de {data_inicio} a {data_fim}.")
            return


        confirmation = messagebox.askyesno("Confirmação", f"Tem a certeza que deseja adicionar esta reserva?")
        if not confirmation:
            return

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()

            # Check if foreign keys exist
            cur.execute("SELECT 1 FROM clientes WHERE id_cliente = ?", (id_cliente,))
            if cur.fetchone() is None:
                messagebox.showerror("Erro", f"O Cliente com ID {id_cliente} não existe.")
                return

            cur.execute("SELECT 1 FROM veiculos WHERE id_veiculo = ?", (id_veiculo,))
            if cur.fetchone() is None:
                messagebox.showerror("Erro", f"O Veículo com ID {id_veiculo} não existe.")
                return

            cur.execute("SELECT 1 FROM formas_pagamento WHERE id_forma_pagamento = ?", (id_forma_pagamento,))
            if cur.fetchone() is None:
                messagebox.showerror("Erro", f"A Forma de Pagamento com ID {id_forma_pagamento} não existe.")
                return

            cur.execute("""
                INSERT INTO reservas (id_cliente, id_veiculo, data_inicio, data_fim, preco_total, id_forma_pagamento, data_reserva)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (id_cliente, id_veiculo, data_inicio, data_fim, preco_total, id_forma_pagamento, data_reserva))
            conn.commit()
            messagebox.showinfo("Sucesso", "Reserva adicionada com sucesso!")
            self.listar()
            self.limpar_campos()

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar a reserva: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()


# Definição da função editar que permite alterar os registos à base de dados              

    def editar(self):
        # Garante que um item está selecionado na Treeview
        selected_item = self.my_tree.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione uma reserva na tabela para editar.")
            return

        # Obter os valores originais do item selecionado na Treeview (para campos não editáveis no formulário)
        values_from_tree = self.my_tree.item(selected_item, 'values')
        if not values_from_tree: # Verifica se há valores (um item pode estar focado mas sem valores)
            messagebox.showerror("Erro", "Não foi possível obter os dados da reserva selecionada.")
            return

        # ID_Reserva é obtido da Treeview porque é read-only no formulário
        id_reserva = _validate_int_input(values_from_tree[0], "ID Reserva")
        if id_reserva is None: return # Se a validação do ID da reserva falhar

        # Data de Fim ORIGINAL da Treeview (não editável)
        original_data_fim_str = str(values_from_tree[4]).strip() 
        
        # Obter os valores dos campos de entrada editáveis pelo utilizador
        data_inicio_str = self.entry4_r.get().strip()
        
        # Validar e obter a Data de Início do campo de entrada (já formatada por _validate_date_input)
        data_inicio = _validate_date_input(data_inicio_str, "Data Início") 
        if data_inicio is None: return # Se a validação da Data de Início falhar, a função já exibiu o erro.

        preco_total = _validate_float_input(self.entry6_r.get().strip(), "Preço Total")
        id_cliente = _validate_int_input(self.entry2_r.get().strip(), "ID Cliente")
        id_veiculo = _validate_int_input(self.entry3_r.get().strip(), "ID Veículo")
        id_forma_pagamento = _validate_int_input(self.entry7_r.get().strip(), "ID Forma Pagamento")


        # Verifica se todos os campos obrigatórios e válidos foram preenchidos (exceto Data Início, já tratada)
        if not all([id_cliente is not None, id_veiculo is not None, preco_total is not None, id_forma_pagamento is not None]):
            # As funções _validate_* já exibiram a mensagem de erro para outros campos.
            return

        # Validação da Data de Início vs. Data de Fim
        try:
            start_date_dt = datetime.datetime.strptime(data_inicio, '%Y-%m-%d')
            
            end_date_dt = None
            if original_data_fim_str: # Apenas tenta converter se não for uma string vazia
                try:
                    # Tenta converter a data de fim. Se tiver um componente de hora, remove-o primeiro.
                    end_date_dt = datetime.datetime.strptime(original_data_fim_str.split(' ')[0], '%Y-%m-%d')
                except ValueError:
                    messagebox.showerror("Erro de Validação", f"A Data de Fim '{original_data_fim_str}' da tabela tem um formato inválido. Deve ser YYYY-MM-DD.")
                    return
            else:
                messagebox.showerror("Erro de Validação", "A Data de Fim da reserva selecionada está vazia ou inválida.")
                return

            if start_date_dt > end_date_dt:
                messagebox.showerror("Erro de Validação", "A Data de Início não pode ser posterior à Data de Fim.")
                return
        except ValueError as ve:
            messagebox.showerror("Erro de Validação", f"Ocorreu um erro ao comparar as datas. Verifique os formatos (YYYY-MM-DD). Detalhe: {ve}")
            return

        # NOVO: Verificar disponibilidade do veículo para o período de edição
        # Usamos original_data_fim_str porque a data de fim não é editável no formulário
        if not self._is_vehicle_available(id_veiculo, data_inicio, original_data_fim_str, exclude_reserva_id=id_reserva):
            messagebox.showerror("Erro de Disponibilidade", f"O veículo com ID {id_veiculo} já tem uma reserva sobreposta para o período de {data_inicio} a {original_data_fim_str}.")
            return


        confirmation = messagebox.askyesno("Confirmação", f"Tem a certeza que deseja editar a reserva ID {id_reserva}? A Data de Fim não será alterada.")
        if not confirmation:
            return

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()

            # Validações de chaves estrangeiras
            cur.execute("SELECT 1 FROM clientes WHERE id_cliente = ?", (id_cliente,))
            if cur.fetchone() is None:
                messagebox.showerror("Erro", f"O Cliente com ID {id_cliente} não existe.")
                return

            cur.execute("SELECT 1 FROM veiculos WHERE id_veiculo = ?", (id_veiculo,))
            if cur.fetchone() is None:
                messagebox.showerror("Erro", f"O Veículo com ID {id_veiculo} não existe.")
                return

            cur.execute("SELECT 1 FROM formas_pagamento WHERE id_forma_pagamento = ?", (id_forma_pagamento,))
            if cur.fetchone() is None:
                messagebox.showerror("Erro", f"A Forma de Pagamento com ID {id_forma_pagamento} não existe.")
                return

            cur.execute("""
                UPDATE reservas
                SET
                    id_cliente = ?,
                    id_veiculo = ?,
                    data_inicio = ?,
                    preco_total = ?,
                    id_forma_pagamento = ?
                WHERE id_reserva = ?
            """, (id_cliente, id_veiculo, data_inicio, preco_total, id_forma_pagamento, id_reserva))
            conn.commit()
            if cur.rowcount > 0:
                messagebox.showinfo("Sucesso", f"Reserva ID {id_reserva} editada com sucesso!")
                self.listar()
                self.limpar_campos()
            else:
                messagebox.showinfo("Informação", "Nenhuma reserva foi atualizada. Verifique se o ID da reserva existe.")

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao editar a reserva: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    # Definição da função remover registos da base de dados

    def remover(self):
        
        selected_item = self.my_tree.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione uma reserva na tabela para remover.")
            return

        values = self.my_tree.item(selected_item, 'values')
        id_reserva_to_delete = values[0]

        confirmation = messagebox.askyesno("Confirmação", f"Tem a certeza que deseja remover a reserva ID {id_reserva_to_delete}?")
        if not confirmation:
            return

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            cur.execute("DELETE FROM reservas WHERE id_reserva = ?", (id_reserva_to_delete,))
            if cur.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Sucesso", f"Reserva ID {id_reserva_to_delete} removida com sucesso!")
                self.listar()
                self.limpar_campos()
            else:
                messagebox.showinfo("Informação", f"Nenhuma reserva com o ID '{id_reserva_to_delete}' foi encontrada.")

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao remover a reserva: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def limpar_campos(self):
        
        self.entry1_r.configure(state='normal')
        self.entry1_r.delete(0, tk.END)
        self.entry1_r.configure(state='readonly')
        self.entry2_r.delete(0, tk.END)
        self.entry3_r.delete(0, tk.END)
        self.entry4_r.delete(0, tk.END)
        
        self.entry5_r.configure(state='normal') # Set to normal to clear
        self.entry5_r.delete(0, tk.END)
        self.entry5_r.configure(state='readonly') # Set back to readonly after clearing
        
        self.entry6_r.delete(0, tk.END)
        self.entry7_r.delete(0, tk.END)
        
        self.entry8_r.configure(state='normal') 
        self.entry8_r.delete(0, tk.END)
        self.entry8_r.configure(state='readonly') 
        self.search_var.set("") 

    # Função para exportar dados para Excel 

    def export_to_excel(self):
        
        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            
            df = pd.read_sql_query("""
                SELECT
                    id_reserva AS "ID Reserva",
                    id_cliente AS "ID Cliente",
                    id_veiculo AS "ID Veículo",
                    data_inicio AS "Data Início",
                    data_fim AS "Data Fim",
                    preco_total AS "Preço Total",
                    id_forma_pagamento AS "ID Forma Pagamento",
                    data_reserva AS "Data Reserva"
                FROM reservas
                ORDER BY id_reserva ASC
            """, conn)

            if df.empty:
                messagebox.showinfo("Exportar para Excel", "Não há dados para exportar.")
                return

            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     filetypes=[("Excel files", "*.xlsx")],
                                                     title="Guardar como Excel")
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Exportar para Excel", f"Dados exportados com sucesso para:\n{file_path}")

        except sqlite3.Error as e:
            messagebox.showerror("Erro de Base de Dados", f"Erro ao aceder à base de dados: {e}")
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

            df = pd.read_sql_query("""
                SELECT
                    id_reserva AS "ID Reserva",
                    id_cliente AS "ID Cliente",
                    id_veiculo AS "ID Veículo",
                    data_inicio AS "Data Início",
                    data_fim AS "Data Fim",
                    preco_total AS "Preço Total",
                    id_forma_pagamento AS "ID Forma Pagamento",
                    data_reserva AS "Data Reserva"
                FROM reservas
                ORDER BY id_reserva ASC
            """, conn)

            if df.empty:
                messagebox.showinfo("Exportar para CSV", "Não há dados para exportar.")
                return

            file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                     filetypes=[("CSV files", "*.csv")],
                                                     title="Guardar como CSV")
            if file_path:
                df.to_csv(file_path, index=False, encoding='utf-8')
                messagebox.showinfo("Exportar para CSV", f"Dados exportados com sucesso para:\n{file_path}")

        except sqlite3.Error as e:
            messagebox.showerror("Erro de Base de Dados", f"Erro ao aceder à base de dados: {e}")
        except Exception as e:
            messagebox.showerror("Erro de Exportação", f"Ocorreu um erro ao exportar para CSV: {e}")
        finally:
            if conn:
                conn.close()

# Função para voltar ao menu principal

    def menu(self):
        self.parent.deiconify()
        self.destroy()

# Função para sair da aplicação

    def sair(self):
        confirm = messagebox.askyesno("Sair", "Tem a certeza que deseja sair?")
        if confirm:
            self.parent.destroy()
            self.destroy() # Destroy the Toplevel window first


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()