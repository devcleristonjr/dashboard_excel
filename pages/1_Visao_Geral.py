
import streamlit as st
from src.ui import sidebar_data_pipeline, kpi_cards
from src.charts import bar_valor_por_orgao, donut_situacao

st.title("📌 Visão Geral")

df_f, base, logs = sidebar_data_pipeline()
if base.empty:
    st.info("Carregue os dados na barra lateral.")
    st.stop()

# KPIs
kpi_cards(df_f)

st.markdown("---")
colA, colB = st.columns([2, 1])

with colA:
    st.plotly_chart(bar_valor_por_orgao(df_f, top=10), use_container_width=True)

with colB:
    st.plotly_chart(donut_situacao(df_f), use_container_width=True)
