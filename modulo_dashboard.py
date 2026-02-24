# Importar as librarias necessárias

import tkinter as tk
from tkinter import ttk, Scrollbar, VERTICAL, BOTH, RIGHT, Y, W, CENTER, END, messagebox, filedialog
import customtkinter as ctk
import sqlite3
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter, DayLocator


# Importar as janelas secundarias (top level windows) de cada modulo por classes

from modulo_veiculos import JanelaVeiculos
from modulo_clientes import JanelaClientes
from modulo_reservas import JanelaReservas
from modulo_pagamentos import JanelaFormasPagamento
from modulo_utilizadores import JanelaUtilizadores


# Configuração custom tkinter

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


#Configuração do Banco de Dados

DATABASE_NAME = os.path.join("database", "BD_Frota.db")

def get_data_from_db_universal(query):
    
    conn = None
    try:
        # Garante que o diretório 'database' existe, mesmo que o DB já exista
        os.makedirs(os.path.dirname(DATABASE_NAME), exist_ok=True)
        conn = sqlite3.connect(DATABASE_NAME)
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Erro ao buscar dados da base de dados: {e}")
        messagebox.showerror("Erro de Banco de Dados", f"Não foi possível conectar ou consultar o banco de dados: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()


# Definição da janela principal em CustomTkinter 

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("App Gestão Luxury Wheels")
        self.geometry("500x500")
        self.resizable(True, True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3,4,5,6), weight=1) # Permite que os botões se expandam

        self.mylabel = ctk.CTkLabel(self, text="Escolha o Módulo", font=ctk.CTkFont(size=20, weight="bold"))
        self.mylabel.grid(row=0, column=0, pady=20)


# Definição dos Widgets da janela principal: 

        self.mylabel = ctk.CTkLabel(self, text="Escolha o Módulo", font=ctk.CTkFont(size=20, weight="bold"))
        self.mylabel.grid(row=0, column=0, pady=20)

        self.b1 = ctk.CTkButton(self, text="Dashboard",command=self.janela_dashboard, height=40)
        self.b1.grid(row=1, column=0, sticky="nsew", pady=10, padx=100)

        self.b2 = ctk.CTkButton(self, text="Reservas", height=40)
        self.b2.grid(row=2, column=0, sticky="nsew", pady=10, padx=100)

        self.b3 = ctk.CTkButton(self, text="Veículos", height=40)
        self.b3.grid(row=3, column=0, sticky="nsew", pady=10, padx=100)

        self.b4 = ctk.CTkButton(self, text="Clientes", height=40)
        self.b4.grid(row=4, column=0, sticky="nsew", pady=10, padx=100)

        self.b5 = ctk.CTkButton(self, text="Formas de Pagamento", height=40)
        self.b5.grid(row=5, column=0, sticky="nsew", pady=10, padx=100)

        self.b6 = ctk.CTkButton(self, text="Utilizadores", height=40)
        self.b6.grid(row=6, column=0, sticky="nsew", pady=10, padx=100)


# Funções auxiliares para abrir janelas dos módulos

    def open_veiculos_window(self):
        self.iconify() # Minimiza a janela principal
        window = JanelaVeiculos(self)
        window.grab_set()

    def open_clientes_window(self):
        self.iconify()
        window = JanelaClientes(self)
        window.grab_set()

    def open_reservas_window(self):
        self.iconify()
        window = JanelaReservas(self)
        window.grab_set()

    def open_pagamentos_window(self):
        self.iconify()
        window = JanelaFormasPagamento(self)
        window.grab_set()

    def open_utilizadores_window(self):
        self.iconify()
        window = JanelaUtilizadores(self)
        window.grab_set()

    def janela_dashboard(self):
        self.dashboard_window = JanelaDashboard(self)
        self.dashboard_window.grab_set() # Torna a janela do dashboard modal
        self.iconify() # Minimiza a janela principal


# Definição da janela secundária Dashboard

