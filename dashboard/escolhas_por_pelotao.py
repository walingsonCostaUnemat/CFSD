# dashboard/escolhas_por_pelotao.py
import streamlit as st
import plotly.express as px
import pandas as pd

def limpar_nome_cidade(nome):
    partes = nome.split(" - ")
    return partes[1] if len(partes) > 1 else partes[0]

def escolhas_por_pelotao(data):
    st.header("Escolhas de Cidade por Pelotão")
    
    # Seletor de pelotão
    pelotao = st.selectbox("Selecione o Pelotão", data['Pelotão'].unique())
    
    # Filtrar dados pelo pelotão selecionado
    data_pelotao = data[data['Pelotão'] == pelotao]
    
    # Limpar os nomes das cidades
    data_pelotao['Cidades Limpo'] = data_pelotao['Cidades'].apply(limpar_nome_cidade)
    
    # Contagem das cidades
    cidade_counts_pelotao = data_pelotao['Cidades Limpo'].value_counts().reset_index()
    cidade_counts_pelotao.columns = ['Cidades', 'Contagem']
    
    # Gráfico de pizza interativo
    fig = px.pie(cidade_counts_pelotao, values='Contagem', names='Cidades', title=f'Escolhas de Cidade por {pelotao}')
    st.plotly_chart(fig)
    
    # Total de alunos por cidade
    st.subheader("Total de Alunos por Cidade")
    st.table(cidade_counts_pelotao)
    
    # Filtro por cidade
    cidade = st.selectbox("Selecione a Cidade", cidade_counts_pelotao['Cidades'])
    alunos_na_cidade = data_pelotao[data_pelotao['Cidades Limpo'] == cidade].sort_values(by='Classificação no CFSD')
    
    st.subheader(f"Alunos em {cidade}")
    for _, row in alunos_na_cidade.iterrows():
        st.write(f"- {row['Nome de Guerra']} (Classificação: {row['Classificação no CFSD']})")

# Aplicação principal
if __name__ == "__main__":
    # Carregar os dados
    file_path = 'escolha.csv'
    data = pd.read_csv(file_path)

    # Ajustar o nome da coluna "Justificativa "
    data = data.rename(columns={"Justificativa ": "Justificativa"})

    # Interface do Streamlit
    st.title("Dashboard de Preferências de Cidades")
    st.sidebar.title("Navegação")
    modulo = st.sidebar.selectbox("Selecione o Módulo", ["Distribuição de Alunos por Cidades", "Escolhas de Cidade por Pelotão", "Selecionar Colunas e Aplicar Filtros"])

    if modulo == "Distribuição de Alunos por Cidades":
        distribuicao_cidades(data)
    elif modulo == "Escolhas de Cidade por Pelotão":
        escolhas_por_pelotao(data)
    elif modulo == "Selecionar Colunas e Aplicar Filtros":
        selecionar_colunas(data)
