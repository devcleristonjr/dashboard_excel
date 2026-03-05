import streamlit as st
from src.ui import sidebar_data_pipeline, kpi_cards

st.set_page_config(page_title="Dashboard Excel - SERIN", layout="wide")

st.title("📊 Dashboard Interativo para Excel")
st.caption("Envie planilhas na barra lateral e navegue pelas páginas acima (Visão Geral, Órgãos, Municípios, Tempo, Dados).")

# Carrega dados + filtros globais na sidebar (fica disponível em qualquer página).
df_f, base, logs = sidebar_data_pipeline()

if base.empty:
    st.info("Envie uma ou mais planilhas (.xlsx/.xls) na barra lateral. Detectamos automaticamente as abas com os cabeçalhos padrão.")
    if logs:
        with st.expander("📄 Log de leitura"):
            for m in logs: st.caption(m)
    st.stop()

# KPIs rápidos na Home (mesmo recorte aplicado)
kpi_cards(df_f)
st.success("Pronto! Agora use as páginas no topo para explorar: Visão Geral, Órgãos, Municípios, Tempo e Dados.")
