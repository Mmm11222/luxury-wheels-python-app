import tkinter as tk
from tkinter import ttk, Scrollbar, VERTICAL, BOTH, RIGHT, Y, W, CENTER, END, messagebox, filedialog
import customtkinter as ctk
import sqlite3
import os
import datetime
import pandas as pd
import io
from PIL import Image, ImageTk # Import ImageTk

# Funções auxiliares de conversão de dados

def _convert_disponivel_to_db(value_str):
    """Converte 'Sim'/'Não' (ou 1/0) para o formato booleano do SQLite (1/0)."""
    if isinstance(value_str, bool): # boolean para integer
        return 1 if value_str else 0
    if isinstance(value_str, int): # string para integer( 0 ou 1)
        return value_str

    value_str = str(value_str).strip().lower()
    if value_str in ('sim', 'true', '1'):
        return 1
    elif value_str in ('não', 'nao', 'false', '0'):
        return 0
    return None

def _convert_disponivel_from_db(value_int):
    """Converte 1/0 do SQLite para 'Sim'/'Não' para exibição."""
    if value_int == 1:
        return "Sim"
    elif value_int == 0:
        return "Não"
    return ""

def _validate_numeric_input(value, field_name):
    """Valida se um valor pode ser convertido para inteiro ou float."""
    try:
        if field_name in ["Preco_dia"]:
            return float(value)
        else:
            return int(value)
    except ValueError:
        messagebox.showerror("Erro de Entrada", f"O campo '{field_name}' deve ser um número válido.")
        return None

def _validate_date_input(date_str, field_name):
    """Valida se uma string é uma data no formato AAAA-MM-DD."""
    if not date_str: # Allow empty date strings
        return None
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        return date_str
    except ValueError:
        messagebox.showerror("Erro de Entrada", f"O campo '{field_name}' deve ter o formato AAAA-MM-DD.")
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

        self.b3 = ctk.CTkButton(self, text="Veículos", command=self.janela_veiculos, height=40)
        self.b3.grid(row=3, column=0, sticky="nsew", pady=10, padx=100)

        self.b4 = ctk.CTkButton(self, text="Clientes", height=40)
        self.b4.grid(row=4, column=0, sticky="nsew", pady=10, padx=100)

        self.b5 = ctk.CTkButton(self, text="Formas de Pagamento", height=40)
        self.b5.grid(row=5, column=0, sticky="nsew", pady=10, padx=100)

        self.b6 = ctk.CTkButton(self, text="Utilizadores", height=40)
        self.b6.grid(row=6, column=0, sticky="nsew", pady=10, padx=100)


    def janela_veiculos(self):

        self.iconify() # Minimiza a janela principal
        self.after(10, self._create_veiculos_window_and_alerts)


    def _create_veiculos_window_and_alerts(self):
        #
        self.veiculos_window = JanelaVeiculos(self)
        self.veiculos_window.grab_set()


# Definição da janela secundária Veiculos

