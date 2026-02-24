# Importar as librarias necessárias

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Scrollbar, VERTICAL, BOTH, RIGHT, Y, W, CENTER, END, messagebox
import tkinter.font as tkFont
import customtkinter as ctk
import datetime
import sqlite3
import io
from PIL import Image, ImageTk # Import ImageTk


#Importar as janelas secundarias( top level windows) de cada modulo  por classes

from modulo_veiculos import JanelaVeiculos
from modulo_clientes import JanelaClientes
from modulo_reservas import JanelaReservas
from modulo_pagamentos import JanelaFormasPagamento
from modulo_dashboard import JanelaDashboard
from modulo_utilizadores import JanelaUtilizadores


# Configuração custom tkinter

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


# Definição da janela de login 

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App Gestão Luxury Wheels")
        self.geometry("350x400") 
        self.resizable(False, False) 

    
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        
        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=0) 
        self.grid_rowconfigure(2, weight=0) # Username label
        self.grid_rowconfigure(3, weight=0) # Username entry
        self.grid_rowconfigure(4, weight=0) # Password label
        self.grid_rowconfigure(5, weight=0) # Password entry
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=0) # Login button

      
        self.main_title = ctk.CTkLabel(self, text="Bem-vindo!",
                                       font=ctk.CTkFont(size=24, weight="bold"))
        self.main_title.grid(row=0, column=0, pady=(40, 20), sticky="n") 


        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, rowspan=4, padx=20, pady=0, sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.label_username = ctk.CTkLabel(self.input_frame, text="Utilizador:",
                                           font=ctk.CTkFont(weight="bold"))
        self.label_username.grid(row=0, column=0, padx=0, pady=(10, 0), sticky="ew") 

        self.entry_username = ctk.CTkEntry(self.input_frame, width=250, height=30) 
        self.entry_username.grid(row=1, column=0, padx=0, pady=(0, 15), sticky="ew")

        self.label_password = ctk.CTkLabel(self.input_frame, text="Password:",
                                           font=ctk.CTkFont(weight="bold"))
        self.label_password.grid(row=2, column=0, padx=0, pady=(10, 0), sticky="ew")

        self.entry_password = ctk.CTkEntry(self.input_frame, show="*", width=250, height=30) 
        self.entry_password.grid(row=3, column=0, padx=0, pady=(0, 15), sticky="ew")

# Definição dos Widgets da janela 

        self.login_button = ctk.CTkButton(self, text="Entrar", command=self.check_login,
                                          fg_color="#488cc4", text_color="black",
                                          hover_color="#6fabdc", font=ctk.CTkFont(size=16, weight="bold"),
                                          height=35, width=250) 
        self.login_button.grid(row=6, column=0, pady=(10, 60), sticky="s") 

        
        self.entry_password.bind("<Return>", lambda event: self.check_login())
        self.entry_username.bind("<Return>", lambda event: self.check_login())

        self.login_successful = False # 

# Definição da função do check de login:

    def check_login(self):
        username_input = self.entry_username.get()
        password_input = self.entry_password.get()

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cursor = conn.cursor()

            cursor.execute("SELECT password, ativo FROM utilizador WHERE nome = ?", (username_input,))
            result = cursor.fetchone()

            if result:
                db_password = result[0]
                db_ativo = result[1]

                if password_input == db_password: 
                    if db_ativo == 1:
                        messagebox.showinfo("Sucesso", "Login bem-sucedido!")
                        self.login_successful = True 
                        self.destroy() 
                    else:
                        messagebox.showerror("Erro de Login", "A sua conta está inativa. Contacte o administrador.")
                else:
                    messagebox.showerror("Erro de Login", "Nome de utilizador ou palavra-passe incorretos.")
                    self.entry_password.delete(0, END) 
            else:
                messagebox.showerror("Erro de Login", "Nome de utilizador ou palavra-passe incorretos.")
                self.entry_password.delete(0, END) 

        except sqlite3.Error as e:
            messagebox.showerror("Erro de Base de Dados", f"Ocorreu um erro ao aceder à base de dados: {e}")
        finally:
            if conn:
                conn.close()


# Definição da janela principal customtkinter

class Mainwindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App Gestão Luxury Wheels")
        self.geometry("500x500")
        self.resizable(True, True)
        self.grid_columnconfigure(0, weight=1)


# Definição dos Widgets da janela principal:

        self.mylabel = ctk.CTkLabel(self, text="Escolha o Módulo", font=ctk.CTkFont(size=20, weight="bold"))
        self.mylabel.grid(row=0, column=0, pady=20)

        self.b1 = ctk.CTkButton(self, text="Dashboard",command=self.janela_dashboard, height=40)
        self.b1.grid(row=1, column=0, sticky="nsew", pady=10, padx=100)

        self.b2 = ctk.CTkButton(self, text="Reservas",command=self.janela_reservas, height=40)
        self.b2.grid(row=2, column=0, sticky="nsew", pady=10, padx=100)

        self.b3 = ctk.CTkButton(self, text="Veículos", command=self.janela_veiculos, height=40)
        self.b3.grid(row=3, column=0, sticky="nsew", pady=10, padx=100)

        self.b4 = ctk.CTkButton(self, text="Clientes",command=self.janela_clientes, height=40)
        self.b4.grid(row=4, column=0, sticky="nsew", pady=10, padx=100)

        self.b5 = ctk.CTkButton(self, text="Formas de Pagamento",command=self.janela_formas_pagamento, height=40)
        self.b5.grid(row=5, column=0, sticky="nsew", pady=10, padx=100)

        self.b6 = ctk.CTkButton(self, text="Utilizadores",command=self.janela_utilizadores, height=40)
        self.b6.grid(row=6, column=0, sticky="nsew", pady=10, padx=100)


    def janela_veiculos(self):

        self.iconify() # Minimiza a janela principal
        self.after(10, self._create_veiculos_window_and_alerts)

    def _create_veiculos_window_and_alerts(self):
        
        self.veiculos_window = JanelaVeiculos(self)
        self.veiculos_window.grab_set()    
        
    def janela_clientes(self):  
        self.clientes_window = JanelaClientes(self) 
        self.clientes_window.grab_set() 
        self.iconify()  

    def janela_reservas(self):  
        self.reservas_window = JanelaReservas(self) 
        self.reservas_window.grab_set() 
        self.iconify()   

    def janela_formas_pagamento(self):  
        self.pagamento_window = JanelaFormasPagamento(self) 
        self.pagamento_window.grab_set() 
        self.iconify()  

    def janela_dashboard(self):  
        self.dashboard_window = JanelaDashboard(self) 
        self.dashboard_window.grab_set() 
        self.iconify() 

    def janela_utilizadores(self):  
        self.utilizadores_window = JanelaUtilizadores(self) 
        self.utilizadores_window.grab_set() 
        self.iconify()


if __name__ == "__main__":
   
# Cria e corre a janela de login em 1ºlugar

    login_app = LoginWindow()
    login_app.mainloop()

# Se login ok, corre a janela principal

if login_app.login_successful:
    app =Mainwindow()
    app.mainloop()
    