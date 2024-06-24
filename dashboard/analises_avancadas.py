import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from sklearn.cluster import KMeans
import re
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from pyvis.network import Network
import streamlit.components.v1 as components
import os


def limpar_classificacao(classificacao):
    return int(re.sub(r'\D', '', classificacao))

def clusterizacao(data):
    st.header("Clusterização dos Militares")

    # Descrição da metodologia
    st.markdown("""
    ## Metodologia de Clusterização
    Para realizar a clusterização dos militares, utilizamos a técnica de KMeans. Este método agrupa os militares em três clusters com base nas seguintes características:
    - **Classificação no CFSD**: A classificação do militar no curso.
    - **Nova Categoria Graduação**: A formação acadêmica do militar.
    - **Categoria Experiência**: As experiências profissionais do militar.
    - **Especialização**: Se o militar possui especialização.
    - **Mestrado**: Se o militar possui mestrado.
    - **Doutorado**: Se o militar possui doutorado.
    - **Categoria CNH**: A categoria da carteira de habilitação do militar.

    Cada grupo resultante da clusterização possui características semelhantes, permitindo recomendações de alocação mais precisas.
    """)

    # Limpar a coluna de classificação
    data['Classificação no CFSD'] = data['Classificação no CFSD'].apply(limpar_classificacao)

    # Aplicar KMeans
    X = data[['Classificação no CFSD', 'Nova Categoria Graduação', 'Categoria Experiência', 'Especialização', 'Mestrado', 'Doutorado', 'Categoria CNH']]
    X = pd.get_dummies(X, columns=['Nova Categoria Graduação', 'Categoria Experiência', 'Especialização', 'Mestrado', 'Doutorado', 'Categoria CNH'], drop_first=True)
    kmeans = KMeans(n_clusters=3)
    data['Cluster'] = kmeans.fit_predict(X)

    st.subheader("Visualização dos Grupos de Clusterização")
    fig_cluster = px.scatter(data, x='Classificação no CFSD', y='Cluster', color='Cluster', hover_name='Nome de Guerra', 
                             title='Clusterização dos Militares por Graduação, Experiência e Outros Fatores',
                             labels={'Classificação no CFSD': 'Classificação no CFSD', 'Cluster': 'Grupo'})
    st.plotly_chart(fig_cluster)

    st.markdown("""
    A clusterização acima mostra os principais perfis de militares com base nas graduações, experiências e outros fatores. 
    Cada ponto no gráfico representa um militar, e a cor indica o grupo ao qual ele pertence. 
    Vamos analisar cada grupo em detalhe para entender melhor suas características e recomendações de alocação.
    """)

    # Recomendações de alocação
    def recomendacao(graduacao, experiencia):
        if graduacao == 'Engenharia Civil' and experiencia == 'Construção':
            return "Engenharia e Construção"
        elif graduacao == 'Medicina' and experiencia == 'Saúde':
            return "Saúde e Atendimento Pré-Hospitalar"
        elif graduacao == 'Administração' and experiencia == 'Gestão':
            return "Administração e Gestão"
        elif graduacao == 'Educação Física' and experiencia == 'Treinamento':
            return "Educação e Treinamento"
        elif graduacao == 'Tecnologia da Informação' and experiencia == 'TI':
            return "Tecnologia da Informação e Comunicação"
        else:
            return f"{graduacao} com experiência em {experiencia}"

    for cluster_id in data['Cluster'].unique():
        st.write(f"**Grupo {cluster_id}**")
        grupo = data[data['Cluster'] == cluster_id]
        grupo['Recomendação'] = grupo.apply(lambda row: recomendacao(row['Nova Categoria Graduação'], row['Categoria Experiência']), axis=1)

        # Tabela com detalhes dos militares
        detalhes_militares = grupo[['Classificação no CFSD', 'Nome de Guerra', 'Graduação', 'Recomendação', 'Categoria CNH']]
        detalhes_militares = detalhes_militares.rename(columns={
            'Classificação no CFSD': 'Classificação',
            'Nome de Guerra': 'Nome de Guerra',
            'Nova Categoria CNH': 'CNH'
        })
        detalhes_militares = detalhes_militares.set_index('Classificação')
        detalhes_militares = detalhes_militares.sort_index()

        st.markdown(f"**Detalhes dos Militares do Grupo {cluster_id}:**")
        st.table(detalhes_militares)
