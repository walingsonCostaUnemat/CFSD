import streamlit as st
import plotly.express as px
import pandas as pd

def limpar_nome_cidade(nome):
    partes = nome.split(" - ")
    return partes[1] if len(partes) > 1 else partes[0]

def destacar_justificativa(justificativa):
    termos_concurso = ['concurso', 'concursada', 'concursado', 'efetiva']
    termos_conjuge = ['doença','Doente','Autismo',"Autista",'autismo', 'autista']
    return (
        any(termo in justificativa.lower() for termo in termos_concurso),
        any(termo in justificativa.lower() for termo in termos_conjuge)
    )

def distribuicao_cidades(data):
    st.header("Distribuição de Alunos no Interior de MT")
    
    # Limpar os nomes das cidades
    data['Cidades Limpo'] = data['Cidades'].apply(limpar_nome_cidade)
    
    # Filtrar todas as cidades exceto Cuiabá e Várzea Grande
    data_filtrada = data[~data['Cidades Limpo'].isin(['Cuiabá', 'Várzea Grande'])]
    
    # Contagem das cidades
    cidade_counts = data_filtrada['Cidades Limpo'].value_counts().reset_index()
    cidade_counts.columns = ['Cidades', 'Contagem']
    
    # Gráfico de pizza interativo
    fig = px.pie(cidade_counts, values='Contagem', names='Cidades', title='Distribuição de Alunos no Interior de MT')
    st.plotly_chart(fig)
    
    # Exibir nomes dos alunos e classificação abaixo do gráfico
    st.subheader("Nomes dos Alunos e Classificação no CFSD")
    alunos_com_conjuge = []
    alunos_com_concurso = []
    nomes_formatados = {}

    for cidade in cidade_counts['Cidades']:
        nomes_formatados[cidade] = []
        alunos_na_cidade = data_filtrada[data_filtrada['Cidades Limpo'] == cidade].sort_values(by='Classificação no CFSD')
        for _, row in alunos_na_cidade.iterrows():
            nome_guerra = row['Nome de Guerra']
            classificacao = row['Classificação no CFSD']
            justificativa = row['Justificativa']
            concurso, conjuge = destacar_justificativa(justificativa)
            if concurso or conjuge:
                nome_formatado = f"** *{nome_guerra}***"
                justificativa_completa = f"{nome_formatado} - {justificativa}"
                if concurso:
                    alunos_com_concurso.append(justificativa_completa)
                else:
                    alunos_com_conjuge.append(justificativa_completa)
            else:
                nome_formatado = nome_guerra
            nomes_formatados[cidade].append(f"- {nome_formatado} (Classificação: {classificacao})")
    
    # Exibir nomes sem justificativas agrupados por cidade
    for cidade, nomes in nomes_formatados.items():
        st.write(f"**{cidade} ({len(nomes)} interessados)**")
        for nome in nomes:
            st.write(nome)
    
    # Adicionar nota ao final
    st.subheader("Nota")
    st.write("Os seguintes alunos possuem cônjuges com concurso público efetivo no município e/ou cônjuges já residentes no município:")
    for aluno in alunos_com_concurso + alunos_com_conjuge:
        st.write(f"- {aluno}")

  

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
