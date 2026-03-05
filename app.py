# app.py
import streamlit as st
from src.theme import apply_theme
from src import data_io as io

# ===== Configuração da página (sempre primeiro) =====
st.set_page_config(
    page_title="Dashboard Excel",
    page_icon="📊",
    layout="wide"
)

# ===== Tema (cores Steam, fontes brancas, etc.) =====
apply_theme()

# ===== Título e descrição =====
st.title("Dashboard Excel")
st.caption("")

st.markdown(
    """
## Como usar esta aplicação

1. **Faça o upload do arquivo Excel** pela **sidebar** (à esquerda).  
2. Escolha a **aba** (sheet) da planilha, quando aplicável.  
3. Navegue entre as páginas no menu lateral:
   - **Visão Geral**: KPIs e panorama dos dados  
   - **Órgão**: filtros e análises por órgão  
   - **Municípios**: distribuição e métricas por município  

> Dica: Você pode trocar o arquivo a qualquer momento na sidebar.
"""
)

st.markdown("---")

