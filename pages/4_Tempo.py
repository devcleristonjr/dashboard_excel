
import streamlit as st
from src.ui import sidebar_data_pipeline
from src.charts import area_ato_tempo

st.title("⏱️ Tempo")

df_f, base, logs = sidebar_data_pipeline()
if base.empty:
    st.info("Carregue os dados na barra lateral.")
    st.stop()

st.plotly_chart(area_ato_tempo(df_f), use_container_width=True)
