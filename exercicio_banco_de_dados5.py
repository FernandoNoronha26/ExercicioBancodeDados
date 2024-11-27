import tkinter as tk
from tkinter import messagebox
import pyodbc

# Configuração do Banco de Dados
server = 'PCH_SD-001'  # Nome do servidor SQL Server
database = 'IMC_DB'      # Nome do banco de dados
username = 'Fernando' # Usuário do SQL Server
password = 'Fernando'   # Senha do SQL Server

# Conexão ao Banco de Dados
def conectar_banco():
    try:
        conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        return conn
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados.\nErro: {e}")
        return None

def criar_tabela():
    """Cria a tabela no banco de dados, caso ainda não exista."""
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='CalculosIMC' AND xtype='U')
            CREATE TABLE CalculosIMC (
                id INT IDENTITY PRIMARY KEY,
                nome NVARCHAR(100),
                endereco NVARCHAR(255),
                altura FLOAT,
                peso FLOAT,
                imc FLOAT,
                classificacao NVARCHAR(50),
                data_registro DATETIME DEFAULT GETDATE()
            )
        """)
        conn.commit()
        conn.close()

def salvar_no_banco(nome, endereco, altura, peso, imc, classificacao):
    """Salva os dados do cálculo no banco de dados."""
    conn = conectar_banco()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO CalculosIMC (nome, endereco, altura, peso, imc, classificacao)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, endereco, altura, peso, imc, classificacao))
        conn.commit()
        conn.close()

# Lógica da Calculadora de IMC
def calcular_imc():
    try:
        nome = entry_nome.get().strip()
        endereco = entry_endereco.get().strip()
        altura = float(entry_altura.get()) / 100  # altura em metros
        peso = float(entry_peso.get())
        imc = peso / (altura ** 2)

        # Classificação do IMC
        if imc < 18.5:
            classificacao = "Magreza"
        elif 18.5 <= imc < 24.9:
            classificacao = "Normal"
        elif 25 <= imc < 29.9:
            classificacao = "Sobrepeso"
        else:
            classificacao = "Obesidade"

        # Exibir Resultado
        resultado = f"Seu IMC é: {imc:.2f}\nClassificação: {classificacao}"
        label_resultado.config(text=resultado)

        # Salvar no Banco de Dados
        salvar_no_banco(nome, endereco, altura, peso, imc, classificacao)

    except ValueError:
        messagebox.showerror("Erro", "Insira valores válidos para altura e peso.")

def reiniciar():
    entry_nome.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    entry_altura.delete(0, tk.END)
    entry_peso.delete(0, tk.END)
    label_resultado.config(text="")

# Configuração da janela principal
root = tk.Tk()
root.title("Calculadora de IMC")
root.geometry("400x300")
root.configure(bg="#f2f2f2")  # Cor de fundo da janela

# Mensagem de boas-vindas
label_titulo = tk.Label(root, text="Calculadora de IMC", font=("Arial", 16, "bold"), bg="#f2f2f2", fg="#333")
label_titulo.grid(row=0, column=0, columnspan=3, pady=10)

# Campos de entrada
tk.Label(root, text="Nome:", font=("Arial", 10), bg="#f2f2f2").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_nome = tk.Entry(root, font=("Arial", 10), width=30)
entry_nome.grid(row=1, column=1, columnspan=2, pady=5)

tk.Label(root, text="Endereço:", font=("Arial", 10), bg="#f2f2f2").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_endereco = tk.Entry(root, font=("Arial", 10), width=30)
entry_endereco.grid(row=2, column=1, columnspan=2, pady=5)

tk.Label(root, text="Altura (cm):", font=("Arial", 10), bg="#f2f2f2").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_altura = tk.Entry(root, font=("Arial", 10), width=10)
entry_altura.grid(row=3, column=1, pady=5)

tk.Label(root, text="Peso (kg):", font=("Arial", 10), bg="#f2f2f2").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_peso = tk.Entry(root, font=("Arial", 10), width=10)
entry_peso.grid(row=4, column=1, pady=5)

# Botões
btn_calcular = tk.Button(root, text="Calcular IMC", font=("Arial", 10), command=calcular_imc, bg="#4CAF50", fg="white", width=10)
btn_calcular.grid(row=5, column=0, pady=20, padx=5)

btn_reiniciar = tk.Button(root, text="Reiniciar", font=("Arial", 10), command=reiniciar, bg="#2196F3", fg="white", width=10)
btn_reiniciar.grid(row=5, column=1, pady=20, padx=5)

btn_sair = tk.Button(root, text="Sair", font=("Arial", 10), command=root.quit, bg="#f44336", fg="white", width=10)
btn_sair.grid(row=5, column=2, pady=20, padx=5)

# Resultado
label_resultado = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#333")
label_resultado.grid(row=6, column=0, columnspan=3, pady=10)

# Configuração Inicial
criar_tabela()

root.mainloop()
