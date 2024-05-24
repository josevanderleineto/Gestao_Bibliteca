import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Conectar ao banco de dados SQLite ou criá-lo se não existir
conn = sqlite3.connect('dados_sibi.db')
cursor = conn.cursor()

# Verificar se a tabela já existe, se não, criar uma nova
cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (
                    mes TEXT PRIMARY KEY,
                    ebsco REAL,
                    capes REAL,
                    pergumum REAL,
                    minha_biblioteca REAL,
                    total_mensal REAL
                )''')

# Função para inserir dados no banco de dados
def inserir_dados(mes, ebsco, capes, pergumum, minha_biblioteca, total_mensal):
    cursor.execute('''INSERT OR REPLACE INTO gastos (mes, ebsco, capes, pergumum, minha_biblioteca, total_mensal)
                      VALUES (?, ?, ?, ?, ?, ?)''', (mes, ebsco, capes, pergumum, minha_biblioteca, total_mensal))
    conn.commit()

# Carregar os dados do banco de dados SQLite
def carregar_dados():
    cursor.execute("SELECT * FROM gastos")
    data = cursor.fetchall()
    return data

# Carregar os dados
data = carregar_dados()

# Se não houver dados no banco de dados, inserir os dados iniciais
if not data:
    cursor.executemany('''INSERT INTO gastos (mes, ebsco, capes, pergumum, minha_biblioteca, total_mensal)
                           VALUES (?, ?, ?, ?, ?, ?)''', [
                               ("Janeiro", 5000, 800, 2000, 1100, 8900),
                               ("Fevereiro", 1000, 800, 2000, 1100, 4900),
                               ("Março", 1000, 810, 2500, 1100, 5410),
                               ("Abril", 1000, 1000, 0, 0, 2000),
                               ("Maio", 0, 0, 0, 0, 0),
                               ("Junho", 0, 0, 0, 0, 0),
                               ("Julho", 0, 0, 0, 0, 0),
                               ("Agosto", 0, 0, 0, 0, 0),
                               ("Setembro", 0, 0, 0, 0, 0),
                               ("Outubro", 0, 0, 0, 0, 0),
                               ("Novembro", 0, 0, 0, 0, 0),
                               ("Dezembro", 0, 0, 0, 0, 0)
                           ])
    conn.commit()

# Criar o formulário para permitir ao usuário inserir novos dados
st.write("### Insira Novos Dados:")
meses_disponiveis = [m[0] for m in data]
mes = st.selectbox("Mês:", options=meses_disponiveis)
ebsco = st.number_input("EBSCO (R$):", value=0)
capes = st.number_input("CAPES (R$):", value=0)
pergumum = st.number_input("Pergamum (R$):", value=0)
minha_biblioteca = st.number_input("Minha Biblioteca (R$):", value=0)
total_mensal = ebsco + capes + pergumum + minha_biblioteca

if st.button("Inserir Dados"):
    inserir_dados(mes, ebsco, capes, pergumum, minha_biblioteca, total_mensal)
    st.success("Dados inseridos com sucesso!")

# Exibir os dados
df = pd.DataFrame(data, columns=["Mês", "EBSCO (R$)", "CAPES (R$)", "Pergamum (R$)", "Minha Biblioteca (R$)", "Total Mensal (R$)"])
df.set_index("Mês", inplace=True)

# Gráfico de barras
st.write("### Gastos do SIBI UniFTC:")
st.bar_chart(df)

# Gráfico de pizza
st.write("### Total por Serviço:")
fig, ax = plt.subplots()
ax.pie(df.iloc[:, :4].sum(), labels=df.columns[:4], autopct='%1.1f%%')
st.pyplot(fig)

# Gráfico de linha
st.write("### Total Mensal:")
st.line_chart(df["Total Mensal (R$)"])
