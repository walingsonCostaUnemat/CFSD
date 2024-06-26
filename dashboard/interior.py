import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

def carregar_dados(file_path):
    def formatar_telefone(numero):
        """
        Formata um número de telefone para o formato (99)99999-9999 ou (99)9999-9999.

        Args:
        numero (str): Número de telefone a ser formatado.

        Returns:
        str: Número de telefone formatado.
        """
        numero_str = ''.join(filter(str.isdigit, str(numero)))  # Remove caracteres não numéricos
        if len(numero_str) == 11:
            return f"({numero_str[:2]}){numero_str[2:7]}-{numero_str[7:]}"
        elif len(numero_str) == 10:
            return f"({numero_str[:2]}){numero_str[2:6]}-{numero_str[6:]}"
        else:
            return numero  # Retorna o número original se não tiver o tamanho esperado

    data = pd.read_csv(file_path)
    
    if 'Telefone DDD' in data.columns:
        data['Telefone DDD'] = data['Telefone DDD'].apply(formatar_telefone)
    
    return data

def verificar_colunas(data):
    st.header("Verificação de Colunas")
    st.write(data.columns)

def introducao():
    st.title("Relatório de Preferências de Alunos no Interior de MT")
    st.markdown("""
    ## Introdução
    Este relatório apresenta uma análise das preferências dos alunos em relação às cidades do interior de Mato Grosso.
    O objetivo é fornecer insights sobre a distribuição dos alunos por cidade e ajudar na tomada de decisões estratégicas.
    """)

def resumo_geral(data):
    st.header("Resumo Geral")
    
    # Remover cidades do CR 1
    data = data[~data['Cidades'].str.contains('CR 1')]
    
    # Total de alunos
    total_alunos = len(data)
    st.subheader(f"Total de Alunos: {total_alunos}")
    st.markdown(f"Atualmente, temos um total de **{total_alunos}** alunos interessados nas cidades do interior de Mato Grosso.")
    
    # Distribuição por cidade
    cidade_counts = data['Cidades'].value_counts().reset_index()
    cidade_counts.columns = ['Cidade', 'Quantidade']
    st.subheader("Distribuição por Cidade")
    fig_cidade_bar = px.bar(cidade_counts, x='Cidade', y='Quantidade', title='Distribuição de Alunos por Cidade')
    st.plotly_chart(fig_cidade_bar)
    
    # Agregação por CR
    data['CR'] = data['Cidades'].apply(lambda x: x.split(" - ")[0])
    cr_counts = data['CR'].value_counts().reset_index()
    cr_counts.columns = ['CR', 'Quantidade']
    fig_cr_pie = px.pie(cr_counts, values='Quantidade', names='CR', title='Distribuição de Alunos por CR')
    st.plotly_chart(fig_cr_pie)
    
    st.markdown("Os gráficos acima mostram a distribuição dos alunos por cidade e por CR. Podemos observar que algumas regiões possuem um número significativamente maior de alunos interessados.")

def perfil_demografico(data):
    st.header("Perfil Demográfico")
    
    # Remover cidades do CR 1
    data = data[~data['Cidades'].str.contains('CR 1')]
    
    # Agregação por CR e Pelotões
    data['CR'] = data['Cidades'].apply(lambda x: x.split(" - ")[0])
    pelotao_counts = data.groupby(['CR', 'Pelotão']).size().reset_index(name='Quantidade')
    
    fig_combined = go.Figure()
    
    for pelotao in pelotao_counts['Pelotão'].unique():
        pelotao_data = pelotao_counts[pelotao_counts['Pelotão'] == pelotao]
        fig_combined.add_trace(go.Bar(x=pelotao_data['CR'], y=pelotao_data['Quantidade'], name=pelotao))
    
    fig_combined.update_layout(
        title='Distribuição de Alunos por CR e Pelotões',
        xaxis_title='CR',
        yaxis_title='Quantidade',
        barmode='stack'
    )
    
    st.plotly_chart(fig_combined)
    
    st.markdown("### Distribuição por CR e Pelotões")
    st.write(pelotao_counts)

