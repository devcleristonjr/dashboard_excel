
import streamlit as st
import pandas as pd
from src.ui import sidebar_data_pipeline
from src.charts import municipio_time_series, municipio_valor_por_orgao
from src.theme import apply_theme

apply_theme()


st.title("🏙️ Municípios")

df_f, base, logs = sidebar_data_pipeline()
if base.empty:
    st.info("Carregue os dados na barra lateral.")
    st.stop()

mun_rank = (df_f.groupby("MUNICÍPIOS")["VALOR_NUM"].sum()
            .sort_values(ascending=False).reset_index())
if mun_rank.empty:
    st.info("Sem dados no recorte atual.")
    st.stop()

mun_escolhido = st.selectbox("Selecione um Município", options=mun_rank["MUNICÍPIOS"], index=0)
df_m = df_f[df_f["MUNICÍPIOS"] == mun_escolhido].copy()

col1, col2 = st.columns([2, 2])
with col1:
    st.plotly_chart(municipio_time_series(df_m), use_container_width=True)

with col2:
    st.plotly_chart(municipio_valor_por_orgao(df_m), use_container_width=True)
