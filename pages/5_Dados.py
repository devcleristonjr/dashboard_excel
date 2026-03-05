
import io
import pandas as pd
import streamlit as st
from src.ui import sidebar_data_pipeline, dataframe_pretty, downloads_box

st.title("🧾 Dados")

df_f, base, logs = sidebar_data_pipeline()
if base.empty:
    st.info("Carregue os dados na barra lateral.")
    st.stop()

colunas_ordem = [
    "ITEM", "DATA EVENTO", "ÓRGÃO", "MUNICÍPIOS", "DESCRIÇÃO",
    "VALOR ESTIMADO (R$)", "VALOR_NUM", "ATO", "Situação", "__ARQUIVO__", "__ABA__"
]
cols = [c for c in colunas_ordem if c in df_f.columns]
view = df_f[cols].copy()

order_cols = [c for c in ["DATA EVENTO", "VALOR_NUM"] if c in view.columns]
if order_cols:
    asc = [True if c == "DATA EVENTO" else False for c in order_cols]
    view = view.sort_values(by=order_cols, ascending=asc)

dataframe_pretty(view.head(1000))
downloads_box(view)
