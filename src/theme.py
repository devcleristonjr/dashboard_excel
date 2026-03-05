# src/theme.py
import streamlit as st

def inject_base_css():
    """Injeta CSS para reforçar contraste e detalhes do tema."""
    CUSTOM_CSS = """
    /* Títulos com branco intenso e leve sombra para legibilidade */
    h1, h2, h3, h4, h5, h6 {
      color: #ffffff !important;
      text-shadow: 0 1px 2px rgba(0,0,0,0.25);
    }

    /* Texto geral */
    html, body, [class^="css"]  {
      color: #ffffff !important;
    }

    /* Container principal (apenas padding) */
    .block-container { padding-top: 1.5rem; }

    /* Botões com azul Steam e estados de hover */
    .stButton > button {
      background: #66c0f4 !important;
      color: #0b141c !important;           /* texto escuro para contraste no botão */
      border: 1px solid #2a475e !important;
    }
    .stButton > button:hover {
      background: #8ac9f8 !important;
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox > div > div,
    .stDateInput > div > div > input,
    .stNumberInput input {
      color: #ffffff !important;
      background: #1b2838 !important;
      border: 1px solid #2a475e !important;
    }

    /* Tabelas (dataframes) */
    .stDataFrame, .stTable {
      color: #ffffff !important;
    }

    /* Links */
    a, a:visited { color: #66c0f4 !important; }
    a:hover { color: #8ac9f8 !important; }

    /* Barra de rolagem (dark) - opcional */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: #171a21; }
    ::-webkit-scrollbar-thumb { background: #2a475e; border-radius: 8px; }
    ::-webkit-scrollbar-thumb:hover { background: #3b6a85; }
    """
    st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)


def setup_plotly_theme():
    """Configura um template Plotly com a paleta Steam."""
    try:
        import plotly.io as pio
        pio.templates["steam"] = dict(
            layout=dict(
                paper_bgcolor="#171a21",
                plot_bgcolor="#171a21",
                font=dict(color="#FFFFFF"),
                xaxis=dict(color="#FFFFFF", gridcolor="#2a475e"),
                yaxis=dict(color="#FFFFFF", gridcolor="#2a475e"),
                legend=dict(font=dict(color="#FFFFFF")),
                colorway=["#66c0f4", "#a1c3d1", "#c7d5e0", "#2a475e", "#1b2838"]
            )
        )
        pio.templates.default = "steam"
    except Exception:
        # Silencia caso Plotly não esteja instalado
        pass


def setup_altair_theme():
    """Configura um tema Altair com a paleta Steam."""
    try:
        import altair as alt
        steam_theme = {
            "config": {
                "title": {"color": "#FFFFFF"},
                "background": "#171a21",
                "axis": {"labelColor": "#FFFFFF", "titleColor": "#FFFFFF", "gridColor": "#2a475e"},
                "legend": {"labelColor": "#FFFFFF", "titleColor": "#FFFFFF"},
                "view": {"stroke": "transparent"},
                "range": {
                    "category": ["#66c0f4", "#a1c3d1", "#c7d5e0", "#2a475e", "#1b2838"]
                }
            }
        }
        alt.themes.register("steam", lambda: steam_theme)
        alt.themes.enable("steam")
    except Exception:
        pass


def setup_matplotlib_theme():
    """Configura Matplotlib com a paleta Steam."""
    try:
        import matplotlib.pyplot as plt
        plt.rcParams.update({
            "figure.facecolor": "#171a21",
            "axes.facecolor": "#171a21",
            "axes.edgecolor": "#FFFFFF",
            "axes.labelcolor": "#FFFFFF",
            "xtick.color": "#FFFFFF",
            "ytick.color": "#FFFFFF",
            "text.color": "#FFFFFF",
            "grid.color": "#2a475e",
            "savefig.facecolor": "#171a21"
        })
    except Exception:
        pass


def apply_theme():
    """
    Chame esta função no começo do app (e de cada page se rodarem isoladas).
    Ela injeta CSS e configura temas de bibliotecas de gráficos.
    """
    inject_base_css()
    setup_plotly_theme()
    setup_altair_theme()
    setup_matplotlib_theme()