class JanelaDashboard(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Dashboard")
        self.geometry("1400x850") # Aumentado para acomodar 6 gráficos
        self.resizable(True, True)
        self.parent = parent # Referência à janela principal

        # Aplicar um fundo cinza claro quase branco a toda a janela
        self.configure(fg_color="#F0F0F0") # Light grey, almost white

        # Configurar a única coluna e linha para preencher toda a janela
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Frame de Conteúdo Principal 
        self.main_content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent") 
        self.main_content_frame.grid(row=0, column=0, sticky="nsew")
        
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.main_content_frame.grid_rowconfigure(0, weight=0) 
        self.main_content_frame.grid_rowconfigure(1, weight=1) 

        # Frame para o cabeçalho (botão Menu e métricas)
        self.header_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1) # 4 columas: Menu button + 3 kpis

        # Botão para voltar ao Menu Principal
        self.back_button = ctk.CTkButton(self.header_frame, text="Menu", command=self.menu,
                                         fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.back_button.grid(row=0, column=0, sticky="w") # Posicionado à esquerda

        # Frame scrollable para os gráficos
        self.scrollable_content_frame = ctk.CTkScrollableFrame(self.main_content_frame, fg_color="transparent")
        self.scrollable_content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=0)
        
        # Configurar a grade para 3x2 gráficos dentro da scrollable_content_frame
        self.scrollable_content_frame.grid_columnconfigure((0, 1), weight=1)

        # Cada gráfico + título ocupa 2 linhas na grid, então 3 pares de linhas para 6 gráficos
        self.scrollable_content_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1) 

        self.display_dashboard_content() # Carregar o dashboard por padrão

        self.protocol("WM_DELETE_WINDOW", self.sair) 

    def clear_content_frame(self, frame):
        """Limpa todos os widgets de uma frame específica."""
        for widget in frame.winfo_children():
            widget.destroy()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Muda o modo de aparência da aplicação e recarrega os gráficos."""
        ctk.set_appearance_mode(new_appearance_mode)
        self.display_dashboard_content() # Recarregar para aplicar o tema aos gráficos

    def apply_theme_to_plot(self, fig, ax):
        """Aplica as cores do tema CustomTkinter aos gráficos Matplotlib."""
        current_mode = ctk.get_appearance_mode().lower()

        # Aplicar fundo cinza claro quase branco aos gráficos
        bg_color = "#F0F0F0" 
        text_color = 'black' if current_mode == "light" else 'white'

        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)

        for spine in ax.spines.values():
            spine.set_edgecolor(text_color)

        ax.tick_params(axis='x', colors=text_color)
        ax.tick_params(axis='y', colors=text_color)
        
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)
        ax.title.set_color(text_color)
        
        if ax.xaxis.grid:
            ax.xaxis.grid(color='gray', linestyle='--', alpha=0.5)
        if ax.yaxis.grid:
            ax.yaxis.grid(color='gray', linestyle='--', alpha=0.5)


        # Configuração do texto
        for text_obj in ax.texts:
            text_obj.set_color(text_color)

        if hasattr(ax, 'patches'): # Check para pie chart
            for text_obj in ax.texts: 
                text_obj.set_color(text_color)

    def create_and_display_plot(self, parent_frame, plot_func, title, row, col):
        """Função auxiliar para criar o título e o gráfico."""
        graph_title_label = ctk.CTkLabel(parent_frame, text=title,
                                         font=ctk.CTkFont(size=14, weight="bold")) # Fonte ligeiramente menor
        graph_title_label.grid(row=row, column=col, padx=10, pady=(15, 0), sticky="w") # Ajustar padding

        # O gráfico será colocado na linha seguinte, mas dentro do mesmo par de linhas lógicas (row*2, row*2+1)
        plot_func(parent_frame, row + 1, col)


# Funções de Criação de Gráficos 


    def plot_clientes_registados_por_mes(self, parent_frame, row_num, col_num): 

    # Clientes registados por mês desde o início do ano (Line Chart)
    
        query = """
        SELECT STRFTIME('%Y-%m', data_registo) AS mes_registo,
               COUNT(id_cliente) AS total_clientes
        FROM clientes
        WHERE STRFTIME('%Y', data_registo) = STRFTIME('%Y', 'now')
        GROUP BY mes_registo
        ORDER BY mes_registo ASC
        """
        df_clients_per_month = get_data_from_db_universal(query)

        if not df_clients_per_month.empty:
            month_names = {
                '01': 'Jan', '02': 'Fev', '03': 'Mar', '04': 'Abr', 
                '05': 'Mai', '06': 'Jun', '07': 'Jul', '08': 'Ago', 
                '09': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'
            }
            df_clients_per_month['mes_label'] = df_clients_per_month['mes_registo'].apply(lambda x: month_names[x[5:7]])

            fig, ax = plt.subplots(figsize=(6, 3.5))
            ax.plot(df_clients_per_month['mes_label'], df_clients_per_month['total_clientes'], marker='o', 
                    color=ctk.get_appearance_mode().lower() == "dark" and "lightblue" or "skyblue")
            ax.set_title("Clientes Registados por Mês (Ano Atual)", fontsize=10)
            ax.set_xlabel("Mês")
            ax.set_ylabel("Número de Clientes")
            plt.xticks(rotation=45, ha="right", fontsize=8)
            plt.tight_layout()
            self.apply_theme_to_plot(fig, ax)
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=row_num, column=col_num, padx=20, pady=(0, 10), sticky="nsew")
            canvas.draw()
        else:
            no_data_label = ctk.CTkLabel(parent_frame, text="Nenhum cliente registado este ano.", font=ctk.CTkFont(size=12))
            no_data_label.grid(row=row_num, column=col_num, padx=20, pady=(0, 10), sticky="nsew")


    def plot_dinamica_veiculos_disponiveis_por_tipo_e_categoria(self, parent_frame, row_num, col_num):

      # Quantidade de veículos disponíveis por tipo e categoria (Bar Chart Agrupado)

        query = """
        SELECT tipo, categoria, COUNT(id_veiculo) AS quantidade
        FROM veiculos
        WHERE disponivel = 1
        GROUP BY tipo, categoria
        ORDER BY tipo, categoria
        """
        df_available_dynamic = get_data_from_db_universal(query)

        if not df_available_dynamic.empty:
            df_available_dynamic['label'] = df_available_dynamic['tipo'] + ' - ' + df_available_dynamic['categoria']
            
            fig, ax = plt.subplots(figsize=(6, 3.5))
            ax.bar(df_available_dynamic['label'], df_available_dynamic['quantidade'], 
                    color=plt.cm.Paired(range(len(df_available_dynamic)))) 
            
            ax.set_title("Veículos Disponíveis por Tipo e Categoria", fontsize=10)
            ax.set_xlabel("Tipo - Categoria")
            ax.set_ylabel("Quantidade")
            plt.xticks(rotation=60, ha="right", fontsize=8) 
            plt.tight_layout()
            self.apply_theme_to_plot(fig, ax)
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=row_num, column=col_num, padx=20, pady=(0, 10), sticky="nsew")
            canvas.draw()
        else:
            no_data_label = ctk.CTkLabel(parent_frame, text="Nenhum veículo disponível por tipo e categoria.", font=ctk.CTkFont(size=12))
            no_data_label.grid(row=row_num, column=col_num, padx=20, pady=(0, 10), sticky="nsew")


    def plot_reservas_mes_e_financeiro(self, parent_frame, row_num, col_num):

       # Reservas do mês e total financeiro do mês (Gráfico de Linhas Duplo)

        query = """
        SELECT STRFTIME('%Y-%m', data_inicio) AS mes,
               COUNT(id_reserva) AS total_reservas,
               SUM(preco_total) AS total_financeiro
        FROM reservas
        GROUP BY mes
        ORDER BY mes
        """
        df_monthly_data = get_data_from_db_universal(query)

        if not df_monthly_data.empty:
            month_names = {
                '01': 'Jan', '02': 'Fev', '03': 'Mar', '04': 'Abr', 
                '05': 'Mai', '06': 'Jun', '07': 'Jul', '08': 'Ago', 
                '09': 'Set', '10': 'Out', '11': 'Nov', '12': 'Dez'
            }
            df_monthly_data['mes_label'] = df_monthly_data['mes'].apply(lambda x: month_names[x[5:7]])

            fig, ax1 = plt.subplots(figsize=(6, 3.5))

            color_reservas = ctk.get_appearance_mode().lower() == "dark" and "lightgreen" or "mediumseagreen"
            color_financeiro = ctk.get_appearance_mode().lower() == "dark" and "cornflowerblue" or "royalblue"

            ax1.plot(df_monthly_data['mes_label'], df_monthly_data['total_reservas'], marker='o', color=color_reservas, label='Total de Reservas')
            ax1.set_xlabel("Mês")
            ax1.set_ylabel("Número de Reservas", color=color_reservas)
            ax1.tick_params(axis='y', labelcolor=color_reservas)

            ax2 = ax1.twinx() 
            ax2.plot(df_monthly_data['mes_label'], df_monthly_data['total_financeiro'], marker='x', linestyle='--', color=color_financeiro, label='Total Financeiro (€)')
            ax2.set_ylabel("Total Financeiro (€)", color=color_financeiro)
            ax2.tick_params(axis='y', labelcolor=color_financeiro)

            ax1.set_title("Reservas e Receita Mensal", fontsize=10)
            plt.xticks(rotation=45, ha="right", fontsize=8)
            fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9)) 
            plt.tight_layout()
            self.apply_theme_to_plot(fig, ax1) 
            self.apply_theme_to_plot(fig, ax2) 
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=row_num, column=col_num, padx=20, pady=(0, 10), sticky="nsew")
            canvas.draw()
        else:
            no_data_label = ctk.CTkLabel(parent_frame, text="Nenhum dado de reservas ou financeiro por mês.", font=ctk.CTkFont(size=12))
            no_data_label.grid(row=row_num, column=col_num, padx=20, pady=(0, 10), sticky="nsew")



    def plot_veiculos_revisao_matricula_data_scatter(self, parent_frame, row_num, col_num):

       # Gráfico de dispersão para Veículos com revisão próxima (data no X, label com matrícula)

        query = """
        SELECT matricula, proxima_data_revisao
        FROM veiculos
        WHERE proxima_data_revisao IS NOT NULL
          AND DATE(proxima_data_revisao) BETWEEN DATE('now') AND DATE('now', '+15 days')
        ORDER BY proxima_data_revisao ASC
        """
        df_revisao = get_data_from_db_universal(query)

        if not df_revisao.empty:
            df_revisao['proxima_data_revisao'] = pd.to_datetime(df_revisao['proxima_data_revisao'])
            
            fig, ax = plt.subplots(figsize=(6, 3.5))

            color_revisao = ctk.get_appearance_mode().lower() == "dark" and "indianred" or "firebrick"

            y_constant = [0] * len(df_revisao) 
            
            ax.scatter(df_revisao['proxima_data_revisao'], y_constant, 
                       marker='o', color=color_revisao, alpha=0.8, s=100) # s é o tamanho do ponto

            # Adicionar data labels com a matrícula
            text_color = 'white' if ctk.get_appearance_mode().lower() == "dark" else 'black'
            for idx, row in df_revisao.iterrows():
                # Ajustar a posição vertical do label para evitar sobreposição se houver muitos pontos
                # Aumentamos o offset y ligeiramente para cada ponto, criando uma "escadinha"
                ax.annotate(row['matricula'], (row['proxima_data_revisao'], y_constant[idx]),
                            textcoords="offset points", xytext=(5, 5 + idx * 5), ha='left', va='center',
                            fontsize=7, color=text_color, clip_on=True)

            ax.set_title("Revisões Próximas por Veículo (15 Dias)", fontsize=10)
            ax.set_xlabel("Data da Revisão")
            
            # Remover eixo Y
            ax.set_yticks([]) # Remove os ticks do eixo Y
            ax.set_ylabel("") # Remove o label do eixo Y
            
            # Formatar o eixo X para mostrar datas
            ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(DayLocator(interval=2)) # Ticks a cada 2 dias para clareza
            
            # Ajustar limites do eixo X para os próximos 15 dias
            start_date = datetime.datetime.now()
            end_date = start_date + datetime.timedelta(days=15)
            ax.set_xlim(start_date, end_date)

            plt.xticks(rotation=45, ha="right", fontsize=8)
            plt.tight_layout()
            self.apply_theme_to_plot(fig, ax)
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=row_num, column=col_num, padx=20, pady=(0, 10), sticky="nsew")
            canvas.draw()
        else:
            no_data_label = ctk.CTkLabel(parent_frame, text="Nenhum veículo com revisão nos próximos 15 dias.", font=ctk.CTkFont(size=12))
            no_data_label.grid(row=row_num, column=col_num, padx=20, pady=(0, 10), sticky="nsew")


    def plot_veiculos_inspecao_matricula_data_scatter(self, parent_frame, row_num, col_num):

        # Gráfico de dispersão para Veículos com inspeção próxima (data no X, label com matrícula).

        query = """
        SELECT matricula, proxima_data_inspecao
        FROM veiculos
        WHERE proxima_data_inspecao IS NOT NULL
          AND DATE(proxima_data_inspecao) BETWEEN DATE('now') AND DATE('now', '+15 days')
        ORDER BY proxima_data_inspecao ASC
        """
        df_inspecao = get_data_from_db_universal(query)

        if not df_inspecao.empty:
            df_inspecao['proxima_data_inspecao'] = pd.to_datetime(df_inspecao['proxima_data_inspecao'])

            fig, ax = plt.subplots(figsize=(6, 3.5))

            color_inspecao = ctk.get_appearance_mode().lower() == "dark" and "darkorange" or "orange"

           
            y_constant = [0] * len(df_inspecao) 

            ax.scatter(df_inspecao['proxima_data_inspecao'], y_constant, 
                       marker='o', color=color_inspecao, alpha=0.8, s=100) # s é o tamanho do ponto

            # Adicionar data labels com a matrícula
            text_color = 'white' if ctk.get_appearance_mode().lower() == "dark" else 'black'
            for idx, row in df_inspecao.iterrows():
                ax.annotate(row['matricula'], (row['proxima_data_inspecao'], y_constant[idx]),
                            textcoords="offset points", xytext=(5, 5 + idx * 5), ha='left', va='center',
                            fontsize=7, color=text_color, clip_on=True)
            
            ax.set_title("Inspeções Próximas por Veículo (15 Dias)", fontsize=10)
            ax.set_xlabel("Data da Inspeção")
            
            # Remover eixo Y
            ax.set_yticks([]) # Remove os ticks do eixo Y
            ax.set_ylabel("") # Remove o label do eixo Y

            # Formatar o eixo X para mostrar datas
            ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(DayLocator(interval=2)) # Ticks a cada 2 dias para clareza

            # Ajustar limites do eixo X para os próximos 15 dias
            start_date = datetime.datetime.now()
            end_date = start_date + datetime.timedelta(days=15)
            ax.set_xlim(start_date, end_date)
            
            plt.xticks(rotation=45, ha="right", fontsize=8) 
            plt.tight_layout()
            self.apply_theme_to_plot(fig, ax)
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=row_num, column=col_num, padx=20, pady=(0, 10), sticky="nsew")
            canvas.draw()
        else:
            no_data_label = ctk.CTkLabel(parent_frame, text="Nenhum veículo com inspeção nos próximos 15 dias.", font=ctk.CTkFont(size=12))
            no_data_label.grid(row=row_num, column=col_num, padx=20, pady=(0, 10), sticky="nsew")


    def plot_veiculos_atualmente_alugados(self, parent_frame, row_num, col_col):

        # Veículos atualmente alugados e dias restantes (Tabela)

        query = """
        SELECT v.marca, v.modelo,
               CAST(JULIANDAY(r.data_fim) - JULIANDAY('now') AS INTEGER) AS dias_restantes,
               r.preco_total AS valor_total_reserva -- Adicionando a coluna preco_total
        FROM reservas r
        JOIN veiculos v ON r.id_veiculo = v.id_veiculo
        WHERE DATE(r.data_fim) > DATE('now') AND DATE(r.data_inicio) <= DATE('now')
        ORDER BY dias_restantes ASC
        """
        df_rented_vehicles = get_data_from_db_universal(query)

        table_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        table_frame.grid(row=row_num, column=col_col, padx=20, pady=(0, 10), sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        if not df_rented_vehicles.empty:
            # Adicionar 'Marca' e 'Valor Total' à lista de colunas do Treeview
            tree = ttk.Treeview(table_frame, columns=("Marca", "Modelo", "Dias Restantes", "Valor Total (€)"), show="headings", height=5)
            
            # Definir os cabeçalhos das novas colunas
            tree.heading("Marca", text="Marca", anchor=CENTER)
            tree.heading("Modelo", text="Modelo", anchor=CENTER)
            tree.heading("Dias Restantes", text="Dias Restantes", anchor=CENTER)
            tree.heading("Valor Total (€)", text="Valor Total (€)", anchor=CENTER) # Novo cabeçalho
            
            # Definir larguras das colunas
            tree.column("Marca", width=80, anchor=CENTER)
            tree.column("Modelo", width=120, anchor=CENTER)
            tree.column("Dias Restantes", width=100, anchor=CENTER)
            tree.column("Valor Total (€)", width=100, anchor=CENTER) # Nova largura

            style = ttk.Style()
            current_mode = ctk.get_appearance_mode().lower()
            if current_mode == "dark":
                style.theme_use("clam")
                style.configure("Treeview", 
                                background="#2B2B2B", 
                                foreground="white", 
                                fieldbackground="#2B2B2B",
                                borderwidth=0)
                style.map("Treeview", 
                          background=[('selected', '#5B84B1')])
                style.configure("Treeview.Heading", 
                                background="#343638", 
                                foreground="white")
            else:
                style.theme_use("default")
                style.configure("Treeview", 
                                background="white", 
                                foreground="black", 
                                fieldbackground="white",
                                borderwidth=0)
                style.map("Treeview", 
                          background=[('selected', '#C9D6DF')])
                style.configure("Treeview.Heading", 
                                background="#E0E0E0", 
                                foreground="black")

            for index, row_data in df_rented_vehicles.iterrows():

                # Inserir os valores para as novas colunas, incluindo o 'valor_total_reserva'
                tree.insert("", END, values=(row_data['marca'], row_data['modelo'], row_data['dias_restantes'], f"{row_data['valor_total_reserva']:.2f}"))
            
            tree.pack(fill="both", expand=True, padx=5, pady=5)
        else:
            no_data_label = ctk.CTkLabel(table_frame, text="Nenhum veículo atualmente alugado.", font=ctk.CTkFont(size=12))
            no_data_label.pack(expand=True, fill="both", padx=5, pady=5)


    def display_dashboard_content(self):

        # Carrega e exibe os gráficos e métricas no dashboard.

        self.clear_content_frame(self.header_frame)
        self.clear_content_frame(self.scrollable_content_frame)

        self.back_button = ctk.CTkButton(self.header_frame, text="Menu", command=self.menu,
                                         fg_color="#eeb752", text_color="black", hover_color="#d4a347")
        self.back_button.grid(row=0, column=0, sticky="w")

        total_vehicles_df = get_data_from_db_universal("SELECT COUNT(id_veiculo) FROM veiculos")
        total_clients_df = get_data_from_db_universal("SELECT COUNT(id_cliente) FROM clientes")
        total_reservations_df = get_data_from_db_universal("SELECT COUNT(id_reserva) FROM reservas")

        total_vehicles = total_vehicles_df.iloc[0, 0] if not total_vehicles_df.empty else 0
        total_clients = total_clients_df.iloc[0, 0] if not total_clients_df.empty else 0
        total_reservations = total_reservations_df.iloc[0, 0] if not total_reservations_df.empty else 0

        metric_label_1 = ctk.CTkLabel(self.header_frame, text=f"Total de Veículos: {total_vehicles}", font=ctk.CTkFont(size=16, weight="bold"))
        metric_label_1.grid(row=0, column=1, padx=(50, 10), pady=0, sticky="w")

        metric_label_2 = ctk.CTkLabel(self.header_frame, text=f"Total de Clientes: {total_clients}", font=ctk.CTkFont(size=16, weight="bold"))
        metric_label_2.grid(row=0, column=2, padx=10, pady=0, sticky="w")

        metric_label_3 = ctk.CTkLabel(self.header_frame, text=f"Total de Reservas: {total_reservations}", font=ctk.CTkFont(size=16, weight="bold"))
        metric_label_3.grid(row=0, column=3, padx=10, pady=0, sticky="w")


# Exibir Gráficos 

        self.create_and_display_plot(self.scrollable_content_frame, self.plot_clientes_registados_por_mes, "Clientes Registados por Mês", 0, 0)
        self.create_and_display_plot(self.scrollable_content_frame, self.plot_dinamica_veiculos_disponiveis_por_tipo_e_categoria, "Veículos Disponíveis (Tipo/Categoria)", 0, 1)
        
        self.create_and_display_plot(self.scrollable_content_frame, self.plot_reservas_mes_e_financeiro, "Reservas e Receita Mensal", 2, 0)
        
        # Novas chamadas para os gráficos de dispersão com labels de matrícula
        self.create_and_display_plot(self.scrollable_content_frame, self.plot_veiculos_revisao_matricula_data_scatter, "Revisões Próximas por Veículo (15 Dias)", 2, 1)

        self.create_and_display_plot(self.scrollable_content_frame, self.plot_veiculos_inspecao_matricula_data_scatter, "Inspeções Próximas por Veículo (15 Dias)", 4, 0)
        self.create_and_display_plot(self.scrollable_content_frame, self.plot_veiculos_atualmente_alugados, "Veículos Atualmente Alugados", 4, 1)


    def menu(self):
        """Volta à janela principal e fecha a janela do dashboard."""
        self.parent.deiconify()
        self.destroy()

    def sair(self):
        """Fecha a aplicação completamente."""
        self.parent.destroy()
        self.destroy()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()