def analise_rede(data):
    st.header("Análise de Rede entre Categorias de Graduação e Experiência")

    # Descrição da metodologia
    st.markdown("""
    ## Metodologia de Análise de Rede
    A análise de rede é uma metodologia utilizada para identificar e visualizar as conexões entre diferentes categorias de graduação e experiência dos militares. 
    Isso permite entender como essas categorias estão inter-relacionadas e identificar clusters ou grupos que compartilham características semelhantes.

    ### Aplicação
    A aplicação da análise de rede no contexto dos militares permite identificar quais formações e experiências estão mais associadas, ajudando na tomada de decisões estratégicas para alocação e treinamento.

    ### Importância
    A análise de rede é importante para:
    - Visualizar as inter-relações entre diferentes categorias.
    - Identificar clusters de militares com características semelhantes.
    - Apoiar a alocação estratégica e o planejamento de treinamentos específicos.
    """)

    # Construção da rede
    G = nx.Graph()

    # Adicionando nós e arestas
    for i, row in data.iterrows():
        G.add_node(row['Nome de Guerra'], title=row['Nome de Guerra'])
        G.add_edge(row['Nova Categoria Graduação'], row['Nome de Guerra'])
        G.add_edge(row['Categoria Experiência'], row['Nome de Guerra'])

    # Gerar a rede usando pyvis
    net = Network(notebook=True, height="750px", width="100%", bgcolor="#ffffff", font_color="black")

    # Adicionando os nós e arestas do NetworkX para o Pyvis
    net.from_nx(G)

    # Configurar para permitir arrastar e soltar
    net.toggle_physics(True)

    # Salvar a rede em um arquivo HTML temporário
    html_file_path = 'network.html'
    net.save_graph(html_file_path)

    # Exibir o gráfico interativo
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    components.html(html_content, height=750)


import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

