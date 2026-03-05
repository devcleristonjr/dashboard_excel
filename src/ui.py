
import io
import pandas as pd
import streamlit as st
from src.processing import consolidate_files, apply_filters

# -------------- Pipeline de sidebar --------------
def sidebar_data_pipeline():
    """
    Desenha a sidebar (upload + filtros) e retorna:
    (df_filtrado, base_consolidada, logs)
    Usa st.session_state para persistir entre páginas.
    """
    st.sidebar.header("📁 Dados & Filtros")

    # Upload: manter persistência dos arquivos entre páginas
    files = st.sidebar.file_uploader(
        "Envie uma ou mais planilhas (.xlsx/.xls)",
        type=["xlsx","xls"], accept_multiple_files=True
    )

    if files:
        base, logs = consolidate_files(files)
        st.session_state["__base__"] = base
        st.session_state["__logs__"] = logs
    else:
        base = st.session_state.get("__base__", pd.DataFrame())
        logs = st.session_state.get("__logs__", [])

    # Log
    if logs:
        with st.sidebar.expander("📄 Log de leitura", expanded=False):
            for m in logs: st.caption(m)

    # Filtros globais
    periodo = None
    if not base.empty:
        datas_validas = base["DATA EVENTO"].dropna()
        if not datas_validas.empty:
            dmin, dmax = datas_validas.min().date(), datas_validas.max().date()
            c1, c2 = st.sidebar.columns(2)
            with c1:
                ini = st.date_input("Início", value=dmin, min_value=dmin, max_value=dmax)
            with c2:
                fim = st.date_input("Fim", value=dmax, min_value=dmin, max_value=dmax)
            periodo = (pd.to_datetime(ini), pd.to_datetime(fim))

    def opts(col):
        return sorted([v for v in base[col].dropna().astype(str).unique() if v.strip()]) if not base.empty else []

    org_sel = st.sidebar.multiselect("Órgão (global)", options=opts("ÓRGÃO"))
    mun_sel = st.sidebar.multiselect("Município (global)", options=opts("MUNICÍPIOS"))
    ato_sel = st.sidebar.multiselect("Ato (global)", options=opts("ATO"))
    sit_sel = st.sidebar.multiselect("Situação (global)", options=opts("Situação"))
    busca  = st.sidebar.text_input("Buscar na descrição (contém)", "")

    df_f = apply_filters(base, periodo, org_sel, mun_sel, ato_sel, sit_sel, busca)
    return df_f, base, logs

# -------------- KPIs --------------
def formatar_brl(v):
    if pd.isna(v): return "-"
    return f"R$ {v:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

def kpi_cards(df_f: pd.DataFrame):
    total_itens = len(df_f)
    total_valor = df_f["VALOR_NUM"].sum(skipna=True)
    media_valor = df_f["VALOR_NUM"].mean(skipna=True)
    distinct_mun = int(df_f["MUNICÍPIOS"].nunique(dropna=True))
    distinct_org = int(df_f["ÓRGÃO"].nunique(dropna=True))

    st.markdown("""
    <style>
    .kpi-card {background:#f8fafc;border:1px solid #e6e8eb;border-radius:12px;padding:14px 16px;}
    .kpi-label {color:#64748b;font-size:13px;margin-bottom:4px;}
    .kpi-value {color:#0f172a;font-weight:700;font-size:22px;}
    </style>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(f"<div class='kpi-card'><div class='kpi-label'>Itens</div><div class='kpi-value'>{total_itens:,}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card'><div class='kpi-label'>Valor Estimado</div><div class='kpi-value'>{formatar_brl(total_valor)}</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card'><div class='kpi-label'>Valor Médio</div><div class='kpi-value'>{formatar_brl(media_valor)}</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-card'><div class='kpi-label'>Municípios</div><div class='kpi-value'>{distinct_mun}</div></div>", unsafe_allow_html=True)
    c5.markdown(f"<div class='kpi-card'><div class='kpi-label'>Órgãos</div><div class='kpi-value'>{distinct_org}</div></div>", unsafe_allow_html=True)

# -------------- Tabela bonita + Downloads --------------
def dataframe_pretty(view: pd.DataFrame):
    col_config = {}
    if "VALOR_NUM" in view.columns:
        col_config["VALOR_NUM"] = st.column_config.NumberColumn(
            "Valor (numérico)", format="R$ %.2f",
            help="Campo numérico calculado a partir de 'VALOR ESTIMADO (R$)'",
            width="medium"
        )
    if "VALOR ESTIMADO (R$)" in view.columns:
        col_config["VALOR ESTIMADO (R$)"] = st.column_config.TextColumn(
            "Valor Estimado (R$)", help="Valor original da planilha", width="large"
        )
    for c in ["DESCRIÇÃO","MUNICÍPIOS","ÓRGÃO","ATO","Situação"]:
        if c in view.columns:
            col_config[c] = st.column_config.TextColumn(c, width="large")

    st.dataframe(view, use_container_width=True, hide_index=True, column_config=col_config)

def downloads_box(view: pd.DataFrame):
    csv_bytes = view.to_csv(index=False, sep=";", encoding="utf-8").encode("utf-8")
    buffer_xlsx = io.BytesIO()
    with pd.ExcelWriter(buffer_xlsx, engine="openpyxl") as writer:
        view.to_excel(writer, index=False, sheet_name="dados")
    buffer_xlsx.seek(0)

    cdl1, cdl2 = st.columns(2)
    cdl1.download_button("⬇️ Baixar CSV (filtrado)", data=csv_bytes,
                         file_name="dados_filtrados.csv", mime="text/csv")
    cdl2.download_button("⬇️ Baixar Excel (filtrado)", data=buffer_xlsx,
                         file_name="dados_filtrados.xlsx",
                         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
