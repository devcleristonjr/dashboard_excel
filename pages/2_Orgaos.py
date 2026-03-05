
import streamlit as st
import pandas as pd
from src.ui import sidebar_data_pipeline
from src.charts import org_top_municipios, ato_por_municipio_stacked
from src.theme import apply_theme

apply_theme()


st.title("🏛️ Órgãos")

df_f, base, logs = sidebar_data_pipeline()
if base.empty:
    st.info("Carregue os dados na barra lateral.")
    st.stop()

org_rank = (df_f.groupby("ÓRGÃO")["VALOR_NUM"].sum()
            .sort_values(ascending=False).reset_index())
if org_rank.empty:
    st.info("Sem dados no recorte atual.")
    st.stop()

org_escolhido = st.selectbox("Selecione um Órgão", options=org_rank["ÓRGÃO"], index=0)
df_o = df_f[df_f["ÓRGÃO"] == org_escolhido].copy()

col1, col2 = st.columns([2, 2])
with col1:
    top_k = st.slider("Top Municípios", 3, 20, 10, 1)
    st.plotly_chart(org_top_municipios(df_o, top_k), use_container_width=True)

with col2:
    muns_exibidos = (df_o.groupby("MUNICÍPIOS")["VALOR_NUM"].sum()
                     .sort_values(ascending=False).head(top_k).index)
    st.plotly_chart(ato_por_municipio_stacked(df_o[df_o["MUNICÍPIOS"].isin(muns_exibidos)]),
                    use_container_width=True)
