
import pandas as pd
import plotly.express as px

# ---------- Visão Geral ----------

def bar_valor_por_orgao(df: pd.DataFrame, top: int = 10):
    org = (df.groupby("ÓRGÃO")["VALOR_NUM"].sum()
           .sort_values(ascending=False).head(top).reset_index())
    fig = px.bar(
        org, x="VALOR_NUM", y="ÓRGÃO", orientation="h",
        title=f"Valor por Órgão (Top {top})",
        color="ÓRGÃO", color_discrete_sequence=px.colors.qualitative.Set2,
        labels={"VALOR_NUM":"Valor (R$)","ÓRGÃO":"Órgão"},
        text="VALOR_NUM"
    )
    fig.update_traces(texttemplate="R$ %{x:,.0f}", textposition="outside", cliponaxis=False)
    fig.update_xaxes(tickprefix="R$ ", separatethousands=True)
    fig.update_layout(showlegend=False, margin=dict(t=60, r=20, b=20, l=80))
    return fig

def donut_situacao(df: pd.DataFrame):
    pie = df["Situação"].fillna("(Sem informação)").value_counts().reset_index()
    pie.columns = ["Situação","Qtd"]
    fig = px.pie(pie, names="Situação", values="Qtd", hole=0.45,
                 title="Distribuição por Situação",
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(legend_title="")
    return fig

# ---------- Órgãos ----------

def org_top_municipios(df_org: pd.DataFrame, top_k: int = 10):
    mun_val = (df_org.groupby("MUNICÍPIOS")["VALOR_NUM"].sum()
               .sort_values(ascending=False).head(top_k).reset_index())
    fig = px.bar(
        mun_val, x="VALOR_NUM", y="MUNICÍPIOS", orientation="h",
        title=f"Top {top_k} Municípios por Valor",
        labels={"VALOR_NUM":"Valor (R$)","MUNICÍPIOS":"Município"},
        color_discrete_sequence=px.colors.qualitative.Set2,
        text="VALOR_NUM"
    )
    fig.update_traces(texttemplate="R$ %{x:,.0f}", textposition="outside", cliponaxis=False)
    fig.update_xaxes(tickprefix="R$ ", separatethousands=True)
    fig.update_layout(showlegend=False, margin=dict(t=60, r=20, b=20, l=100))
    return fig

def ato_por_municipio_stacked(df: pd.DataFrame):
    ato_mun = (df.groupby(["MUNICÍPIOS","ATO"])["VALOR_NUM"].sum()
               .reset_index())
    fig = px.bar(
        ato_mun, x="MUNICÍPIOS", y="VALOR_NUM", color="ATO", barmode="stack",
        title="Ato por Município (stacked)",
        labels={"VALOR_NUM":"Valor (R$)","MUNICÍPIOS":"Município"}
    )
    fig.update_yaxes(tickprefix="R$ ", separatethousands=True)
    fig.update_layout(legend_title="Ato", margin=dict(t=60, r=20, b=80, l=40))
    return fig

# ---------- Municípios ----------

def municipio_time_series(df_m: pd.DataFrame):
    ts = (df_m.dropna(subset=["ANO_MES"])
          .groupby("ANO_MES")["VALOR_NUM"].sum()
          .reset_index().sort_values("ANO_MES"))
    fig = px.line(
        ts, x="ANO_MES", y="VALOR_NUM", markers=True,
        title="Valor ao longo do tempo",
        labels={"ANO_MES":"Ano-Mês","VALOR_NUM":"Valor (R$)"}
    )
    fig.update_yaxes(tickprefix="R$ ", separatethousands=True)
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Valor: R$ %{y:,.2f}<extra></extra>")
    return fig

def municipio_valor_por_orgao(df_m: pd.DataFrame):
    org_m = (df_m.groupby("ÓRGÃO")["VALOR_NUM"].sum()
             .sort_values(ascending=False).reset_index())
    fig = px.bar(
        org_m, x="ÓRGÃO", y="VALOR_NUM",
        title="Valor por Órgão",
        labels={"VALOR_NUM":"Valor (R$)","ÓRGÃO":"Órgão"},
        color="ÓRGÃO", color_discrete_sequence=px.colors.qualitative.Set2,
        text="VALOR_NUM"
    )
    fig.update_traces(texttemplate="R$ %{y:,.0f}")
    fig.update_yaxes(tickprefix="R$ ", separatethousands=True)
    fig.update_layout(showlegend=False, xaxis_tickangle=-25, margin=dict(t=60, r=20, b=80, l=40))
    return fig

# ---------- Tempo ----------

def area_ato_tempo(df: pd.DataFrame):
    curve = (df.dropna(subset=["ANO_MES"]).groupby(["ANO_MES","ATO"])["VALOR_NUM"].sum()
             .reset_index().sort_values("ANO_MES"))
    fig = px.area(
        curve, x="ANO_MES", y="VALOR_NUM", color="ATO",
        title="Valor ao longo do tempo por Ato (stacked)",
        labels={"ANO_MES":"Ano-Mês","VALOR_NUM":"Valor (R$)"}
    )
    fig.update_yaxes(tickprefix="R$ ", separatethousands=True)
    return fig
