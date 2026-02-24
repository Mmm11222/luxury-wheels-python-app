# Importar as librarias necessárias

import tkinter as tk
from tkinter import ttk, Scrollbar, VERTICAL, BOTH, RIGHT, Y, W, CENTER, END, messagebox, filedialog
import tkinter.font as tkFont
import customtkinter as ctk
import os
import datetime
import sqlite3
import pandas as pd 


# Funções auxiliares de conversão de dados

def _validate_int_input(value_str, field_name):
  
    if not value_str:
        return None 
    try:
        return int(value_str)
    except ValueError:
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' deve ser um número inteiro válido.")
        return None


def _validate_float_input(value_str, field_name):
    """Valida se a string pode ser convertida para um número decimal (float)."""
    if not value_str:
        return None 
    try:
        return float(value_str)
    except ValueError:
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' deve ser um número decimal válido (ex: 123.45).")
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


def _validate_datetime_input(datetime_str, field_name):
    """Valida se a string da data/hora está no formato YYYY-MM-DD HH:MM:SS."""
    if not datetime_str:
        return None
    try:
        datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return datetime_str
    except ValueError:
        messagebox.showerror("Erro de Validação", f"O campo '{field_name}' deve estar no formato YYYY-MM-DD HH:MM:SS.")
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

        self.b5 = ctk.CTkButton(self, text="Formas de Pagamento",command=self.janela_formas_pagamento, height=40)
        self.b5.grid(row=5, column=0, sticky="nsew", pady=10, padx=100)

        self.b6 = ctk.CTkButton(self, text="Utilizadores", height=40)
        self.b6.grid(row=6, column=0, sticky="nsew", pady=10, padx=100)



    def janela_formas_pagamento(self):
        self.janela_formas_pagamento_window = JanelaFormasPagamento(self)
        self.janela_formas_pagamento_window.grab_set()
        self.iconify()

# Definição da janela secundária Pagamentos

class JanelaFormasPagamento(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Módulo Formas de Pagamento")
        self.geometry("1000x700")
        self.resizable(True, True)


 # Permitir a expansão das colunas e linhas da janela  

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Treeview frame
        self.grid_rowconfigure(1, weight=0) # Search frame
        self.grid_rowconfigure(2, weight=0) # Data entry frame
        self.grid_rowconfigure(3, weight=0) # Action buttons frame
        self.grid_rowconfigure(4, weight=0) # Export buttons frame

        self.protocol("WM_DELETE_WINDOW", self.sair)


# Configuração  do estilo da janela pagamentos

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

 
# Definição dos Widgets da janela pagamentos:

# Definição da Treeview -  Frame       

        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        self.tree_scrollbar= Scrollbar(self.tree_frame, orient=VERTICAL)
        self.tree_scrollbar.pack(side=RIGHT, fill=Y)

        self.my_tree= ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scrollbar.set, show="headings")
        self.my_tree.pack(pady=10, fill=BOTH, expand=True)
        self.tree_scrollbar.config(command=self.my_tree.yview)

        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="#D9F3FB")


