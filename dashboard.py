import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
data = {
    "Mês": [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ],
    "EBSCO (R$)": [5000, 1000, 1000, 1000, 0, 0, 0, 0, 0, 0, 0, 0],
    "CAPES (R$)": [800, 800, 810, 1000, 0, 0, 0, 0, 0, 0, 0, 0],
    "Pergamum (R$)": [2000, 2000, 2500, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Minha Biblioteca (R$)": [1100, 1100, 1100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Total Mensal (R$)": [8900, 4900, 5410, 2000, 0, 0, 0, 0, 0, 0, 0, 0]
}

df = pd.DataFrame(data)

# Certifique-se de que o DataFrame está na ordem correta dos meses
meses_ordem_certa = [
    "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto",
    "Setembro", "Outubro", "Novembro", "Dezembro"
]

df['Mês'] = pd.Categorical(df['Mês'], categories=meses_ordem_certa, ordered=True)
df = df.sort_values('Mês')

# Exibir os dados
st.write("### Gastos do SIBI UniFTC:")
st.write(df)

# Gráficos
st.write("### Fluxo de Gastos:")

# Gráfico de Barras
st.bar_chart(df.set_index("Mês"))

# Gráfico de Pizza
st.write("#### Total por Produtos:")
fig, ax = plt.subplots()
ax.pie(df.iloc[:, 1:5].sum(), labels=df.columns[1:5], autopct='%1.1f%%')
st.pyplot(fig)

# Gráfico de Linha
st.write("#### Total Mensal (Linha):")
st.line_chart(df.set_index("Mês")["Total Mensal (R$)"])

# Gráfico de Barras Horizontais Empilhadas para Total Anual por Serviço
st.write("#### Total Anual por Serviço:")
total_anual = df.iloc[:, 1:5].sum()
st.bar_chart(pd.DataFrame(total_anual).T)
