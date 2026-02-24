# Importar as librarias
import tkinter as tk
from tkinter import ttk, Scrollbar, VERTICAL, BOTH, RIGHT, Y, W, CENTER, END, messagebox, filedialog
import tkinter.font as tkFont
import customtkinter as ctk
import os
from  dotenv import load_dotenv

load_dotenv()

def login():
    """
    Função para verificar as credenciais de login.
    """
    username = entry_username.get()
    password = entry_password.get()

    # BUSCA AS CREDENCIAIS - Sem valores padrão (se não houver .env, retorna None)
    admin_user = os.getenv("ADMIN_USER")
    admin_pass = os.getenv("ADMIN_PASS")

    # Verifica se as variáveis existem e se coincidem
    if admin_user and admin_pass and username == admin_user and password == admin_pass:
        messagebox.showinfo("Login", "Login bem-sucedido!")
        root.destroy()
    else:
        messagebox.showerror("Login", "Falha na autenticação.")


# Configuração da janela principal
root = tk.Tk()
root.title("Tela de Login")
root.geometry("300x150") # Define o tamanho da janela (largura x altura)
root.resizable(False, False) # Impede que o usuário redimensione a janela

# Centralizar a janela na tela
window_width = 300
window_height = 150
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Criação dos widgets (rótulos, campos de entrada, botão)

# Rótulo para o nome de usuário
label_username = tk.Label(root, text="Usuário:")
label_username.pack(pady=5) # Adiciona um espaçamento vertical

# Campo de entrada para o nome de usuário
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# Rótulo para a senha
label_password = tk.Label(root, text="Senha:")
label_password.pack(pady=5)

# Campo de entrada para a senha (mostrar asteriscos)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Botão de Login
button_login = tk.Button(root, text="Login", command=login)
button_login.pack(pady=10)

# Iniciar o loop principal da interface gráfica
root.mainloop()