# Definição das colunas da Treeview para pagamentos
        
        self.my_tree["columns"] = ("ID_Forma_Pagamento","Tipo","Detalhes")

        
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.column("ID_Forma_Pagamento", anchor=CENTER, width=200)
        self.my_tree.heading("ID_Forma_Pagamento", text="ID Forma Pgto.")
        self.my_tree.column("Tipo", anchor=W, width=300)
        self.my_tree.heading("Tipo", text="Tipo")
        self.my_tree.column("Detalhes", anchor=W, width=300)
        self.my_tree.heading("Detalhes", text="Detalhes")


 # Definição do campo pesquisar 

        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(fill='x', expand='yes', padx=20, pady=10)
        self.search_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.search_label = ctk.CTkLabel(self.search_frame, text="Pesquisar por:", font=ctk.CTkFont(weight="bold"))
        self.search_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self.search_frame, textvariable=self.search_var, width=100)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.search_button = ctk.CTkButton(self.search_frame, text="Pesquisar", font=ctk.CTkFont(weight="bold"), command=self.search_database,
                                              fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        self.search_options_label= ctk.CTkLabel(self.search_frame, text="Opções de Pesquisa:", font=ctk.CTkFont(weight="bold"))
        self.search_options_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        self.search_option_var = ctk.StringVar(value="ID_Forma_Pagamento") 

        self.search_option_id = ctk.CTkRadioButton(self.search_frame, text="ID Forma Pgto.", variable=self.search_option_var, value="ID_Forma_Pagamento")
        self.search_option_id.grid(row=1, column=1, padx=10, pady=2, sticky="ew")

        self.search_option_tipo = ctk.CTkRadioButton(self.search_frame, text="Tipo", variable=self.search_option_var, value="Tipo")
        self.search_option_tipo.grid(row=1, column=2, padx=10, pady=2, sticky="ew")

        self.search_option_detalhes = ctk.CTkRadioButton(self.search_frame, text="Detalhes", variable=self.search_option_var, value="Detalhes")
        self.search_option_detalhes.grid(row=1, column=3, padx=10, pady=2, sticky="ew")


# Definição do campo dados

        self.data_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.data_frame.pack(fill='x', expand='yes', padx=20, pady=10)
        self.data_frame.grid_columnconfigure((0, 1, 2, 3), weight=1) 

        # Linha 0 de entradas
        self.label1 = ctk.CTkLabel(self.data_frame, text="ID_Forma_Pagamento")
        self.label1.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.entry1 = ctk.CTkEntry(self.data_frame, width=80, state='readonly')
        self.entry1.grid(row=0, column=1, padx=2, pady=2, sticky="ew")

        self.label2 = ctk.CTkLabel(self.data_frame, text="Tipo")
        self.label2.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.entry2 = ctk.CTkEntry(self.data_frame, width=300)
        self.entry2.grid(row=0, column=3, padx=2, pady=2, sticky="ew")

        # Linha 1 de entradas
        self.label3 = ctk.CTkLabel(self.data_frame, text="Detalhes")
        self.label3.grid(row=1, column=0, padx=2, pady=2, sticky=W)
        self.entry3 = ctk.CTkEntry(self.data_frame, width=300)
        self.entry3.grid(row=1, column=1, padx=2, pady=2, sticky="ew")


# Definição do campo registos (botões) 

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(fill='x', expand='yes', padx=20, pady=10)
        self.button_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.button1 = ctk.CTkButton(self.button_frame, text="Listar", command=self.listar,
                                        fg_color="#eeb752", text_color="black", font=ctk.CTkFont(weight="bold"), hover_color="#d4a347")
        self.button1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.button2 = ctk.CTkButton(self.button_frame, text="Adicionar", font=ctk.CTkFont(weight="bold"), command=self.adicionar,
                                        fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.button3 = ctk.CTkButton(self.button_frame, text="Remover", font=ctk.CTkFont(weight="bold"), command=self.remover,
                                        fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button3.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.button4 = ctk.CTkButton(self.button_frame, text="Editar", font=ctk.CTkFont(weight="bold"), command=self.editar,
                                        fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button4.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        self.button5 = ctk.CTkButton(self.button_frame, text="Menu", font=ctk.CTkFont(weight="bold"), command=self.menu,
                                        fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button5.grid(row=0, column=4, padx=10, pady=10, sticky="ew")

        self.button6 = ctk.CTkButton(self.button_frame, text="Sair", font=ctk.CTkFont(weight="bold"), command=self.sair,
                                        fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.button6.grid(row=0, column=5, padx=10, pady=10, sticky="ew")


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
            cur.execute("SELECT id_forma_pagamento, tipo, Detalhes FROM formas_pagamento ORDER BY id_forma_pagamento ASC")
            rows = cur.fetchall()

            for i, row in enumerate(rows):
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                self.my_tree.insert("", END, values=row, tags=tags)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao aceder à base de dados de formas de pagamento: {e}")
        finally:
            if conn:
                conn.close()


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

            if search_option == "ID_Forma_Pagamento":
                try:
                    search_value = int(search_term)
                    query = "SELECT id_forma_pagamento, tipo, detalhes FROM formas_pagamento WHERE id_forma_pagamento = ?"
                    search_param = (search_value,)
                except ValueError:
                    messagebox.showerror("Erro de Pesquisa", "Por favor, insira um número inteiro válido para o ID.")
                    self.listar()
                    return
    
            elif search_option == "Tipo":
                query = "SELECT id_forma_pagamento, tipo, Detalhes FROM formas_pagamento WHERE tipo LIKE ?"
                search_param = (f"%{search_term}%",)

            elif search_option == "Detalhes":
                query = "SELECT id_forma_pagamento, tipo, detalhes FROM formas_pagamento WHERE detalhes LIKE ?"
                search_param = (f"%{search_term}%",)

            else:
                messagebox.showinfo("Informação", "Selecione uma opção de pesquisa válida.")
                return

            cur.execute(query, search_param)
            rows = cur.fetchall()

            if not rows:
                messagebox.showinfo("Pesquisa", "Nenhuma forma de pagamento encontrada com os critérios fornecidos.")

            for i, row in enumerate(rows):
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                self.my_tree.insert("", END, values=row, tags=tags)

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao pesquisar formas de pagamento: {e}")
        finally:
            if conn:
                conn.close()


    def aceder_registo(self, event):
        
        try:
            selected_item = self.my_tree.focus()
            if not selected_item:
                return

            values = self.my_tree.item(selected_item, 'values')
            if not values:
                return

            self.entry1.configure(state='normal')
            self.limpar_campos()

            self.entry1.insert(0, str(values[0])) # ID_Forma_Pagamento
            self.entry2.insert(0, values[1]) # Tipo
            self.entry3.insert(0, values[2]) # Detalhe

            self.entry1.configure(state='readonly')

        except Exception as e:
            messagebox.showerror("Erro ao Aceder Registo", f"Ocorreu um erro ao aceder ao registo: {e}")


 # Definição da função adicionar registos à base de dados 

    def adicionar(self):
        """Adds a new payment method record to the database."""
        tipo = self.entry2.get().strip()
        detalhe = self.entry3.get().strip()

        if not tipo:
            messagebox.showerror("Erro de Validação", "O Tipo é obrigatório.")
            return
        if not detalhe:
            messagebox.showerror("Erro de Validação", "O Detalhe é obrigatório.")
            return

        confirmation = messagebox.askyesno("Confirmação", f"Tem a certeza que deseja adicionar a forma de pagamento '{tipo}'?")
        if not confirmation:
            return

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()

            # Check for duplicate description
            cur.execute("SELECT 1 FROM formas_pagamento WHERE tipo = ? AND detalhes = ?", (tipo, detalhes))
            if cur.fetchone():
                messagebox.showerror("Erro", f"A forma de pagamento '{tipo}' com o detalhe '{detalhes}' já existe.")
                return

            cur.execute("INSERT INTO formas_pagamento (tipo, detalhes) VALUES (?, ?)", (tipo, detalhes))
            conn.commit()
            messagebox.showinfo("Sucesso", "Forma de pagamento adicionada com sucesso!")
            self.listar()
            self.limpar_campos()

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar a forma de pagamento: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()


# Definição da função editar que permite alterar os registos à base de dados 

    def editar(self):
   
        selected_item = self.my_tree.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione uma forma de pagamento na tabela para editar.")
            return

      
        values = self.my_tree.item(selected_item, 'values')
        if not values:
            message_box.showerror("Erro", "Não foi possível obter os detalhes do registo selecionado.")
            return

        id_forma_pagamento = values[0] 
        
        tipo = self.entry2.get().strip()
        detalhes = self.entry3.get().strip()

        if not tipo:
            messagebox.showerror("Erro de Validação", "O Tipo é obrigatório.")
            return
        if not detalhes:
            messagebox.showerror("Erro de Validação", "O Detalhe é obrigatório.")
            return

        confirmation = messagebox.askyesno("Confirmação", f"Tem a certeza que deseja editar a forma de pagamento ID {id_forma_pagamento}?")
        if not confirmation:
            return

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()


            cur.execute("SELECT 1 FROM formas_pagamento WHERE tipo = ? AND detalhes = ? AND id_forma_pagamento != ?", (tipo, detalhes, id_forma_pagamento))
            if cur.fetchone():
                messagebox.showerror("Erro", f"Já existe outra forma de pagamento com o tipo '{tipo}' e detalhe '{detalhes}'.")
                return

            cur.execute("UPDATE formas_pagamento SET tipo = ?, detalhes = ? WHERE id_forma_pagamento = ?",
                        (tipo, detalhes, id_forma_pagamento))
            conn.commit()
            if cur.rowcount > 0:
                messagebox.showinfo("Sucesso", f"Forma de pagamento ID {id_forma_pagamento} editada com sucesso!")
                self.listar()
                self.limpar_campos()
            else:
                messagebox.showinfo("Informação", "Nenhuma forma de pagamento foi atualizada. Verifique se o ID existe.")

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao editar a forma de pagamento: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()


 # Definição da função remover registos da base de dados

    def remover(self):
        """Removes a selected payment method record from the database."""
        selected_item = self.my_tree.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione uma forma de pagamento na tabela para remover.")
            return

        values = self.my_tree.item(selected_item, 'values')
        id_forma_pagamento_to_delete = values[0]

        confirmation = messagebox.askyesno("Confirmação", f"Tem a certeza que deseja remover a forma de pagamento ID {id_forma_pagamento_to_delete}?")
        if not confirmation:
            return

        conn = None
        try:
            conn = sqlite3.connect('database/BD_Frota.db')
            cur = conn.cursor()
            
            # Check for foreign key dependency in 'reservas' table
            cur.execute("SELECT 1 FROM reservas WHERE id_forma_pagamento = ?", (id_forma_pagamento_to_delete,))
            if cur.fetchone():
                messagebox.showerror("Erro", "Não é possível remover esta forma de pagamento porque está associada a uma ou mais reservas.")
                return

            cur.execute("DELETE FROM formas_pagamento WHERE id_forma_pagamento = ?", (id_forma_pagamento_to_delete,))
            if cur.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Sucesso", f"Forma de pagamento ID {id_forma_pagamento_to_delete} removida com sucesso!")
                self.listar()
                self.limpar_campos()
            else:
                messagebox.showinfo("Informação", f"Nenhuma forma de pagamento com o ID '{id_forma_pagamento_to_delete}' foi encontrada.")

        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao remover a forma de pagamento: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    def limpar_campos(self):
      
        self.entry1.configure(state='normal')
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.entry3.delete(0, tk.END)

        self.entry1.configure(state='readonly')
        self.search_var.set("") #


 # Função para exportar dados para Excel         

    def export_to_excel(self):
        
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
        
        self.master.deiconify()
        self.destroy()


# Função para sair da aplicação

    def sair(self):
        self.master.deiconify()
        self.destroy()

# Iniciar a aplicação

if __name__ == "__main__":
   
    app = MainWindow()
    app.mainloop()
