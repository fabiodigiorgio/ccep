import streamlit as st
import requests
from PIL import Image

# Função para consultar cidade e rua via API do ViaCEP
def buscar_endereco_por_cep(cep):
    try:
        cep = cep.replace("-", "").strip()
        if not cep.isdigit() or len(cep) != 8:
            return ("FORMATO DE CEP INVÁLIDO", None)
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        data = response.json()
        if "erro" in data:
            return ("CEP NÃO ENCONTRADO", None)
        cidade = data.get("localidade", "CIDADE NÃO IDENTIFICADA")
        rua = data.get("logradouro", "RUA NÃO INFORMADA")
        return (cidade, rua)
    except:
        return ("ERRO NA CONSULTA", None)

# Lista de cidades com atendimento disponível
cidades_disponiveis = [
    "São Paulo", "Guarulhos", "Osasco", "Santo André", "São Bernardo do Campo",
    "Diadema", "Barueri", "Carapicuíba", "Mauá", "Suzano", "Taboão da Serra",
    "Embu das Artes", "Itapevi", "Ferraz de Vasconcelos", "Francisco Morato",
    "Franco da Rocha", "Caieiras", "Cotia", "Poá", "Ribeirão Pires",
    "Rio Grande da Serra", "Santa Isabel", "Santana de Parnaíba", "Arujá",
    "Embu-Guaçu", "Itapecerica da Serra", "Jandira", "Mairiporã", "Vargem Grande Paulista",
    "Jundiaí", "São Caetano do Sul", "Alphaville (Barueri)"
]

# Layout da página
st.set_page_config(page_title="Consulta Área Atendimento", layout="centered")

# Logo centralizado
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        logo = Image.open("logo.png")
        st.image(logo, width=150)
    except:
        st.warning("⚠️ Logo não encontrado. Certifique-se de que 'logo.png' está na mesma pasta do script.")

# Título e instrução
st.title("🔍 Consulta Área Atendimento")
st.markdown("Digite um CEP válido para verificar se há atendimento disponível.")

# Campo de entrada de CEP
cep_input = st.text_input("CEP (Ex: 07010-000 ou 07010000)", max_chars=9)

if cep_input:
    cidade, rua = buscar_endereco_por_cep(cep_input)

    st.write(f"📍 **Cidade:** {cidade}")
    if rua:
        st.write(f"📬 **Rua:** {rua}")

    if cidade in cidades_disponiveis:
        st.success("✅ ATENDIMENTO DISPONÍVEL")
    elif cidade in ["CEP NÃO ENCONTRADO", "FORMATO DE CEP INVÁLIDO", "ERRO NA CONSULTA", "CIDADE NÃO IDENTIFICADA"]:
        st.error(f"❌ {cidade}")
    else:
        st.warning("⚠️ INDISPONIBILIDADE DE ATENDIMENTO")

# Rodapé
st.markdown("---")
st.caption("Sistema automatizado de consulta baseado na API ViaCEP e lista de cobertura da RMSP.")
