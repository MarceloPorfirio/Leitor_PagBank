from flask import Flask, render_template, request
import pandas as pd
import plotly.figure_factory as ff

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
   
    # table3 = ff.create_table(pd.DataFrame({'Total': [total_positive]}))
    # html_str3 = total_positive.to_html()
    # html_str4 = total_negative.to_html()

    # exibe a tabela com o método show() da biblioteca plotly
    
    
    # Exibe o DataFrame carregado na saída
    return render_template('tabelas.html',table1=html_str1,table2=html_str2,total_positive=total_positive,total_negative=total_negative )

# @app.route('/upload_neg', methods=['POST'])
# def upload_negativo():
#     # Verifica se um arquivo CSV foi enviado
#     if 'file' not in request.files:
#         return 'Nenhum arquivo selecionado.'
    
#     # Lê o arquivo CSV usando o pandas
#     file = request.files['file']
#     df = pd.read_csv(file,sep=';')
#     df['VALOR'] = df['VALOR'].str.replace(',','.')
#     df['VALOR'] = df['VALOR'].astype(float)

#     df_grouped = df.groupby(['DESCRICAO','TIPO']).sum().reset_index()

#     # agrupa os dados por uma coluna e calcula a média
#     positive_values = df_grouped[df_grouped['VALOR'] <= 0].round(2)
#     columns = [ 'DESCRICAO','TIPO', 'VALOR']
#     table = ff.create_table(positive_values[columns])
    

#     # exibe a tabela com o método show() da biblioteca plotly
    
    
#     # Exibe o DataFrame carregado na saída
#     return table.to_html()
    

if __name__ == '__main__':
    app.run()
