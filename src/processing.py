
from typing import List, Tuple
import pandas as pd
from src.data_io import read_all_sheets, eh_aba_candidata, preparar_base

def consolidate_files(uploaded_files: List) -> Tuple[pd.DataFrame, list]:
    """
    uploaded_files: lista de UploadedFile do Streamlit
    Retorna (base_consolidada, logs)
    """
    frames, logs = [], []
    for f in uploaded_files:
        try:
            sheets = read_all_sheets(f.read(), f.name)
            usadas = []
            for aba, df in sheets.items():
                if eh_aba_candidata(df):
                    df2 = preparar_base(df.copy())
                    df2["__ARQUIVO__"] = f.name
                    df2["__ABA__"] = aba
                    frames.append(df2)
                    usadas.append(aba)
            if usadas:
                logs.append(f"✅ {f.name}: abas usadas → {', '.join(usadas)}")
            else:
                logs.append(f"⚠️ {f.name}: nenhuma aba com as colunas esperadas.")
        except Exception as e:
            logs.append(f"❌ Erro ao ler {f.name}: {e}")
    if frames:
        base = pd.concat(frames, ignore_index=True)
        logs.append(f"📦 Consolidado: {len(base)} linhas | {base['__ARQUIVO__'].nunique()} arquivo(s) | {base['__ABA__'].nunique()} aba(s)")
        return base, logs
    return pd.DataFrame(), logs

def apply_filters(base: pd.DataFrame, periodo, org_sel, mun_sel, ato_sel, sit_sel, busca: str) -> pd.DataFrame:
    if base is None or base.empty: return pd.DataFrame()
    m = pd.Series(True, index=base.index)
    if periodo:
        m &= base["DATA EVENTO"].between(periodo[0], periodo[1], inclusive="both")
    def apl(col, vals):
        return base[col].isin(vals) if vals else pd.Series(True, index=base.index)
    m &= apl("ÓRGÃO", org_sel)
    m &= apl("MUNICÍPIOS", mun_sel)
    m &= apl("ATO", ato_sel)
    m &= apl("Situação", sit_sel)
    if busca and busca.strip():
        import re as _re
        q = busca.strip().lower()
        m &= base["DESCRIÇÃO"].fillna("").str.lower().str.contains(_re.escape(q))
    return base[m].copy()
