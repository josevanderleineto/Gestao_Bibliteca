import streamlit as st
import pandas as pd
import plotly.graph_objs as go

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

# Gráfico de Barras
bar_trace = go.Bar(
    x=filtered_df["Mês"],
    y=[filtered_df[col] for col in filtered_df.columns[1:5]],
)
bar_layout = go.Layout(title="Despesas por Serviço")
bar_fig = go.Figure(data=[bar_trace], layout=bar_layout)
st.plotly_chart(bar_fig)

# Gráfico de Pizza
pie_trace = go.Pie(
    labels=filtered_df.columns[1:5],
    values=filtered_df.iloc[0, 1:5],
    hoverinfo='label+percent',
    textinfo='value',
    textposition='inside',
)
pie_layout = go.Layout(title="Total por Serviço")
pie_fig = go.Figure(data=[pie_trace], layout=pie_layout)
st.plotly_chart(pie_fig)

# Gráfico de Linhas
line_trace = go.Scatter(
    x=df["Mês"],
    y=df["Total Mensal (R$)"],
    mode='lines+markers',
    name='Total Mensal (R$)',
    marker=dict(color='skyblue')
)
line_layout = go.Layout(title="Total Mensal")
line_fig = go.Figure(data=[line_trace], layout=line_layout)
st.plotly_chart(line_fig)

# Segmentação de dados por datas
st.write("### Segmentação de Dados por Datas:")
st.write(df)

# Gráfico de Barras Horizontais Empilhadas para Total Anual por Serviço
total_annual_trace = go.Bar(
    y=df.columns[1:5],
    x=df.iloc[-1, 1:5],
    orientation='h',
)
total_annual_layout = go.Layout(title="Total Anual por Serviço")
total_annual_fig = go.Figure(data=[total_annual_trace], layout=total_annual_layout)
st.plotly_chart(total_annual_fig)

# Gráfico de Linha para Total Anuale
total_annual_line_trace = go.Scatter(
    x=df["Mês"],
    y=df["Total Mensal (R$)"],
    mode='lines',
    name='Total Mensal (R$)',
    marker=dict(color='skyblue')
)
total_annual_line_layout = go.Layout(title="Total Mensal (Linha)")
total_annual_line_fig = go.Figure(data=[total_annual_line_trace], layout=total_annual_line_layout)
st.plotly_chart(total_annual_line_fig)
