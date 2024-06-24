# dashboard/selecionar_colunas.py
import streamlit as st
import pandas as pd

def formatar_nome_completo(nome):
    palavras = nome.split()
    nome_formatado = ' '.join([palavra.capitalize() if len(palavra) >= 3 else palavra for palavra in palavras])
    return nome_formatado

def solicitar_senha_coordenacao():
    senha = st.text_input("Digite a palavra-passe para visualizar justificativas", type="password")
    if st.button("Verificar"):
        if senha == "Coordenação 19":
            st.session_state["justificativa_autenticada"] = True
            st.success("Autenticação bem-sucedida!")
        else:
            st.error("Palavra-passe incorreta!")

def selecionar_colunas(data):
    st.header("Selecionar Colunas e Aplicar Filtros")
    
    # Filtrar todas as cidades exceto Cuiabá e Várzea Grande
    data_filtrada = data[~data['Cidades Limpo'].isin(['Cuiabá', 'Várzea Grande'])]
    
    # Remover duplicatas com base na coluna "Classificação no CFSD"
    data_filtrada = data_filtrada.drop_duplicates(subset=['Classificação no CFSD'])
    
    colunas = st.multiselect("Selecione as Colunas", data_filtrada.columns, key="colunas")
    if colunas:
        if 'Justificativa' in colunas and not st.session_state.get("justificativa_autenticada", False):
            st.warning("Disponível somente para coordenação.")
            solicitar_senha_coordenacao()
            colunas.remove('Justificativa')
        
        data_selecionada = data_filtrada[colunas]
        
        # Aplicar formatação
        if 'Nome de Guerra' in colunas:
            data_selecionada['Nome de Guerra'] = data_selecionada['Nome de Guerra'].str.upper()
        if 'Nome Completo' in colunas:
            data_selecionada['Nome Completo'] = data_selecionada['Nome Completo'].apply(formatar_nome_completo)
        if 'Justificativa' in colunas:
            data_selecionada['Justificativa'] = data_selecionada['Justificativa'].str.capitalize()
        
        st.write("Dados Filtrados:", data_selecionada)
        
        filtro_coluna = st.selectbox("Selecione a Coluna para Filtrar", colunas, key="filtro_coluna")
        if filtro_coluna:
            valores_unicos = data_selecionada[filtro_coluna].unique()
            valor_filtro = st.selectbox(f"Selecione o Valor de {filtro_coluna}", valores_unicos, key="valor_filtro")
            data_filtrada_filtro = data_selecionada[data_selecionada[filtro_coluna] == valor_filtro]
            
            st.write("Dados Filtrados:", data_filtrada_filtro)
