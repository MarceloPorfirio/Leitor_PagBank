import csv
import tkinter as tk
from tkinter import filedialog

# Cria a janela principal
root = tk.Tk()

# Define a função para abrir o diálogo de seleção de arquivo
def open_file_dialog():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

# Define a função para filtrar o arquivo CSV e exibir o resultado
def filter_csv():
    # Lê o conteúdo do arquivo CSV
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Cria uma lista com as linhas que contêm o termo de pesquisa
        filtered_rows = [row for row in csv_reader if search_term.get().lower() in row[field.get()].lower()]

    # Cria o widget Text e exibe as linhas filtradas
    text_widget = tk.Text(root)
    for row in filtered_rows:
        text_widget.insert(tk.END, row[field.get()] + "\n")
    text_widget.pack()

# Cria os widgets Entry e Button para inserir o termo de pesquisa e filtrar o arquivo CSV
search_term = tk.Entry(root)
search_term.pack()

field = tk.StringVar(root)
field.set("Nome")  # Define o campo padrão para filtragem
field_options = ["Nome", "Idade", "Email"]  # Opções de campo para filtragem
field_dropdown = tk.OptionMenu(root, field, *field_options)
field_dropdown.pack()

filter_button = tk.Button(root, text="Filtrar", command=filter_csv)
filter_button.pack()

# Cria o botão "Abrir arquivo"
open_button = tk.Button(root, text="Abrir arquivo", command=open_file_dialog)
open_button.pack()

# Inicia o loop da janela principal
root.mainloop()
