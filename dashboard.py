import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# Função para carregar os dados do banco de dados
def carregar_dados():
    conn = sqlite3.connect('contratos.db')
    df = pd.read_sql_query("SELECT * FROM contratos", conn)
    conn.close()
    return df

# Função para criar o banco de dados SQLite e definir a tabela
def criar_banco_dados():
    conn = sqlite3.connect('contratos.db')
    cursor = conn.cursor()

    # Definir o schema da tabela
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS contratos (
        Empresa TEXT,
        Data_de_Vencimento TEXT,
        Quantidade_de_Licencas INTEGER,
        Data_de_Renovacao TEXT,
        Valor_do_Contrato INTEGER,
        Data_de_Pagamento TEXT,
        Valor_Pago INTEGER,
        Valor_a_Vencer INTEGER
    )
    '''
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

# Função para inserir os dados na tabela
def inserir_dados(empresa, data_vencimento, quantidade, data_renovacao, valor_contrato):
    conn = sqlite3.connect('contratos.db')
    cursor = conn.cursor()

    # Inserir os dados na tabela com data de pagamento como a data atual
    data_pagamento = datetime.today().strftime("%d/%m/%Y")
    cursor.execute('''
        INSERT INTO contratos (Empresa, Data_de_Vencimento, Quantidade_de_Licencas, Data_de_Renovacao, Valor_do_Contrato, Data_de_Pagamento, Valor_Pago, Valor_a_Vencer)
        VALUES (?, ?, ?, ?, ?, ?, 0, ?)
    ''', (empresa, data_vencimento, quantidade, data_renovacao, valor_contrato, data_pagamento, valor_contrato))

    conn.commit()
    conn.close()


# Função para atualizar o dashboard
def atualizar_dashboard(df):

    st.header("Tabela de Dados")
    # Adicionar uma nova coluna para indicar se o pagamento está em atraso ou não
    hoje = datetime.today().date()
    df['Em Atraso'] = df.apply(lambda row: 'Sim' if pd.to_datetime(row['Data_de_Pagamento'], errors='coerce', format='%d/%m/%Y').date() < hoje and row['Valor_Pago'] == 0 else 'Não', axis=1)
    st.write(df)

    # Gráfico 1: Evolução do Valor Pago ao Longo do Tempo (Gráfico de Linha)
    df["Data_de_Pagamento"] = pd.to_datetime(df["Data_de_Pagamento"], errors='coerce', format='%d/%m/%Y')
    fig1 = px.line(df, x="Data_de_Pagamento", y="Valor_Pago", title="Evolução do Valor Pago ao Longo do Tempo", 
                   color_discrete_sequence=["#FF6347", "#32CD32", "#1E90FF"])
    fig1.update_layout(title_font_size=22, title_font_color="#333", plot_bgcolor="#f9f9f9")

    # Gráfico 2: Valor do Contrato por Empresa (Gráfico de Barras)
    fig2 = px.bar(df, x="Empresa", y="Valor_do_Contrato", title="Valor do Contrato por Empresa", 
                  color="Empresa", color_discrete_sequence=["#FFA500", "#32CD32", "#1E90FF"])
    fig2.update_layout(title_font_size=22, title_font_color="#333", plot_bgcolor="#f9f9f9")

    # Gráfico 3: Quantidade de Licenças por Empresa (Gráfico de Colunas)
    fig3 = px.bar(df, x="Empresa", y="Quantidade_de_Licencas", title="Quantidade de Licenças por Empresa", 
                  color="Empresa", barmode="group", text_auto=True, color_discrete_sequence=["#FF1493", "#FFD700", "#00CED1"])
    fig3.update_layout(title_font_size=22, title_font_color="#333", plot_bgcolor="#f9f9f9")

    # Gráfico 4: Distribuição do Valor do Contrato (Gráfico de Pizza)
    fig4 = px.pie(df, values="Valor_do_Contrato", names="Empresa", title="Distribuição do Valor do Contrato",
                  color_discrete_sequence=["#FF4500", "#32CD32", "#1E90FF"])
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    fig4.update_layout(title_font_size=22, title_font_color="#333", plot_bgcolor="#f9f9f9")

    # Gráfico 5: Valor a Vencer por Empresa (Gráfico de Barras Horizontais)
    fig5 = px.bar(df, x="Valor_a_Vencer", y="Empresa", orientation='h', title="Valor a Vencer por Empresa", 
                  color="Empresa", color_discrete_sequence=["#32CD32", "#FF4500", "#1E90FF"])
    fig5.update_layout(title_font_size=22, title_font_color="#333", plot_bgcolor="#f9f9f9")

    # Exibir gráficos em duas colunas
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        st.plotly_chart(fig4, use_container_width=True)

    st.plotly_chart(fig5, use_container_width=True)

# Configurar a página
st.set_page_config(layout="wide")

# Criar ou carregar os dados do banco de dados
criar_banco_dados()

# Botões para inserir novos dados e apagar os dados de pagamento
st.title("Dashboard de Contratos")

st.title("Inserir Novo Contrato")

empresas_existente = carregar_dados()['Empresa'].unique()
empresa = st.selectbox("Empresa:", empresas_existente)
data_vencimento = st.date_input("Data de Vencimento:")
quantidade = st.number_input("Quantidade de Licenças:", min_value=0)
data_renovacao = st.date_input("Data de Renovação:")
valor_contrato = st.number_input("Valor do Contrato:", min_value=0)

submit_button = st.button("Inserir")

if submit_button:
    inserir_dados(empresa, data_vencimento, quantidade, data_renovacao, valor_contrato)
    st.success("Novo contrato inserido com sucesso.")
    atualizar_dashboard(carregar_dados())

# Botão para apagar os dados de pagamento
st.title("Apagar Dados de Pagamento")
apagar_button = st.button("Apagar Dados de Pagamento")

if apagar_button:
    apagar_dados_de_pagamento()

# Atualizar o dashboard no início
atualizar_dashboard(carregar_dados())
