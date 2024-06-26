import streamlit as st
import pandas as pd
from dashboard.distribuicao_cidades import distribuicao_cidades
from dashboard.escolhas_por_pelotao import escolhas_por_pelotao
from dashboard.selecionar_colunas import selecionar_colunas
from dashboard.interesses_cuiaba_varzea_grande import interesses_cuiaba_varzea_grande
from dashboard.selecionar_colunas_capital import selecionar_colunas_capital
from dashboard.cuiaba import gerar_relatorio
from dashboard.interior import gerar_relatorio_interior  # Importar a nova função

def pagina_principal():
    st.title("Dashboard de Preferências de Cidades")
    st.markdown("""
    Bem-vindo ao Dashboard de Preferências de Cidades!
    
    Este aplicativo tem como objetivo analisar e visualizar as preferências de cidade dos alunos de acordo com suas escolhas e classificações. 
    Você pode navegar pelos diferentes módulos disponíveis para visualizar as distribuições de alunos por cidades, escolhas de cidade por pelotão e selecionar e filtrar colunas específicas.
    
    ### Módulos Disponíveis:
    - **Distribuição de Alunos por Cidades**: Visualize a distribuição dos alunos nas diferentes cidades.
    - **Escolhas de Cidade por Pelotão**: Visualize as escolhas de cidade divididas por pelotão.
    - **Selecionar Colunas e Aplicar Filtros**: Selecione e filtre colunas específicas para uma análise detalhada.
    - **Interesses em Cuiabá e Várzea Grande**: Visualize os alunos interessados em Cuiabá e Várzea Grande.
    - **Relatório de Cuiabá e Várzea Grande**: Relatório detalhado sobre as preferências dos militares em Cuiabá e Várzea Grande.
    - **Relatório do Interior**: Relatório detalhado sobre as preferências dos militares no interior de MT.
    
    Use a barra lateral para navegar pelos módulos.
    """)

# Carregar os dados
file_path = 'escolha.csv'


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

data = carregar_dados(file_path)
# Ajustar o nome da coluna "Justificativa "
if "Justificativa " in data.columns:
    data = data.rename(columns={"Justificativa ": "Justificativa"})

# Limpar os nomes das cidades
data['Cidades Limpo'] = data['Cidades'].apply(lambda nome: nome.split(" - ")[1] if len(nome.split(" - ")) > 1 else nome.split(" - ")[0])

st.sidebar.title("Navegação")
escolha_local = st.sidebar.radio("Selecione a Localidade", ["Capital", "Interior"])

if escolha_local == "Interior":
    modulo = st.sidebar.selectbox("Selecione o Módulo", ["Relatório do Interior", "Escolhas de Cidade por Pelotão", "Selecionar Colunas e Aplicar Filtros", "Distribuição de Alunos por Cidades"])
    if modulo == "Relatório do Interior":
        gerar_relatorio_interior()
    elif modulo == "Escolhas de Cidade por Pelotão":
        escolhas_por_pelotao(data)
    elif modulo == "Selecionar Colunas e Aplicar Filtros":
        selecionar_colunas(data)
    elif modulo == "Distribuição de Alunos por Cidades":
        distribuicao_cidades(data)
elif escolha_local == "Capital":
    modulo = st.sidebar.selectbox("Selecione o Módulo", ["Relatório Cuiabá", "Filtros personalizados"])
    if modulo == "Filtros personalizados":
        interesses_cuiaba_varzea_grande(pd.read_csv('Cuiaba.csv'))
    elif modulo == "Relatório Cuiabá":
        gerar_relatorio()
else:
    pagina_principal()