def mapas_de_calor(data):
    st.header("Mapas de Calor de Graduações e Experiências por Região")

    # Explicação da metodologia
    st.markdown("""
    ## Metodologia de Mapas de Calor
    Os mapas de calor são ferramentas visuais que permitem identificar a concentração de diferentes categorias, como graduações e experiências, em diferentes regiões.
    Isso ajuda a visualizar rapidamente onde há maior presença de determinadas formações e experiências.

    ### Aplicação
    Aplicar mapas de calor no contexto dos militares ajuda a identificar padrões de distribuição e a tomar decisões estratégicas baseadas na concentração de competências.

    ### Importância
    A importância dos mapas de calor inclui:
    - Identificar concentrações de graduações e experiências por região.
    - Facilitar a alocação de recursos e treinamentos.
    - Apoiar a tomada de decisões estratégicas.
    """)

    # Preparar os dados para o mapa de calor
    heatmap_data = data.pivot_table(index='Cidades', columns='Nova Categoria Graduação', aggfunc='size', fill_value=0)

    # Gerar o mapa de calor
    fig = px.imshow(heatmap_data, text_auto=True, aspect="auto", color_continuous_scale="Blues")
    fig.update_layout(title='Mapa de Calor das Graduações por Cidade', xaxis_title='Nova Categoria Graduação', yaxis_title='Cidades')

    # Exibir o gráfico
    st.plotly_chart(fig, use_container_width=True)

    # Tabela de distribuição de graduações por cidade
    st.markdown("### Distribuição de Graduações por Cidade")
    distribuicao_grad_cidade = data[['Classificação no CFSD', 'Nome de Guerra', 'Cidades', 'Nova Categoria Graduação']]
    distribuicao_grad_cidade = distribuicao_grad_cidade.sort_values(by='Classificação no CFSD')
    distribuicao_grad_cidade = distribuicao_grad_cidade.rename(columns={
        'Classificação no CFSD': 'Classificação',
        'Nome de Guerra': 'Nome de Guerra',
        'Cidades': 'Cidade',
        'Nova Categoria Graduação': 'Categoria de Graduação'
    })
    st.dataframe(distribuicao_grad_cidade)

    # Mapa geográfico de calor
    st.markdown("### Mapa Geográfico de Calor")

    # Select box para graduação
    graduacoes = data['Nova Categoria Graduação'].unique()
    selected_graduacao = st.selectbox("Selecione a Graduação", graduacoes)

    # Filtrar os dados com base na seleção de graduação
    filtered_data = data[data['Nova Categoria Graduação'] == selected_graduacao]

    # Coordenadas fictícias para as cidades (deve ser substituído por coordenadas reais)
    city_coords = {
        'CR 1 - Cuiabá': [-15.6014109, -56.0978917],
        'CR 1 - Várzea Grande - 2º BBM': [-15.6459258, -56.1322715],
        'CR 1 - Poconé - 1º PIBM': [-16.2571, -56.6246],
        'CR 1 - Santo Antônio de Leveger - 2º PIBM': [-15.8548, -56.0704]
    }

    

    # Criar o mapa
    folium_map = folium.Map(location=[-15.6014109, -56.0978917], zoom_start=9)

    # Adicionar pontos de calor ao mapa
    heat_data = []
    for _, row in filtered_data.iterrows():
        if row['Cidades'] in city_coords:
            heat_data.append(city_coords[row['Cidades']] + [1])

    if heat_data:
        HeatMap(heat_data).add_to(folium_map)
        st_folium(folium_map, width=700, height=500)
    else:
        st.warning("Não há dados para gerar o mapa de calor para a graduação selecionada.")

def titulos(data):
    st.header("Militares com Títulos Acadêmicos")
    st.markdown("""
    ### Contextualização
    Este relatório apresenta os militares que possuem títulos acadêmicos, incluindo especialização, mestrado e doutorado.
    A importância de identificar esses militares com títulos avançados é crucial para a alocação estratégica de funções que requerem conhecimentos especializados.
    """)

    # Substituir "Não", "Nao", "Nao possui doutorado." e valores vazios por "-"
    def limpar_titulos(titulo):
        if pd.isna(titulo) or 'não' in str(titulo).lower() or 'nenhuma' in str(titulo).lower() or 'nao' in str(titulo).lower() or 'nao possui doutorado' in str(titulo).lower():
            return ' - '
        return titulo

    titulos_cols = ['Especialização', 'Mestrado', 'Doutorado']
    for col in titulos_cols:
        data[col] = data[col].apply(limpar_titulos)

    # Filtrar militares que possuem pelo menos uma especialização, mestrado ou doutorado válida
    titulos_data = data[
        (data['Especialização'] != ' - ') |
        (data['Mestrado'] != ' - ') |
        (data['Doutorado'] != ' - ')
    ]

    # Selecionar as colunas relevantes
    cols_titulos = ['Classificação no CFSD', 'Nome de Guerra', 'Graduação', 'Especialização', 'Mestrado', 'Doutorado']
    titulos_data = titulos_data[cols_titulos]

    # Ordenar por Doutorado, Mestrado, Especialização e Classificação no CFSD
    titulos_data = titulos_data.sort_values(by=['Doutorado', 'Mestrado', 'Especialização', 'Classificação no CFSD'], ascending=[False, False, False, True])

    # Definir a classificação como índice
    titulos_data.set_index('Classificação no CFSD', inplace=True)

    # Exibir a tabela
    st.dataframe(titulos_data)
# Chamada da função com o dataframe de dados
# data = carregar_dados('caminho/para/seu/arquivo.csv')
# mapas_de_calor(data)
