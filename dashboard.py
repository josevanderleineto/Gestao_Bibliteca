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

# Sidebar - Filtros
st.sidebar.title("Filtros")
selected_month = st.sidebar.selectbox("Selecione o mês:", df["Mês"])

# Filtrar os dados
filtered_df = df[df["Mês"] == selected_month]

# Exibir os dados filtrados
st.write("### Dados do mês selecionado:")
st.write(filtered_df)

# Gráficos
st.write("### Gráficos:")

# Dividindo a tela em duas colunas
col1, col2 = st.columns(2)

# Gráfico de Barras
with col1:
    st.write("#### Despesas por Serviço:")
    st.bar_chart(filtered_df.set_index("Mês").drop(columns=["Total Mensal (R$)"]))

# Gráfico de Pizza
with col2:
    st.write("#### Total por Serviço:")
    fig, ax = plt.subplots()
    ax.pie(filtered_df.iloc[0, 1:5], labels=filtered_df.columns[1:5], autopct='%1.1f%%')
    st.pyplot(fig)

# Gráfico de Linha
st.write("#### Total Mensal:")
st.line_chart(df.set_index("Mês")["Total Mensal (R$)"])

# Segmentação de dados por datas
st.write("### Segmentação de Dados por Datas:")
st.write(df)

# Gráfico de Barras Horizontais Empilhadas para Total Anual por Serviço
st.write("#### Total Anual por Serviço:")
st.bar_chart(df.iloc[-1, 1:5])

# Gráfico de Linha para Total Anual
st.write("#### Total Mensal (Linha):")
st.line_chart(df.set_index("Mês")["Total Mensal (R$)"])
