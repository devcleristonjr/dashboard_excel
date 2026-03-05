
import io
import re
import unicodedata
import pandas as pd
import numpy as np
import streamlit as st

# ============ Normalização de colunas ============
def remover_acentos(s: str) -> str:
    if not isinstance(s, str): s = str(s)
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def normalizar_coluna(col: str) -> str:
    base = remover_acentos(col).upper()
    base = re.sub(r"\s+", " ", base).strip()
    base = re.sub(r"[^A-Z0-9\s]", "", base)
    return base

ALIASES = {
    "ITEM": {"ITEM", "ITENS"},
    "DATA EVENTO": {"DATA EVENTO", "DATA DO EVENTO", "DATA", "DATA_EVENTO", "DATA-EVENTO"},
    "ÓRGÃO": {"ORGAO", "ORGÃO", "ORGAO DEMANDANTE", "ORG DEMANDANTE", "UNIDADE", "SECRETARIA"},
    "MUNICÍPIOS": {"MUNICIPIOS", "MUNICIPIO", "MUNICIPIO(S)", "CIDADE", "MUNICIPALIDADE"},
    "DESCRIÇÃO": {"DESCRICAO", "DESCR", "OBJETO", "DESCRICAO DO ITEM", "DESCRÇÃO"},
    "VALOR ESTIMADO (R$)": {"VALOR ESTIMADO RS", "VALOR ESTIMADO", "VALOR TOTAL", "VALOR", "VALOR ORCADO", "VALOR-ESTIMADO"},
    "ATO": {"ATO", "TIPO DE ATO", "MODALIDADE", "TIPO"},
    "Situação": {"SITUACAO", "STATUS", "SITUAÇÃO", "FASE"},
}
ALIASES_INDEX = {}
for canon, variants in ALIASES.items():
    for v in variants | {canon}:
        ALIASES_INDEX[normalizar_coluna(v)] = canon

CANON_SET = {"ITEM","DATA EVENTO","ÓRGÃO","MUNICÍPIOS","DESCRIÇÃO","VALOR ESTIMADO (R$)","ATO","Situação"}

def mapear_colunas(df: pd.DataFrame) -> pd.DataFrame:
    cols_map = {}
    for c in df.columns:
        key = normalizar_coluna(str(c))
        canon = ALIASES_INDEX.get(key)
        if canon is None:
            if key.startswith("DATA"): canon = "DATA EVENTO"
            elif key.startswith("VALOR"): canon = "VALOR ESTIMADO (R$)"
            else: canon = c
        cols_map[c] = canon
    return df.rename(columns=cols_map)

# ============ Parsing BR ============
def parse_moeda_br(x):
    if pd.isna(x): return np.nan
    if isinstance(x, (int, float, np.number)): return float(x)
    s = str(x).strip()
    if not s: return np.nan
    s = s.replace('R$', '').replace('r$', '').replace(' ',' ').strip()
    s = s.replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        m = re.findall(r"-?\d+(?:\.\d+)?", s)
        return float(m[0]) if m else np.nan

def parse_data_evento_flex(serie: pd.Series) -> pd.Series:
    s1 = pd.to_datetime(serie, errors="coerce")                # MM/DD/YYYY
    s2 = pd.to_datetime(serie, errors="coerce", dayfirst=True) # DD/MM/YYYY
    return s1.fillna(s2)

# ============ Regras de detecção de aba ============
def eh_aba_candidata(df_original: pd.DataFrame) -> bool:
    if df_original is None or df_original.empty: return False
    df_try = mapear_colunas(df_original)
    presentes = set(df_try.columns) & CANON_SET
    return len(presentes) >= 5

# ============ Leitura de Excel ============
@st.cache_data(show_spinner=False)
def read_all_sheets(file_bytes: bytes, filename: str):
    """Retorna dict{aba: DataFrame} a partir de bytes do Excel."""
    bio = io.BytesIO(file_bytes)
    try:
        return pd.read_excel(bio, engine="openpyxl", sheet_name=None)
    except Exception:
        bio.seek(0)
        return pd.read_excel(bio, sheet_name=None)

def preparar_base(df: pd.DataFrame) -> pd.DataFrame:
    df = mapear_colunas(df)
    for col in CANON_SET:
        if col not in df.columns: df[col] = np.nan
    df["DATA EVENTO"] = parse_data_evento_flex(df["DATA EVENTO"])
    df["VALOR_NUM"] = df["VALOR ESTIMADO (R$)"].apply(parse_moeda_br)
    for c in ["ITEM","ÓRGÃO","MUNICÍPIOS","DESCRIÇÃO","ATO","Situação"]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()
            df.loc[df[c].isin(["nan","None"]), c] = np.nan
    df["ANO"] = df["DATA EVENTO"].dt.year
    df["MES"] = df["DATA EVENTO"].dt.month
    df["ANO_MES"] = df["DATA EVENTO"].dt.to_period("M").astype(str)
    return df
