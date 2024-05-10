import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
data = {
    "Mês": [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro", "Total Anual"
    ],
    "EBSCO (R$)": [5000, 1000, 1000, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 8000],
    "CAPES (R$)": [800, 800, 810, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 3410],
    "Pergamum (R$)": [2000, 2000, 2500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6500],
    "Minha Biblioteca (R$)": [1100, 1100, 1100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3300],
    "Total Mensal (R$)": [8900, 4900, 5410, 2000, 0, 0, 0, 0, 0, 0, 0, 0, 21210]
}

df = pd.DataFrame(data)

# Exibir os dados
st.write("### Gasto da Bibliteca:")
st.write(df)

# Gráficos
st.write("### Gráficos:")

# Gráfico de Barras
st.bar_chart(df.set_index("Mês").drop(columns=["Total Mensal (R$)"]))

# Gráfico de Pizza
st.write("#### Total por Serviço:")
fig, ax = plt.subplots()
ax.pie(df.iloc[0:12, 1:5].sum(), labels=df.columns[1:5], autopct='%1.1f%%')
st.pyplot(fig)

# Gráfico de Linha
st.write("#### Total Mensal (Linha):")
st.line_chart(df.set_index("Mês")["Total Mensal (R$)"])

# Gráfico de Barras Horizontais Empilhadas para Total Anual por Serviço
st.write("#### Total Anual por Serviço:")
st.bar_chart(df.iloc[-1, 1:5])
