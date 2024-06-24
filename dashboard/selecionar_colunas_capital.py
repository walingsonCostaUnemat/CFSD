# dashboard/selecionar_colunas_capital.py
import streamlit as st
import pandas as pd

def formatar_nome_completo(nome):
    palavras = nome.split()
    nome_formatado = ' '.join([palavra.capitalize() if len(palavra) >= 3 else palavra for palavra in palavras])
    return nome_formatado

def selecionar_colunas_capital(data):
    st.header("Selecionar Colunas e Aplicar Filtros - Capital")
    
    # Filtrar para apenas Cuiabá e Várzea Grande
    data_filtrada = data[data['Cidades Limpo'].isin(['Cuiabá', 'Várzea Grande'])]
    
    colunas = st.multiselect("Selecione as Colunas", data_filtrada.columns, key="colunas_capital")
    if colunas:
        data_selecionada = data_filtrada[colunas]
        
        # Aplicar formatação
        if 'Nome de Guerra' in colunas:
            data_selecionada['Nome de Guerra'] = data_selecionada['Nome de Guerra'].str.upper()
        if 'Nome Completo' in colunas:
            data_selecionada['Nome Completo'] = data_selecionada['Nome Completo'].apply(formatar_nome_completo)
        if 'Justificativa' in colunas:
            st.warning("Disponível somente para coordenação.")
            senha = st.text_input("Digite a palavra-passe para visualizar justificativas", type="password")
            if st.button("Verificar", key="verificar_justificativa"):
                if senha == "Coordenação 19":
                    st.success("Autenticação bem-sucedida!")
                    data_selecionada['Justificativa'] = data_selecionada['Justificativa'].str.capitalize()
                else:
                    st.error("Palavra-passe incorreta!")
                    colunas.remove('Justificativa')
                    data_selecionada = data_filtrada[colunas]
        
        st.write("Dados Filtrados:", data_selecionada)
        
        filtro_coluna = st.selectbox("Selecione a Coluna para Filtrar", colunas, key="filtro_coluna_capital")
        if filtro_coluna:
            valores_unicos = data_selecionada[filtro_coluna].unique()
            valor_filtro = st.selectbox(f"Selecione o Valor de {filtro_coluna}", valores_unicos, key="valor_filtro_capital")
            data_filtrada_filtro = data_selecionada[data_selecionada[filtro_coluna] == valor_filtro]
            
            st.write("Dados Filtrados:", data_filtrada_filtro)
