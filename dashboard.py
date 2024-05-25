import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import datetime

# Conectar ao banco de dados SQLite ou criá-lo se não existir
conn = sqlite3.connect('dados_sibi.db')
cursor = conn.cursor()

# Verificar se a tabela já existe, se não, criar uma nova
cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (
                    ano INTEGER,
                    mes TEXT,
                    ebsco REAL,
                    capes REAL,
                    pergumum REAL,
                    minha_biblioteca REAL,
                    total_mensal REAL,
                    PRIMARY KEY (ano, mes)
                )''')

# Função para inserir dados no banco de dados
def inserir_dados(ano, mes, ebsco, capes, pergumum, minha_biblioteca, total_mensal):
    cursor.execute('''INSERT OR REPLACE INTO gastos (ano, mes, ebsco, capes, pergumum, minha_biblioteca, total_mensal)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (ano, mes, ebsco, capes, pergumum, minha_biblioteca, total_mensal))
    conn.commit()

# Carregar os dados do banco de dados SQLite
def carregar_dados():
    cursor.execute("SELECT * FROM gastos")
    data = cursor.fetchall()
    return data

# Função para obter o ano atual
def obter_ano_atual():
    now = datetime.datetime.now()
    return now.year

# Criar o formulário para permitir ao usuário inserir novos dados
st.write("### SIBI UniFTC/Unex:")
st.write("#### Controle de Gastos:")
st.write("##### Insira Novos Dados:")
ano = st.number_input("Ano:", value=obter_ano_atual())
mes = st.selectbox("Mês:", options=["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
ebsco = st.number_input("EBSCO (R$):", value=0)
capes = st.number_input("CAPES (R$):", value=0)
pergumum = st.number_input("Pergamum (R$):", value=0)
minha_biblioteca = st.number_input("Minha Biblioteca (R$):", value=0)
total_mensal = ebsco + capes + pergumum + minha_biblioteca

if st.button("Inserir Dados"):
    inserir_dados(ano, mes, ebsco, capes, pergumum, minha_biblioteca, total_mensal)
    st.success("Dados inseridos com sucesso!")

# Carregar os dados
data = carregar_dados()

# Filtrar os dados de acordo com o ano selecionado
df = pd.DataFrame(data, columns=["Ano", "Mês", "EBSCO (R$)", "CAPES (R$)", "Pergamum (R$)", "Minha Biblioteca (R$)", "Total Mensal (R$)"])
df = df[df["Ano"] == ano]

# Exibir os dados em forma de tabela
st.write("### Tabela de Dados:")
st.write(df)

# Reorganizando o DataFrame para usar os meses como colunas e o ano como índice
pivot_df = df.pivot_table(index='Ano', columns='Mês', values='Total Mensal (R$)')

# Gráfico de barras
st.write(f"### Gastos do SIBI UniFTC - Ano {ano}:")
bar_chart = st.bar_chart(pivot_df)
plt.title(f"Gastos do SIBI UniFTC - Ano {ano}")

# Gráfico de pizza
st.write(f"### Total por Serviço - Ano {ano}:")
fig, ax = plt.subplots()
ax.pie(df.iloc[:, 2:6].sum(), labels=df.columns[2:6], autopct='%1.1f%%')
pie_chart = st.pyplot(fig)
plt.title(f"Total por Serviço - Ano {ano}")

# Reconfigurando o DataFrame para exibir o gráfico de linha corretamente
df_total_mensal = df.groupby("Mês")["Total Mensal (R$)"].sum().reset_index()

# Gráfico de linha
st.write(f"### Total Mensal - Ano {ano}:")
line_chart = st.line_chart(df_total_mensal.set_index("Mês"))
plt.title(f"Total Mensal - Ano {ano}")

# Gráfico de colunas
st.write(f"### Total Mensal por Mês - Ano {ano}:")
bar_chart_total_mensal = st.bar_chart(df_total_mensal.set_index("Mês"))
plt.title(f"Total Mensal por Mês - Ano {ano}")