class JanelaVeiculos(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Módulo Veículos")
        self.geometry("1600x800")
        self.resizable(True, True)

        # To store the displayed image to prevent garbage collection
        self.current_photo = None

# Permitir a expansão das colunas e linhas da janela

        for i in range(21):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(0, weight=1) # Para o treeview frame (expandir verticalmente)
        self.grid_rowconfigure(1, weight=0) # Para o search frame
        self.grid_rowconfigure(2, weight=0) # Para o data frame
        self.grid_rowconfigure(3, weight=0) # Para o button frame
        self.grid_rowconfigure(4, weight=0) # For export buttons

        self.protocol("WM_DELETE_WINDOW", self.sair)


# Configuração  do estilo da janela veiculos

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


# Definição dos Widgets da janela veiculos:

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


        self.my_tree.tag_configure('alert_red', foreground='red', font=('Arial', 10, 'bold')) # Alerta com cor vermelha


# Definição das colunas da Treeview para Veículos

        self.my_tree["columns"] = ("ID_Veiculo", "Marca", "Modelo", "Ano", "Matricula", "Tipo", "Categoria", "Combustivel",
                                   "Cilindrada", "Potencia_cv", "Lugares", "Preco_dia", "Disponivel",
                                   "Ultima_Data_Revisao", "Proxima_Data_Revisao", "Ultima_Data_Inspecao",
                                   "Proxima_Data_Inspecao", "fotos", "Id_Utilizador")
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.heading("#0", text="")
        self.my_tree.column("ID_Veiculo", anchor=CENTER, width=80)
        self.my_tree.heading("ID_Veiculo", text="ID")
        self.my_tree.column("Marca", anchor=CENTER, width=120)
        self.my_tree.heading("Marca", text="Marca")
        self.my_tree.column("Modelo", anchor=CENTER, width=120)
        self.my_tree.heading("Modelo", text="Modelo")
        self.my_tree.column("Ano", anchor=CENTER, width=80)
        self.my_tree.heading("Ano", text="Ano")
        self.my_tree.column("Matricula", anchor=CENTER, width=100)
        self.my_tree.heading("Matricula", text="Matrícula")
        self.my_tree.column("Tipo", anchor=CENTER, width=100)
        self.my_tree.heading("Tipo", text="Tipo")
        self.my_tree.column("Categoria", anchor=CENTER, width=100)
        self.my_tree.heading("Categoria", text="Categoria")
        self.my_tree.column("Combustivel", anchor=CENTER, width=80)
        self.my_tree.heading("Combustivel", text="Combustível")
        self.my_tree.column("Cilindrada", anchor=CENTER, width=100)
        self.my_tree.heading("Cilindrada", text="Cilindrada")
        self.my_tree.column("Potencia_cv", anchor=CENTER, width=100)
        self.my_tree.heading("Potencia_cv", text="Potência (CV)")
        self.my_tree.column("Lugares", anchor=CENTER, width=80)
        self.my_tree.heading("Lugares", text="Lugares")
        self.my_tree.column("Preco_dia", anchor=CENTER, width=80)
        self.my_tree.heading("Preco_dia", text="Preço/Dia")
        self.my_tree.column("Disponivel", anchor=CENTER, width=100)
        self.my_tree.heading("Disponivel", text="Disponível")
        self.my_tree.column("Ultima_Data_Revisao", anchor=CENTER, width=120)
        self.my_tree.heading("Ultima_Data_Revisao", text="Última Revisão")
        self.my_tree.column("Proxima_Data_Revisao", anchor=CENTER, width=120)
        self.my_tree.heading("Proxima_Data_Revisao", text="Próxima Revisão")
        self.my_tree.column("Ultima_Data_Inspecao", anchor=CENTER, width=120)
        self.my_tree.heading("Ultima_Data_Inspecao", text="Última Inspeção")
        self.my_tree.column("Proxima_Data_Inspecao", anchor=CENTER, width=120)
        self.my_tree.heading("Proxima_Data_Inspecao", text="Próxima Inspeção")
        self.my_tree.column("fotos", anchor=CENTER, width=120)
        self.my_tree.heading("fotos", text="Foto (BLOB)") # Changed to reflect BLOB nature
        self.my_tree.column("Id_Utilizador", anchor=CENTER, width=80)
        self.my_tree.heading("Id_Utilizador", text="ID Utilizador")


# Definição do campo pesquisar

        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(fill='x', expand='yes', padx=20, pady=10)

        # Permite que as colunas se expandam
        for i in range(10):
            self.search_frame.grid_columnconfigure(i, weight=1)

        self.search_label = ctk.CTkLabel(self.search_frame, text="Pesquisar por:", font=ctk.CTkFont(weight="bold"))
        self.search_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self.search_frame, textvariable=self.search_var, width=200)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.search_button = ctk.CTkButton(self.search_frame, text="Pesquisar",font=ctk.CTkFont(weight="bold"), command=self.search_database,
                                           fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        self.search_options_label = ctk.CTkLabel(self.search_frame, text="Opções de Pesquisa:", font=ctk.CTkFont(weight="bold"))
        self.search_options_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        self.search_option_var = ctk.StringVar(value="Matricula") # Valor padrão para veículos

        self.search_option_marca = ctk.CTkRadioButton(self.search_frame, text="Marca", variable=self.search_option_var, value="Marca")
        self.search_option_marca.grid(row=1, column=1, padx=10, pady=2, sticky=W)
        self.search_option_matricula = ctk.CTkRadioButton(self.search_frame, text="Matrícula", variable=self.search_option_var, value="Matricula")
        self.search_option_matricula.grid(row=1, column=2, padx=10, pady=2, sticky=W)
        self.search_option_modelo = ctk.CTkRadioButton(self.search_frame, text="Modelo", variable=self.search_option_var, value="Modelo")
        self.search_option_modelo.grid(row=1, column=3, padx=10, pady=2, sticky=W)
        self.search_option_ano = ctk.CTkRadioButton(self.search_frame, text="Ano", variable=self.search_option_var, value="Ano")
        self.search_option_ano.grid(row=1, column=4, padx=10, pady=2, sticky=W)
        self.search_option_tipo = ctk.CTkRadioButton(self.search_frame, text="Tipo", variable=self.search_option_var, value="Tipo")
        self.search_option_tipo.grid(row=1, column=5, padx=10, pady=2, sticky=W)
        self.search_option_categoria = ctk.CTkRadioButton(self.search_frame, text="Categoria", variable=self.search_option_var, value="Categoria")
        self.search_option_categoria.grid(row=1, column=6, padx=10, pady=2, sticky=W)
        self.search_option_combustivel = ctk.CTkRadioButton(self.search_frame, text="Combustível", variable=self.search_option_var, value="Combustivel")
        self.search_option_combustivel.grid(row=1, column=7, padx=10, pady=2, sticky=W)
        self.search_option_lugares = ctk.CTkRadioButton(self.search_frame, text="Lugares", variable=self.search_option_var, value="Lugares")
        self.search_option_lugares.grid(row=1, column=8, padx=10, pady=2, sticky=W)
        self.search_option_preco_dia = ctk.CTkRadioButton(self.search_frame, text="Preço/Dia", variable=self.search_option_var, value="Preco_dia")
        self.search_option_preco_dia.grid(row=1, column=9, padx=10, pady=2, sticky=W)
        self.search_option_disponivel = ctk.CTkRadioButton(self.search_frame, text="Disponível", variable=self.search_option_var, value="Disponivel")
        self.search_option_disponivel.grid(row=1, column=10, padx=10, pady=2, sticky=W)


# Definição do campo dados

        self.data_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.data_frame.pack(fill='x', expand='yes', padx=20, pady=10)

        # Configure columns for expansion. We will now use 8 columns for fields and an extra column for the image.
        # This will simplify the layout and give more room to the image.
        # We'll have 4 pairs of label/entry per row, then the image.
        for i in range(8): # Columns 0-7 for the input fields
            self.data_frame.grid_columnconfigure(i, weight=1)
        self.data_frame.grid_columnconfigure(8, weight=3) # Column for the image, giving it more weight

        # Linha 0 de entradas
        self.label1 = ctk.CTkLabel(self.data_frame, text="ID_Veículo:")
        self.label1.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.entry1 = ctk.CTkEntry(self.data_frame, width=100, state='readonly') # ID_Veiculo deve ser readonly
        self.entry1.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.label2 = ctk.CTkLabel(self.data_frame, text="Marca:")
        self.label2.grid(row=0, column=2, padx=5, pady=5, sticky=W)
        self.entry2 = ctk.CTkEntry(self.data_frame, width=120)
        self.entry2.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.label3 = ctk.CTkLabel(self.data_frame, text="Modelo:")
        self.label3.grid(row=0, column=4, padx=5, pady=5, sticky=W)
        self.entry3 = ctk.CTkEntry(self.data_frame, width=120)
        self.entry3.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        self.label4 = ctk.CTkLabel(self.data_frame, text="Ano:")
        self.label4.grid(row=0, column=6, padx=5, pady=5, sticky=W)
        self.entry4 = ctk.CTkEntry(self.data_frame, width=80)
        self.entry4.grid(row=0, column=7, padx=5, pady=5, sticky="ew")

        # Linha 1 de entradas (now including Categoria)
        self.label7 = ctk.CTkLabel(self.data_frame, text="Categoria:") # Moved "Categoria" here
        self.label7.grid(row=1, column=0, padx=5, pady=5, sticky=W) # Now column 0
        self.entry7 = ctk.CTkEntry(self.data_frame, width=100)
        self.entry7.grid(row=1, column=1, padx=5, pady=5, sticky="ew") # Now column 1

        self.label5 = ctk.CTkLabel(self.data_frame, text="Matrícula:")
        self.label5.grid(row=1, column=2, padx=5, pady=5, sticky=W)
        self.entry5 = ctk.CTkEntry(self.data_frame, width=100)
        self.entry5.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        self.label6 = ctk.CTkLabel(self.data_frame, text="Tipo:")
        self.label6.grid(row=1, column=4, padx=5, pady=5, sticky=W)
        self.entry6 = ctk.CTkEntry(self.data_frame, width=100)
        self.entry6.grid(row=1, column=5, padx=5, pady=5, sticky="ew")

        self.label8 = ctk.CTkLabel(self.data_frame, text="Combustível:")
        self.label8.grid(row=1, column=6, padx=5, pady=5, sticky=W)
        self.entry8 = ctk.CTkEntry(self.data_frame, width=100)
        self.entry8.grid(row=1, column=7, padx=5, pady=5, sticky="ew")


        # Linha 2 de entradas
        self.label9 = ctk.CTkLabel(self.data_frame, text="Cilindrada:")
        self.label9.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.entry9 = ctk.CTkEntry(self.data_frame, width=120)
        self.entry9.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.label10 = ctk.CTkLabel(self.data_frame, text="Potência (CV):")
        self.label10.grid(row=2, column=2, padx=5, pady=5, sticky=W)
        self.entry10 = ctk.CTkEntry(self.data_frame, width=120)
        self.entry10.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        self.label11 = ctk.CTkLabel(self.data_frame, text="Lugares:")
        self.label11.grid(row=2, column=4, padx=5, pady=5, sticky=W)
        self.entry11 = ctk.CTkEntry(self.data_frame, width=80)
        self.entry11.grid(row=2, column=5, padx=5, pady=5, sticky="ew")

        self.label12 = ctk.CTkLabel(self.data_frame, text="Preço/Dia:")
        self.label12.grid(row=2, column=6, padx=5, pady=5, sticky=W)
        self.entry12 = ctk.CTkEntry(self.data_frame, width=80)
        self.entry12.grid(row=2, column=7, padx=5, pady=5, sticky="ew")

        # Linha 3 de entradas
        self.label13 = ctk.CTkLabel(self.data_frame, text="Disponível:")
        self.label13.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.entry13 = ctk.CTkEntry(self.data_frame, width=100)
        self.entry13.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.label14 = ctk.CTkLabel(self.data_frame, text="Última Revisão:")
        self.label14.grid(row=3, column=2, padx=5, pady=5, sticky=W)
        self.entry14 = ctk.CTkEntry(self.data_frame, width=120)
        self.entry14.grid(row=3, column=3, padx=5, pady=5, sticky="ew")

        self.label15 = ctk.CTkLabel(self.data_frame, text="Próxima Revisão:")
        self.label15.grid(row=3, column=4, padx=5, pady=5, sticky=W)
        self.entry15 = ctk.CTkEntry(self.data_frame, width=120)
        self.entry15.grid(row=3, column=5, padx=5, pady=5, sticky="ew")

        self.label16 = ctk.CTkLabel(self.data_frame, text="Última Inspeção:")
        self.label16.grid(row=3, column=6, padx=5, pady=5, sticky=W)
        self.entry16 = ctk.CTkEntry(self.data_frame, width=120)
        self.entry16.grid(row=3, column=7, padx=5, pady=5, sticky="ew")

        # Linha 4 de entradas (Id_Utilizador)
        self.label17 = ctk.CTkLabel(self.data_frame, text="Próxima Inspeção:")
        self.label17.grid(row=4, column=0, padx=5, pady=5, sticky=W)
        self.entry17 = ctk.CTkEntry(self.data_frame, width=120)
        self.entry17.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.label19 = ctk.CTkLabel(self.data_frame, text="ID Utilizador:")
        self.label19.grid(row=4, column=2, padx=5, pady=5, sticky=W)
        self.entry19 = ctk.CTkEntry(self.data_frame, width=100)
        self.entry19.grid(row=4, column=3, padx=5, pady=5, sticky="ew")

        # Image and Load Photo Button
        self.label18 = ctk.CTkLabel(self.data_frame, text="Foto:")
        self.label18.grid(row=0, column=8, padx=5, pady=5, sticky=W) # Place label next to image display

        # Image display label (initially empty)
        # Increased width and height significantly, and spanned it across more rows and columns.
        self.image_display_label = ctk.CTkLabel(self.data_frame, text="", width=250, height=200, fg_color="#e0e0e0") # Added fg_color for visibility
        self.image_display_label.grid(row=0, column=9, rowspan=5, columnspan=2, padx=10, pady=5, sticky="nsew") # Spans 5 rows and 2 columns

        
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

        self.button6 = ctk.CTkButton(self.button_frame, text="Sair", command=self.sair,
                                     fg_color="#eeb752", text_color="black", font=ctk.CTkFont(weight="bold"),hover_color="#d4a347")
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
        self.check_maintenance_alerts() # Chama a função de verificação de alertas ao iniciar a janela


# Definição da função listar que vai buscar as tabelas à base de dados e insere-a na treeview

    def listar(self):
        for item in self.my_tree.get_children():
            self.my_tree.delete(item)

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM veiculos")
            rows = cur.fetchall()

            for i, row in enumerate(rows):
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',) # verifica o status da coluna disponibilidade (Boolean 0 ou 1)

                if row[12] == 0: # Se Disponível é 0
                    tags = tags + ('alert_red',) # Cria o tag de alerta

                display_row = list(row) # converte o satatus da coluna 'disponível' 0/1 para 'Não'/'Sim'
                display_row[12] = _convert_disponivel_from_db(row[12])

                # For the "fotos" column, show "Sim" or "Não" if there's data, instead of the raw BLOB
                if row[17]: # Check if the 'fotos' BLOB data exists
                    display_row[17] = "Sim"
                else:
                    display_row[17] = "Não"

                self.my_tree.insert("", END, values=display_row, tags=tags)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao aceder à base de dados de veículos: {e}")
        finally:
            if conn:
                conn.close()


# Definição da  função para verificação de alertas de manutenção e atualizar status

    def check_maintenance_alerts(self):
        conn = None
        alerts = []
        today = datetime.date.today()

        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            cur.execute("SELECT ID_Veiculo, Matricula, Proxima_Data_Revisao, Proxima_Data_Inspecao, Disponivel FROM veiculos")
            vehicles = cur.fetchall()

            for vehicle in vehicles:
                vehicle_id, matricula, next_revision_str, next_inspection_str, disponivel_db = vehicle

                alert_messages = [] # Criação de alertas
                should_suggest_unavailable = False # Flag que sugere a alteração da disponibilidade do veículo


# verificação da proxima data de Revisão

                if next_revision_str:
                    try:
                        next_revision_date = datetime.datetime.strptime(next_revision_str, '%Y-%m-%d').date()
                        days_until_revision = (next_revision_date - today).days
                        if days_until_revision <= 15: # verifica se são 5 ou menos dias até à data de revisão
                            alert_messages.append(f"Próxima Revisão em {days_until_revision} dias.")
                            should_suggest_unavailable = True
                    except ValueError:
                        alert_messages.append(f"Data de Revisão inválida ('{next_revision_str}').")
                else:
                    alert_messages.append("Data da Próxima Revisão não definida.")

# verificação da proxima data de Inspecção

                if next_inspection_str:
                    try:
                        next_inspection_date = datetime.datetime.strptime(next_inspection_str, '%Y-%m-%d').date()
                        days_until_inspection = (next_inspection_date - today).days
                        if days_until_inspection <= 15: # verifica se são 5 ou menos dias até à data de revisão
                            alert_messages.append(f"Próxima Inspeção em {days_until_inspection} dias.")
                            should_suggest_unavailable = True
                    except ValueError:
                        alert_messages.append(f"Data de Inspeção inválida ('{next_inspection_str}').")
                else:
                    alert_messages.append("Data da Próxima Inspeção não definida.")

                if alert_messages: # Verifica se existem alertas
                    full_vehicle_alert = f"Veículo **{matricula}** (ID: {vehicle_id}): " + ", ".join(alert_messages)
                    alerts.append(full_vehicle_alert)

                    if should_suggest_unavailable and disponivel_db == 1:
                        # Aviso para o utilizador
                        response = messagebox.askyesno(
                            "Manutenção Pendente",
                            f"O veículo {matricula} tem manutenção pendente e está atualmente **DISPONÍVEL**.\n\n"
                            f"Detalhes: {', '.join(alert_messages)}\n\n"
                            "Gostaria de marcá-lo como **INDISPONÍVEL** para manutenção agora?"
                        )
                        if response:
                            cur.execute("UPDATE veiculos SET Disponivel = ? WHERE ID_Veiculo = ?", (0, vehicle_id))
                            conn.commit()
                            messagebox.showinfo("Status Atualizado", f"Veículo {matricula} marcado como INDISPONÍVEL.")
                        else:
                            messagebox.showinfo("Status Mantido", f"Veículo {matricula} permanece DISPONÍVEL por sua escolha.")

            if alerts:
                # Apresentação de resumo de alertas
                summary_message = "Resumo dos Alertas de Manutenção:\n\n" + "\n".join(alerts)
                messagebox.showwarning("Alertas de Manutenção de Veículos", summary_message)

            self.listar() # Refresh da Treeview

        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao verificar alertas de manutenção: {e}")
            if conn:
                conn.rollback() # reverte as alterações efetuadas em caso de erro
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
                self.listar()
                return

# Opções mapping search para as colunas
            column_map = {
                "Marca": "marca",
                "Modelo": "modelo",
                "Ano": "ano",
                "Matricula": "matricula",
                "Tipo": "tipo",
                "Categoria": "categoria",
                "Combustivel": "combustivel",
                "Lugares": "lugares",
                "Preco_dia": "preco_dia",
                "Disponivel": "disponivel",
                "Proxima_Data_Revisao": "proxima_data_revisao",
                "Proxima_Data_Inspecao": "proxima_data_inspecao",
            }

            db_column = column_map.get(search_option) # mapping para pesquisa 'Disponivel' search
            if db_column:

                if db_column == "disponivel":
                    if search_term.lower() in ('sim', 'true', '1'):
                        search_value = 1
                    elif search_term.lower() in ('não', 'nao', 'false', '0'):
                        search_value = 0
                    else:
                        messagebox.showinfo("Pesquisa", "Para 'Disponível', use 'Sim' ou 'Não'.")
                        self.listar()
                        return
                    query = f"SELECT * FROM veiculos WHERE {db_column} = ?"
                    search_param = (search_value,)
                else:
                    query = f"SELECT * FROM veiculos WHERE {db_column} LIKE ?"
                    search_param = (f"%{search_term}%",)

            else:
                messagebox.showinfo("Informação", "Selecione uma opção de pesquisa válida para veículos.")
                return

            cur.execute(query, search_param)
            rows = cur.fetchall()

            if not rows:
                messagebox.showinfo("Pesquisa", "Nenhum veículo encontrado com os critérios fornecidos.")

            for i, row in enumerate(rows):
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                if row[12] == 0:
                    tags = tags + ('alert_red',)

                display_row = list(row)
                display_row[12] = _convert_disponivel_from_db(row[12])

                if row[17]: # Check if the 'fotos' BLOB data exists
                    display_row[17] = "Sim"
                else:
                    display_row[17] = "Não"

                self.my_tree.insert("", END, values=display_row, tags=tags)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao pesquisar veículos: {e}")

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

            for entry_widget in [self.entry1, self.entry2, self.entry3, self.entry4, self.entry5, self.entry6,
                                 self.entry7, self.entry8, self.entry9, self.entry10, self.entry11, self.entry12,
                                 self.entry13, self.entry14, self.entry15, self.entry16, self.entry17, self.entry19]: # Exclude entry18
                entry_widget.delete(0, END)

            self.entry1.insert(0, values[0])  # ID_Veiculo
            self.entry2.insert(0, values[1])  # Marca
            self.entry3.insert(0, values[2])  # Modelo
            self.entry4.insert(0, values[3])  # Ano
            self.entry5.insert(0, values[4])  # Matricula
            self.entry6.insert(0, values[5])  # Tipo
            self.entry7.insert(0, values[6])  # Categoria
            self.entry8.insert(0, values[7])  # Combustivel
            self.entry9.insert(0, values[8])  # Cilindrada
            self.entry10.insert(0, values[9]) # Potencia_cv
            self.entry11.insert(0, values[10])# Lugares
            self.entry12.insert(0, values[11])# Preco_dia
            self.entry13.insert(0, values[12])# Disponivel
            self.entry14.insert(0, values[13])# Ultima_Data_Revisao
            self.entry15.insert(0, values[14])# Proxima_Data_Revisao
            self.entry16.insert(0, values[15])# Ultima_Data_Inspecao
            self.entry17.insert(0, values[16])# Proxima_Data_Inspecao
            # values[17] corresponde ao valor nas  'fotos', "Sim" or "Não" from the treeview, e não do atual BLOB
            self.entry19.insert(0, values[18])# Id_Utilizador

            self.entry1.configure(state='readonly')

            # Apresenta a imagem da base de dados, se existir
            vehicle_id = values[0]
            self.display_image_from_db(vehicle_id)

        except IndexError as e:
            messagebox.showerror("Erro de Acesso", f"Erro ao aceder a um índice: {e}. Verifique se todos os campos estão preenchidos na base de dados para o item selecionado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao aceder o registo: {e}")


# Definição da função que permite ler iamgens base de dados 

    def display_image_from_db(self, vehicle_id):
        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            cur.execute("SELECT fotos FROM veiculos WHERE ID_Veiculo = ?", (vehicle_id,))
            result = cur.fetchone()

            if result and result[0]:
                image_blob = result[0]
                image = Image.open(io.BytesIO(image_blob))

                # aumentando a imagem mantendo o aspect ratio
                label_width = self.image_display_label.winfo_width() # largura do label
                label_height = self.image_display_label.winfo_height() # altura do label

                # tamanho default da imagem
                if label_width == 1 and label_height == 1: #
                    label_width = self.image_display_label.cget("width")
                    label_height = self.image_display_label.cget("height")
                
                
                if label_width <= 1: label_width = 250 
                if label_height <= 1: label_height = 200

                image.thumbnail((label_width, label_height), Image.LANCZOS)
                photo = ctk.CTkImage(light_image=image, dark_image=image, size=(image.width, image.height))
                self.image_display_label.configure(image=photo)
                self.image_display_label.image = photo 

            else:
                self.image_display_label.configure(image=None, text="Sem Foto")
                self.image_display_label.image = None
                self.current_photo = None 

        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao carregar imagem do banco de dados: {e}")
            self.image_display_label.configure(image=None, text="Erro ao carregar foto")
            self.image_display_label.image = None
            self.current_photo = None

        except Exception as e:
            messagebox.showerror("Erro de Imagem", f"Não foi possível exibir a imagem: {e}")
            self.image_display_label.configure(image=None, text="Erro ao exibir foto")
            self.image_display_label.image = None
            self.current_photo = None

        finally:
            if conn:
                conn.close()


# Definição da função adicionar registos à base de dados 

    def adicionar(self):
        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()

           
            marca = self.entry2.get().strip()
            modelo = self.entry3.get().strip()
            ano = _validate_numeric_input(self.entry4.get().strip(), "Ano")
            matricula = self.entry5.get().strip()
            tipo = self.entry6.get().strip()
            categoria = self.entry7.get().strip()
            combustivel = self.entry8.get().strip()
            cilindrada = _validate_numeric_input(self.entry9.get().strip(), "Cilindrada")
            potencia_cv = _validate_numeric_input(self.entry10.get().strip(), "Potência (CV)")
            lugares = _validate_numeric_input(self.entry11.get().strip(), "Lugares")
            preco_dia = _validate_numeric_input(self.entry12.get().strip(), "Preco_dia")
            disponivel = _convert_disponivel_to_db(self.entry13.get().strip())
            ultima_data_revisao = _validate_date_input(self.entry14.get().strip(), "Última Data de Revisão")
            proxima_data_revisao = _validate_date_input(self.entry15.get().strip(), "Próxima Data de Revisão")
            ultima_data_inspecao = _validate_date_input(self.entry16.get().strip(), "Última Data de Inspeção")
            proxima_data_inspecao = _validate_date_input(self.entry17.get().strip(), "Próxima Data de Inspeção")
            id_utilizador = _validate_numeric_input(self.entry19.get().strip(), "ID Utilizador")

           
            if not all([marca, modelo, ano, matricula, tipo, categoria, combustivel, cilindrada, potencia_cv, lugares, preco_dia, disponivel is not None, id_utilizador]):
                messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha todos os campos obrigatórios.")
                return

            cur.execute("""INSERT INTO veiculos (Marca, Modelo, Ano, Matricula, Tipo, Categoria, Combustivel,
                                                 Cilindrada, Potencia_cv, Lugares, Preco_dia, Disponivel,
                                                 Ultima_Data_Revisao, Proxima_Data_Revisao, Ultima_Data_Inspecao,
                                                 Proxima_Data_Inspecao, fotos, Id_Utilizador)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (marca, modelo, ano, matricula, tipo, categoria, combustivel, cilindrada, potencia_cv,
                         lugares, preco_dia, disponivel, ultima_data_revisao, proxima_data_revisao,
                         ultima_data_inspecao, proxima_data_inspecao, None, id_utilizador)) # 'fotos' starts as None
            conn.commit()
            messagebox.showinfo("Sucesso", "Veículo adicionado com sucesso!")
            self.limpar_campos()
            self.listar() 

        except sqlite3.IntegrityError as e:

            if "UNIQUE constraint failed: veiculos.Matricula" in str(e):
                messagebox.showerror("Erro de Duplicação", "A Matrícula fornecida já existe. Por favor, insira uma matrícula única.")

            else:
                messagebox.showerror("Erro de Banco de Dados", f"Erro de integridade ao adicionar veículo: {e}")

        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao adicionar veículo: {e}")

            if conn:
                conn.rollback() 

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado ao adicionar veículo: {e}")

        finally:
            if conn:
                conn.close()


# Definição da função remover registos da base de dados

    def remover(self):

        selected_item = self.my_tree.focus()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um veículo para remover.")
            return

        response = messagebox.askyesno("Confirmar Remoção", "Tem certeza que deseja remover o veículo selecionado?")

        if response:
            vehicle_id = self.my_tree.item(selected_item, 'values')[0]
            conn = None

            try:
                conn = sqlite3.connect('database/BD_Frota.db')
                cur = conn.cursor()
                cur.execute("DELETE FROM veiculos WHERE ID_Veiculo = ?", (vehicle_id,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Veículo removido com sucesso!")
                self.limpar_campos()
                self.listar()

            except sqlite3.Error as e:
                messagebox.showerror("Erro de Banco de Dados", f"Erro ao remover veículo: {e}")

            finally:
                if conn:
                    conn.close()


# Definição da função editar que permite alterar os registos à base de dados 

    def editar(self):

        selected_item = self.my_tree.focus()

        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um veículo para editar.")
            return

        vehicle_id = self.my_tree.item(selected_item, 'values')[0]

      
        marca = self.entry2.get().strip()
        modelo = self.entry3.get().strip()
        ano = _validate_numeric_input(self.entry4.get().strip(), "Ano")
        matricula = self.entry5.get().strip()
        tipo = self.entry6.get().strip()
        categoria = self.entry7.get().strip()
        combustivel = self.entry8.get().strip()
        cilindrada = _validate_numeric_input(self.entry9.get().strip(), "Cilindrada")
        potencia_cv = _validate_numeric_input(self.entry10.get().strip(), "Potência (CV)")
        lugares = _validate_numeric_input(self.entry11.get().strip(), "Lugares")
        preco_dia = _validate_numeric_input(self.entry12.get().strip(), "Preco_dia")
        disponivel = _convert_disponivel_to_db(self.entry13.get().strip())
        ultima_data_revisao = _validate_date_input(self.entry14.get().strip(), "Última Data de Revisão")
        proxima_data_revisao = _validate_date_input(self.entry15.get().strip(), "Próxima Data de Revisão")
        ultima_data_inspecao = _validate_date_input(self.entry16.get().strip(), "Última Data de Inspeção")
        proxima_data_inspecao = _validate_date_input(self.entry17.get().strip(), "Próxima Data de Inspeção")
        id_utilizador = _validate_numeric_input(self.entry19.get().strip(), "ID Utilizador")

   
        if not all([marca, modelo, ano, matricula, tipo, categoria, combustivel, cilindrada, potencia_cv, lugares, preco_dia, disponivel is not None, id_utilizador]):
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha todos os campos obrigatórios.")
            return

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            cur.execute("""UPDATE veiculos SET
                           Marca = ?, Modelo = ?, Ano = ?, Matricula = ?, Tipo = ?, Categoria = ?, Combustivel = ?,
                           Cilindrada = ?, Potencia_cv = ?, Lugares = ?, Preco_dia = ?, Disponivel = ?,
                           Ultima_Data_Revisao = ?, Proxima_Data_Revisao = ?, Ultima_Data_Inspecao = ?,
                           Proxima_Data_Inspecao = ?, Id_Utilizador = ?
                           WHERE ID_Veiculo = ?""",
                        (marca, modelo, ano, matricula, tipo, categoria, combustivel, cilindrada, potencia_cv,
                         lugares, preco_dia, disponivel, ultima_data_revisao, proxima_data_revisao,
                         ultima_data_inspecao, proxima_data_inspecao, id_utilizador, vehicle_id))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Veículo ID {vehicle_id} atualizado com sucesso!")
            self.limpar_campos()
            self.listar()

        except sqlite3.IntegrityError as e:

            if "UNIQUE constraint failed: veiculos.Matricula" in str(e):
                messagebox.showerror("Erro de Duplicação", "A Matrícula fornecida já existe para outro veículo. Por favor, insira uma matrícula única.")

            else:
                messagebox.showerror("Erro de Banco de Dados", f"Erro de integridade ao editar veículo: {e}")

        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao editar veículo: {e}")

            if conn:
                conn.rollback()

        finally:
            if conn:
                conn.close()


    def limpar_campos(self):
        self.entry1.configure(state='normal') 

        for entry_widget in [self.entry1, self.entry2, self.entry3, self.entry4, self.entry5, self.entry6,
                             self.entry7, self.entry8, self.entry9, self.entry10, self.entry11, self.entry12,
                             self.entry13, self.entry14, self.entry15, self.entry16, self.entry17, self.entry19]:
            entry_widget.delete(0, END)

        self.image_display_label.configure(image=None, text="Sem Foto")
        self.image_display_label.image = None
        self.current_photo = None 
        self.entry1.configure(state='readonly') 


# Função para exportar dados para Excel 

    def export_to_excel(self):

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            df = pd.read_sql_query("SELECT * FROM veiculos", conn)

            # Converte a coluna  'Disponivel' para exportação para Excel 

            df['Disponivel'] = df['Disponivel'].apply(lambda x: _convert_disponivel_from_db(x))

            # Converte a coluna  'fotos' column fpara exportação para Excel ( "Sim"/"Não")

            df['fotos'] = df['fotos'].apply(lambda x: "Sim" if x else "Não")

            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Salvar como Excel"
            )

            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Exportar para Excel", "Dados exportados para Excel com sucesso!")

        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao exportar para Excel: {e}")

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
            df = pd.read_sql_query("SELECT * FROM veiculos", conn)

            # Converte a coluna  'Disponivel' para exportação para csv

            df['Disponivel'] = df['Disponivel'].apply(lambda x: _convert_disponivel_from_db(x))

            # Converte a coluna  'fotos' column fpara exportação para csv (show "Sim"/"Não")

            df['fotos'] = df['fotos'].apply(lambda x: "Sim" if x else "Não")

            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Salvar como CSV"
            )

            if file_path:
                df.to_csv(file_path, index=False, encoding='utf-8')
                messagebox.showinfo("Exportar para CSV", "Dados exportados para CSV com sucesso!")

        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao exportar para CSV: {e}")

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