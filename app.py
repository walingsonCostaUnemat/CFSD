import streamlit as st
import pandas as pd
from io import BytesIO
import qrcode
import vobject
from PIL import Image
from dashboard.distribuicao_cidades import distribuicao_cidades
from dashboard.escolhas_por_pelotao import escolhas_por_pelotao
from dashboard.selecionar_colunas import selecionar_colunas
from dashboard.interesses_cuiaba_varzea_grande import interesses_cuiaba_varzea_grande
from dashboard.selecionar_colunas_capital import selecionar_colunas_capital
from dashboard.cuiaba import gerar_relatorio
from dashboard.interior import gerar_relatorio_interior  # Importar a nova função

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
            return f"({numero_str[:2]}){numero_str[2:6]}-{numero_str[6:10]}"
        else:
            return numero  # Retorna o número original se não tiver o tamanho esperado

    data = pd.read_csv(file_path)
    
    if 'Telefone DDD' in data.columns:
        data['Telefone DDD'] = data['Telefone DDD'].apply(formatar_telefone)
    
    return data

def criar_qrcode_vcard(nome, telefone, email, whatsapp_url):
    vcard = vobject.vCard()
    vcard.add('fn').value = nome
    vcard.add('tel').value = telefone
    vcard.add('email').value = email
    vcard.add('url').value = whatsapp_url
    vcard.add('note').value = 'Desenvolvedor'

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,  # Reduzindo o tamanho do QR code
        border=2,
    )
    qr.add_data(vcard.serialize())
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

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
data = carregar_dados(file_path)

# Ajustar o nome da coluna "Justificativa "
if "Justificativa " in data.columns:
    data = data.rename(columns={"Justificativa ": "Justificativa"})

# Limpar os nomes das cidades
data['Cidades Limpo'] = data['Cidades'].apply(lambda nome: nome.split(" - ")[1] if len(nome.split(" - ")) > 1 else nome.split(" - ")[0])

st.sidebar.title("Navegação")
escolha_local = st.sidebar.radio("Selecione a Localidade", ["Capital", "Interior"], index=None)

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

# Adicionar QR Code na barra lateral inferior
st.sidebar.markdown("---")
st.sidebar.markdown("### Qr Code para contato")

whatsapp_url = "https://api.whatsapp.com/send/?phone=%2B5566996352623&text&type=phone_number&app_absent=0"
img = criar_qrcode_vcard("Walingson Costa", "+5566996352623", "walingson.costa@unemat.br", whatsapp_url)
buf = BytesIO()
img.save(buf)
buf.seek(0)
st.sidebar.image(buf, caption="Aponte a câmera")
if __name__ == "__main__":
    if escolha_local is None:
        pagina_principal()
