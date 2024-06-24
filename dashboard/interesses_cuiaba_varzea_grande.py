import streamlit as st
import pandas as pd

def interesses_cuiaba_varzea_grande(data):
    st.header("Interesses em Cuiabá e Várzea Grande")
    
    # Selecionar colunas a exibir
    colunas = st.multiselect("Selecione as Colunas para Exibir", options=list(data.columns))
    if not colunas:
        st.warning("Por favor, selecione pelo menos uma coluna para exibir os dados.")
        return
    
    data_selecionada = data[colunas]
    
    st.write("Dados Filtrados:", data_selecionada)
    
    # Filtro de Coluna
    filtro_coluna = st.selectbox("Selecione a Coluna para Filtrar", colunas, key="filtro_coluna_cuiaba")
    if filtro_coluna:
        valores_unicos = data_selecionada[filtro_coluna].unique()
        valor_filtro = st.selectbox(f"Selecione o Valor de {filtro_coluna}", valores_unicos, key="valor_filtro_cuiaba")
        if valor_filtro:
            data_filtrada_filtro = data_selecionada[data_selecionada[filtro_coluna] == valor_filtro]
            num_elementos = len(data_filtrada_filtro)
            st.write(f"Dados Filtrados por {filtro_coluna} ({num_elementos} elementos):", data_filtrada_filtro)

# Aplicação principal
if __name__ == "__main__":
    # Carregar os dados
    file_path = 'Cuiaba.csv'
    data = pd.read_csv(file_path)

    # Interface do Streamlit
    st.title("Dashboard de Preferências de Cidades")
    st.sidebar.title("Navegação")
    modulo = st.sidebar.selectbox("Selecione o Módulo", ["Interesses em Cuiabá e Várzea Grande"])

    if modulo == "Interesses em Cuiabá e Várzea Grande":
        interesses_cuiaba_varzea_grande(data)
