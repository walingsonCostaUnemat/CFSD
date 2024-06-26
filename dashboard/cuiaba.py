import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.analises_avancadas import clusterizacao, analise_rede, mapas_de_calor, titulos

def carregar_dados(file_path):
    data = pd.read_csv(file_path)    
    if 'Nome de Guerra' in data.columns:
        data['Nome de Guerra'] = data['Nome de Guerra'].str.upper()
    return data

    
def resumo_geral(data):
    st.header("Resumo Geral")
    
    # Contagem total de militares
    total_militares = len(data)
    st.subheader(f"Total de Militares: {total_militares}")
    st.markdown(f"Atualmente, temos um total de **{total_militares}** militares interessados em Cuiabá e Várzea Grande.")
    
    # Distribuição por Pelotão
    distribuicao_pelotao = data['Pelotão'].value_counts().reset_index()
    distribuicao_pelotao.columns = ['Pelotão', 'Quantidade']
    st.subheader("Distribuição por Pelotão")
    fig_pelotao = px.bar(distribuicao_pelotao, x='Pelotão', y='Quantidade', title='Distribuição de Militares por Pelotão')
    st.plotly_chart(fig_pelotao)
    st.markdown("O gráfico acima mostra a distribuição dos militares por pelotão. Podemos observar que alguns pelotões possuem um número significativamente maior de militares interessados.")

def contagem_por_graduacao(data):
    st.header("Contagem de Militares por Categoria de Graduação")
    
    # Contagem por categoria de graduação
    graduacao_counts = data['Nova Categoria Graduação'].value_counts().reset_index()
    graduacao_counts.columns = ['Categoria de Graduação', 'Quantidade']
    st.subheader("Contagem por Categoria de Graduação")
    fig_graduacao = px.pie(graduacao_counts, names='Categoria de Graduação', values='Quantidade', title='Distribuição de Militares por Categoria de Graduação')
    st.plotly_chart(fig_graduacao)
    
    st.markdown("A distribuição por categoria de graduação indica a diversidade de formações entre os militares. Abaixo, apresentamos uma tabela detalhada dos militares por categoria de graduação.")
    
    for categoria in graduacao_counts['Categoria de Graduação']:
        st.write(f"**{categoria}**")
        militares_na_categoria = data[data['Nova Categoria Graduação'] == categoria]
        tabela_graduacao = militares_na_categoria[['Classificação no CFSD', 'Nome de Guerra', 'Graduação']]
        tabela_graduacao = tabela_graduacao.rename(columns={
            'Classificação no CFSD': 'Classificação',
            'Nome de Guerra': 'Nome de Guerra',
            'Graduação': 'Nome da Graduação'
        })
        st.dataframe(tabela_graduacao)

def contagem_por_experiencia(data):
    st.header("Contagem de Militares por Categoria de Experiência")
    
    # Contagem por categoria de experiência
    experiencia_counts = data['Categoria Experiência'].value_counts().reset_index()
    experiencia_counts.columns = ['Categoria de Experiência', 'Quantidade']
    st.subheader("Contagem por Categoria de Experiência")
    fig_experiencia = px.bar(experiencia_counts, x='Categoria de Experiência', y='Quantidade', title='Distribuição de Militares por Categoria de Experiência')
    st.plotly_chart(fig_experiencia)
    
    st.markdown("A distribuição por categoria de experiência mostra a variedade de experiências profissionais entre os militares. Abaixo, apresentamos uma tabela detalhada dos militares por categoria de experiência.")
    
    for categoria in experiencia_counts['Categoria de Experiência']:
        st.write(f"**{categoria}**")
        militares_na_categoria = data[data['Categoria Experiência'] == categoria]
        tabela_experiencia = militares_na_categoria[['Classificação no CFSD', 'Nome de Guerra', 'Categoria Experiência', 'Experiências profissionais']]
        tabela_experiencia = tabela_experiencia.rename(columns={
            'Classificação no CFSD': 'Classificação',
            'Nome de Guerra': 'Nome de Guerra',
            'Categoria Experiência': 'Categoria de Experiência',
            'Experiências profissionais': 'Experiência'
        })
        st.dataframe(tabela_experiencia)

def perfil_demografico(data):
    st.header("Perfil Demográfico")
    
    st.subheader("Distribuição de Graduados por Cidade e Pelotão")
    graduacao_cidade_pelotao = data.groupby(['Cidades', 'Pelotão']).size().reset_index(name='Quantidade')
    fig_demografico = px.bar(graduacao_cidade_pelotao, x='Cidades', y='Quantidade', color='Pelotão', title='Distribuição de Graduados por Cidade e Pelotão')
    st.plotly_chart(fig_demografico)
    
    st.markdown("A análise acima mostra a distribuição de graduados por cidade e pelotão. Podemos observar se há uma concentração de certas graduações ou experiências em determinadas regiões.")

def gerar_relatorio():
    st.title("Relatório de Preferências de Militares em Cuiabá e Várzea Grande")
    st.markdown("""
    ## Introdução
    Este relatório apresenta uma análise das preferências dos militares em relação às cidades de Cuiabá e Várzea Grande.
    O objetivo é fornecer insights sobre a distribuição dos militares por diferentes categorias e comandos regionais.
    """)

    # Carregar os dados
    file_path = 'Cuiaba.csv'
    data = carregar_dados(file_path)
    
    # Resumo Geral
    resumo_geral(data)
    
    # Contagem por Categoria de Graduação
    contagem_por_graduacao(data)
    
    # Contagem por Categoria de Experiência
    contagem_por_experiencia(data)
    
    # Perfil Demográfico
    perfil_demografico(data)
    
    
    st.markdown("""
    ## Análises Avançadas
    """)
    
    # Chamar as funções de análises avançadas
    clusterizacao(data)
    titulos(data)
    analise_rede(data)
    mapas_de_calor(data)
    
    st.markdown("""
    ## Conclusão
    Os dados apresentados fornecem uma visão clara sobre as preferências dos militares em Cuiabá e Várzea Grande.
    Essas informações são essenciais para a tomada de decisões estratégicas e alocação de recursos.
    """)

# Chamada da função principal para gerar o relatório
if __name__ == "__main__":
    gerar_relatorio()
