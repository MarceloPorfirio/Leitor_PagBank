from flask import Flask, render_template, request
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    # Verifica se um arquivo CSV foi enviado
    if 'file' not in request.files:
        return 'Nenhum arquivo selecionado.'
    
    # Lê o arquivo CSV usando o pandas
    file = request.files['file']
    df = pd.read_csv(file,sep=';')
    df['VALOR'] = df['VALOR'].str.replace(',','.')
    df['VALOR'] = df['VALOR'].astype(float)

    df_grouped = df.groupby(['DESCRICAO','TIPO']).sum().reset_index()

    # agrupa os dados por uma coluna e calcula a média

    positive_values = df_grouped[df_grouped['VALOR'] >= 0].round(2)
    negative_values = df_grouped[df_grouped['VALOR'] <= 0].round(2)

    columns = [ 'DESCRICAO','TIPO', 'VALOR']
    
    table1 = ff.create_table(positive_values[columns])
    table2 = ff.create_table(negative_values[columns])

    total_positive = round(positive_values['VALOR'].sum(),2)
    total_positive = f'O valor total de entradas é {total_positive}'

    total_negative = round(negative_values['VALOR'].sum(),2)
    total_negative = f'O valor total de saídas é {total_negative}'
    
    # total_negative = negative_values.sum().reset_index()
    print(total_positive)
    print(total_negative)
    
    html_str1 = table1.to_html()
    html_str2 = table2.to_html()
    
    # Exibe o DataFrame carregado na saída
    return render_template('tabelas.html',table1=html_str1,table2=html_str2,total_positive=total_positive,total_negative=total_negative )



    # if action == 'generate_graph':
        # # Verifica se um arquivo CSV foi enviado
        # if 'file' not in request.files:
        #     return 'Nenhum arquivo selecionado.'

        # file = request.files['file']

        # # Verifica se o arquivo não está vazio
        # if file.filename == '':
        #     return 'Arquivo vazio.'

@app.route('/generate_graph', methods=['POST'])
def generate_graph():
        try:
            file = request.files['file']
            
            if not file:
                return 'Nenhum arquivo selecionado ou o arquivo está vazio.'
            
            df = pd.read_csv(file, sep=';', encoding='utf-8', header=0)

            if df.empty:
                return 'O arquivo não contém dados.'

            df['VALOR'] = df['VALOR'].str.replace(',', '.').astype(float)

            df_grouped = df.groupby(['TIPO']).sum().reset_index()

            fig = px.bar(df_grouped, x='TIPO', y='VALOR', title='Gráfico de Valores por Tipo')

            graph_html = fig.to_html(full_html=False)

            return render_template('graficos.html', graph_html=graph_html)
        except pd.errors.EmptyDataError:
            return 'O arquivo não contém dados ou o formato é inválido.'




if __name__ == '__main__':
    app.run()