def mapas_de_calor(data):
    st.header("Mapas de Calor")
    
    st.subheader("Heatmap das Cidades")
    
    # Remover cidades do CR 1
    data = data[~data['Cidades'].str.contains('CR 1')]
    
    # Preparar os dados para o heatmap
    data['CR'] = data['Cidades'].apply(lambda x: x.split(" - ")[0])
    heatmap_data = data.groupby('CR').size().reset_index(name='Quantidade')
    
    # Gerar o heatmap
    fig = px.imshow(heatmap_data.pivot(index='CR', columns='Quantidade', values='Quantidade'), text_auto=True, aspect="auto", color_continuous_scale="Blues")
    fig.update_layout(title='Mapa de Calor dos CRs', xaxis_title='CR', yaxis_title='Total')
    st.plotly_chart(fig)
    
    st.subheader("Mapa Geográfico de Calor")
    
    # Coordenadas das cidades
    city_coords = {
        'CR 3 - Sinop - 4º BBM': [-11.8481, -55.5109],
        'CR 2 - Rondonópolis - 3º BBM': [-16.4673, -54.6356],
        'CR 2 - Campo Verde - 11º CIBM': [-15.5456, -55.1624],
        'CR 2 - Primavera do Leste - 6º CIBM': [-15.5439, -54.2811],
        'CR 2 - Alto Araguaia - NBM': [-17.3156, -53.2181],
        'CR 3 - Lucas do Rio Verde - 13ª CIBM': [-13.0588, -55.9042],
        'CR 3 - Nova Mutum - 5º CIBM': [-13.839, -56.0743],
        'CR 7 - Colíder - 12ª CIBM': [-10.813, -55.4601],
        'CR 4 - Nova Xavantina - 4ª CIBM': [-14.6775, -52.3505],
        'CR 6 - Tangará da Serra - 3ª CIBM': [-14.6229, -57.4935],
        'CR 5 - Cáceres - 2ª CIBM': [-16.0765, -57.6834],
        'CR 3 - Sorriso - 10º CIBM': [-12.5425, -55.7215],
        'CR 4 - Barra do Garças - 1ª CIBM': [-15.8804, -52.2562],
        'CR 5 - Pontes e Lacerda - 8ª CIBM': [-15.226, -59.3355],
        'CR 7 - Alta Floresta - 7ª CIBM': [-9.866, -56.0868]
    }
    
    # Criar o mapa
    folium_map = folium.Map(location=[-15.6014109, -56.0978917], zoom_start=6)
    
    # Adicionar pontos de calor ao mapa
    heat_data = []
    for _, row in data.iterrows():
        cidade = row['Cidades']
        if cidade in city_coords:
            heat_data.append(city_coords[cidade] + [1])
    
    HeatMap(heat_data).add_to(folium_map)
    
    # Exibir o mapa
    st_folium(folium_map, width=700, height=500)

def gerar_tabelas_municipios(data):
    st.header("Tabelas por Município")
    
    # Remover cidades do CR 1
    data = data[~data['Cidades'].str.contains('CR 1')]
    
    # Ordenar por classificação
    data = data.sort_values(by='Classificação no CFSD')
    
    # Exibir tabelas por município
    municipios = data['Cidades'].unique()
    for municipio in municipios:
        st.subheader(f"{municipio}")
        df_municipio = data[data['Cidades'] == municipio][['Classificação no CFSD', 'Nome de Guerra', 'Telefone DDD', 'CNH'] if 'Telefone DDD' in data.columns else ['Classificação no CFSD', 'Nome de Guerra']]
        st.dataframe(df_municipio.set_index('Classificação no CFSD'))

def gerar_tabelas_excepcionalidades(data):
    #st.header("Excepcionalidades")
    
    # Verificar a presença da coluna 'Justificativa' e ajustar caso necessário
    justificativa_col = 'Justificativa' if 'Justificativa' in data.columns else next(col for col in data.columns if 'justificativa' in col.lower())
    
    # Filtrar alunos com palavras-chave nas justificativas
    palavras_chave = ['concurso', 'efetiva', 'TDH', 'autismo', 'doença']
    excepcionalidades = data[data[justificativa_col].str.contains('|'.join(palavras_chave), case=False, na=False)]
    
    # Exibir tabela
    cols = ['Nome de Guerra', 'Cidades', 'Telefone DDD', 'Categoria CNH']
    cols = [col for col in cols if col in data.columns]
    #st.dataframe(excepcionalidades[cols])

def gerar_relacao_alunos(data):
    st.header("Relação de Alunos com Intenção de Lotar no Interior")
    
    st.markdown("""
    ## Excepcionalidades
    Abaixo estão listados os militares que possuem cônjuges efetivos no município e/ou dependentes que necessitam de cuidados especiais, como TDH e Autismo. 
    """)

    # Verifique o nome correto da coluna de justificativas no CSV
    if 'Justificativa ' in data.columns:
        col_justificativa = 'Justificativa '
    elif 'Justificativa' in data.columns:
        col_justificativa = 'Justificativa'
    else:
        st.error("Coluna de justificativa não encontrada.")
        return

    # Filtrar alunos com justificativas que indicam excepcionalidades
    palavras_chave = ['concurso', 'efetiva', 'tdh', 'autismo', 'doença']
    excepcionalidades = data[data[col_justificativa].str.contains('|'.join(palavras_chave), case=False, na=False)]
    
    # Exibir tabela de excepcionalidades
    cols_excepcionalidades = ['Nome de Guerra', 'Cidades', 'Telefone DDD', col_justificativa]
    st.subheader("Tabela de Excepcionalidades")
    st.dataframe(excepcionalidades[cols_excepcionalidades])

    # Ordenar por classificação para a tabela geral
    data = data.sort_values(by='Classificação no CFSD')
    
    # Exibir tabela geral
    st.subheader("Tabela Geral de Alunos")
    cols = ['Classificação no CFSD', 'Nome de Guerra', 'Cidades', 'Telefone DDD', 'CNH']
    cols = [col for col in cols if col in data.columns]
    st.dataframe(data[cols].set_index('Classificação no CFSD'))


def gerar_relatorio_interior():
    # Carregar os dados
    file_path = 'escolha.csv'
    data = carregar_dados(file_path)
    
    # Seções do relatório
    introducao()
    resumo_geral(data)
       
    gerar_relacao_alunos(data)
    gerar_tabelas_excepcionalidades(data)
    gerar_tabelas_municipios(data)
    perfil_demografico(data)
    mapas_de_calor(data)

# Chamada da função principal para gerar o relatório
if __name__ == "__main__":
    gerar_relatorio_interior()
