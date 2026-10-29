import os
import base64
import pandas as pd
import streamlit as st
from PIL import Image

# ==========================================
# 0. CAMINHOS E CONSTANTES
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join("logo-acerpit.jpg")        # logo clara, PNG transparente
FAVICON_PATH = os.path.join(BASE_DIR, "assets", "favicon.png")  # opcional: só o ícone, quadrado

COR_AZUL = "#1d4ed8"
COR_VERDE = "#16a34a"
COR_LARANJA = "#f59e0b"
COR_TEAL = "#0d9488"

# 1. Configuração da Página
st.set_page_config(
    page_title="Espresso App | Acerpit",
    page_icon=Image.open(FAVICON_PATH) if os.path.exists(FAVICON_PATH) else "🔄️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================
# 2. CARREGAMENTO DE USUÁRIOS (SECRETS)
# ==========================================
def carregar_usuarios():
    try:
        return dict(st.secrets["credentials"])
    except Exception as e:
        st.warning(f"Secrets não carregados: {e}")
        return {}


USUARIOS_CADASTRADOS = carregar_usuarios()


# ==========================================
# 3. ELEMENTOS VISUAIS (logo, ícones, helpers de HTML)
# ==========================================
@st.cache_data
def logo_html(altura=36):
    if os.path.exists(LOGO_PATH):
        ext = os.path.splitext(LOGO_PATH)[1].lower().strip(".")
        mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
        with open(LOGO_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f'<img src="data:{mime};base64,{b64}" style="height:{altura}px; width:auto;">'
    return f'<span class="logo-fallback" style="font-size:{int(altura * 0.7)}px;">ACERPIT</span>'


def svg(paths, cor="currentColor", tam=22):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{tam}" height="{tam}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{cor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        f"{paths}</svg>"
    )


ICONES = {
    "converter": '<path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>'
                 '<path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 16h5v5"/>',
    "linhas": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M3 15h18M9 4v16"/>',
    "valor": '<circle cx="12" cy="12" r="9"/><path d="M14.5 9.5c-.5-1-1.5-1.5-2.5-1.5-1.5 0-2.5.8-2.5 2s1 1.7 2.5 2 '
             '2.5.8 2.5 2-1 2-2.5 2c-1 0-2-.5-2.5-1.5M12 6v2m0 8v2"/>',
    "colunas": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18M15 3v18"/>',
}


def metrica(label, valor, cor, icone):
    # HTML sem indentação/linhas em branco (o markdown trataria como bloco de código)
    return (
        '<div class="metrica">'
        f'<div class="metrica-label">{label}</div>'
        f'<div class="metrica-valor" style="color:{cor};">{svg(ICONES[icone], cor)}<span>{valor}</span></div>'
        "</div>"
    )


def card_titulo(texto):
    st.markdown(f'<div class="card-titulo">{texto}</div>', unsafe_allow_html=True)


# ==========================================
# 4. CSS
# ==========================================
CSS_BASE = """
<style>
/* Esconde menus nativos */
#MainMenu, footer, header,
[data-testid="stToolbar"], [data-testid="stDecoration"] {display: none !important;}

/* Fundo geral cinza claro, como na outra ferramenta */
.stApp {background-color: #f1f5f9;}

[data-testid="stMainBlockContainer"], .main .block-container {
    max-width: 1280px;
    padding: 16px 28px 40px 28px;
}

/* BOTÕES PRIMÁRIOS AZUIS */
button[kind="primary"], [data-testid="stBaseButton-primary"] {
    background-color: #1d4ed8 !important;
    border-color: #1d4ed8 !important;
    color: white !important;
    font-weight: 600 !important;
}
button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {
    background-color: #1e40af !important;
    border-color: #1e40af !important;
}
button[kind="primary"] p, [data-testid="stBaseButton-primary"] p {color: white !important;}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background-color: #0b1424;
    min-width: 260px !important;
    max-width: 260px !important;
    border-right: none;
}
[data-testid="stSidebarCollapseButton"] {display: none !important;}
[data-testid="stSidebarHeader"] {display: none !important;}
[data-testid="stSidebarUserContent"] {padding: 24px 16px 0 16px;}

.sb-logo {padding: 4px 8px 22px 8px;}
.logo-fallback {color: #ffffff; font-weight: 700; letter-spacing: 4px;}

.sb-user {
    display: flex; align-items: center; gap: 10px;
    padding: 12px 10px; margin-bottom: 14px;
    border-top: 1px solid #1e293b; border-bottom: 1px solid #1e293b;
}
.sb-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    background: #1d4ed8; color: #fff; font-weight: 700;
    display: flex; align-items: center; justify-content: center; font-size: 14px;
}
.sb-nome {color: #ffffff; font-size: 14px; font-weight: 600; line-height: 1.2;}
.sb-sub {color: #94a3b8; font-size: 12px;}

.nav-item {
    display: flex; align-items: center; gap: 12px;
    padding: 11px 14px; border-radius: 8px;
    color: #cbd5e1; font-size: 14px; font-weight: 500;
}
.nav-item.ativo {background-color: #1e293b; color: #ffffff;}

/* Rodapé fixo da sidebar (equivalente ao "Minimizar" da outra ferramenta) */
.st-key-sidebar_bottom {
    position: fixed; left: 0; bottom: 0; width: 260px; box-sizing: border-box;
    padding: 14px 16px 16px 16px;
    background-color: #0b1424; border-top: 1px solid #1e293b;
}
[data-testid="stSidebar"] button {
    background-color: transparent !important;
    border: 1px solid #273449 !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] button:hover {background-color: #1e293b !important;}
[data-testid="stSidebar"] button p {color: #e2e8f0 !important;}
.sb-footer {color: #64748b; font-size: 11px; text-align: center; margin-top: 10px; line-height: 1.4;}
.sb-footer b {color: #94a3b8;}

/* ---------- ÁREA PRINCIPAL ---------- */
.topbar {display: flex; align-items: flex-end; margin-top: 4px;}
.topbar-tab {
    background: #ffffff; color: #1e293b; font-size: 14px; font-weight: 500;
    padding: 10px 18px; border-radius: 8px 8px 0 0;
}
.st-key-painel {
    background: #ffffff;
    border-radius: 0 10px 10px 10px;
    padding: 24px 28px 32px 28px;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
}
.saudacao {display: flex; align-items: center; gap: 10px; color: #334155; font-size: 14px;}
.tabs {display: flex; gap: 26px; border-bottom: 1px solid #e2e8f0; margin: 14px 0 24px 0;}
.tab {padding: 10px 0; font-size: 14px; color: #475569;}
.tab.ativa {color: #1d4ed8; font-weight: 600; border-bottom: 2px solid #1d4ed8; margin-bottom: -1px;}

/* Cards (st.container com key começando em "card_") */
[class*="st-key-card_"] {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    background: #ffffff;
    padding: 0 24px 22px 24px;
    gap: 0.75rem;
}
.card-titulo {
    font-size: 16px; font-weight: 500; color: #334155;
    padding: 16px 24px; margin: 0 -24px 6px -24px;
    border-bottom: 1px solid #e2e8f0;
}

/* Métricas */
.metrica {text-align: center; padding: 6px 0;}
.metrica-label {font-size: 13px; color: #475569; margin-bottom: 10px;}
.metrica-valor {
    display: flex; justify-content: center; align-items: center; gap: 8px;
    font-size: 26px; font-weight: 500;
}

/* Upload */
[data-testid="stFileUploaderDropzone"] {
    background-color: #f8fafc;
    border: 1.5px dashed #cbd5e1;
    border-radius: 8px;
}
</style>
"""

CSS_LOGIN = """
<style>
.stApp {background-color: #0b1424;}
[data-testid="stSidebar"] {display: none !important;}

.login-logo {text-align: center; margin-top: 8vh;}
.login-titulo {text-align: center; color: #cbd5e1; font-size: 22px; margin: 14px 0 26px 0;}

[data-testid="stForm"] {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 2rem;
    background-color: #ffffff;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
}
[data-testid="stForm"] label p {color: #1e293b !important; font-weight: 600 !important; font-size: 14px !important;}
[data-testid="stForm"] input {
    color: #0f172a !important;
    background-color: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
}
.login-rodape {text-align: center; color: #64748b; font-size: 13px; margin-top: 28px;}
.login-rodape b {color: #94a3b8;}
</style>
"""

st.markdown(CSS_BASE, unsafe_allow_html=True)


# ==========================================
# 5. SESSÃO E AUTENTICAÇÃO
# ==========================================
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = ""


def realizar_login(usuario, senha):
    user_key = usuario.strip().lower()
    if user_key in USUARIOS_CADASTRADOS and USUARIOS_CADASTRADOS[user_key] == senha:
        st.session_state["autenticado"] = True
        st.session_state["usuario_logado"] = user_key
        st.rerun()
    else:
        st.error("❌ Usuário ou senha incorretos.")


def realizar_logout():
    st.session_state["autenticado"] = False
    st.session_state["usuario_logado"] = ""
    st.session_state.pop("resultado", None)
    st.rerun()


# ==========================================
# 6. PROCESSAMENTO (regra de negócio, sem alterações)
# ==========================================
def limpar_texto(valor):
    if pd.isna(valor):
        return ""
    return str(valor).replace("\n", " ").replace("\r", "").replace(";", "-").strip()


def processar_arquivo(arquivo):
    df = pd.read_excel(arquivo, engine="openpyxl", dtype={"CPF": str})

    colunas_excluir = ["URL DO COMPROVANTE", "URL DO RELATÓRIO", "PROJETOS 2"]
    df.drop(columns=colunas_excluir, errors="ignore", inplace=True)

    mapeamento = {
        "USUÁRIO": "USUARIO", "E-MAIL": "EMAIL", "# RELATÓRIO": "NUMRELATORIO",
        "DESCRIÇÃO": "DESCRICAO", "DATA DA DESPESA": "DATA", "NÃO REEMBOLSÁVEL": "TIPO",
        "CARTÃO": "CARTAO", "DATA DE ENVIO": "DATAENVIO",
        "DATA DE APROVAÇÃO": "DATAAPROVACAO", "DATA DE CONCLUSÃO": "DATACONCLUSAO",
        "PROJETOS 1": "PROJETO1",
    }
    df.rename(columns=mapeamento, inplace=True)

    if "CPF" in df.columns:
        df["CPF"] = df["CPF"].astype(str).str.replace(r"[\.\-\s]", "", regex=True)
        df["CPF"] = df["CPF"].replace("nan", "")
        df["CPF"] = df["CPF"].apply(lambda x: x.zfill(11) if x != "" else "")

    for col in df.columns:
        if col not in ["VALOR", "CPF"]:
            df[col] = df[col].apply(limpar_texto)

    valor_total_soma = 0
    if "VALOR" in df.columns:
        df["VALOR"] = pd.to_numeric(df["VALOR"], errors="coerce").fillna(0)
        valor_total_soma = df["VALOR"].sum()
        df["VALOR"] = df["VALOR"].apply(lambda x: "{:.2f}".format(x).replace(".", ","))

    csv_resultado = df.to_csv(index=False, sep=";", encoding="utf-8-sig").encode("utf-8-sig")
    nome_base = os.path.splitext(arquivo.name)[0]

    return {
        "origem": f"{arquivo.name}-{arquivo.size}",
        "csv": csv_resultado,
        "nome_csv": f"{nome_base} EspressoApp.csv",
        "linhas": len(df),
        "colunas": len(df.columns),
        "total": valor_total_soma,
        "previa": df.head(5),
    }


# ==========================================
# 7. TELAS
# ==========================================
def tela_login():
    st.markdown(CSS_LOGIN, unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.4, 1])

    with col:
        st.markdown(
            f'<div class="login-logo">{logo_html(56)}</div>'
            '<div class="login-titulo">Conversor Espresso para ERP</div>',
            unsafe_allow_html=True,
        )
        with st.form("form_login"):
            usuario_input = st.text_input("Usuário")
            senha_input = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar", type="primary", use_container_width=True)
            if submit:
                realizar_login(usuario_input, senha_input)

    st.markdown(
        '<div class="login-rodape">Desenvolvido por <b>Acerpit Soluções Tecnológicas</b></div>',
        unsafe_allow_html=True,
    )


def montar_sidebar(nome):
    inicial = nome[:1].upper() if nome else "?"
    with st.sidebar:
        st.markdown(f'<div class="sb-logo">{logo_html(34)}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sb-user">'
            f'<div class="sb-avatar">{inicial}</div>'
            f'<div><div class="sb-nome">{nome}</div><div class="sb-sub">Usuário ativo</div></div>'
            "</div>",
            unsafe_allow_html=True,
        )
        # Para novos menus, duplique a linha abaixo (use a classe "ativo" no item atual)
        st.markdown(
            f'<div class="nav-item ativo">{svg(ICONES["converter"], tam=18)}<span>Conversor Espresso</span></div>',
            unsafe_allow_html=True,
        )

        with st.container(key="sidebar_bottom"):
            if st.button("Sair", icon=":material/logout:", use_container_width=True, key="btn_sair"):
                realizar_logout()
            st.markdown(
                '<div class="sb-footer">Desenvolvido por<br><b>Acerpit Soluções Tecnológicas</b></div>',
                unsafe_allow_html=True,
            )


def tela_principal():
    usuario = st.session_state["usuario_logado"]
    nome = usuario.replace(".", " ").replace("_", " ").title()
    montar_sidebar(nome)

    st.markdown('<div class="topbar"><span class="topbar-tab">Conversor</span></div>', unsafe_allow_html=True)

    with st.container(key="painel"):
        st.markdown(
            f'<div class="saudacao">{svg(ICONES["converter"], "#475569", 18)}'
            f"<span>Bom te ver de volta, <b>{nome}</b></span></div>"
            '<div class="tabs"><span class="tab ativa">Conversão</span></div>',
            unsafe_allow_html=True,
        )

        # --- Card 1: Seleção do arquivo ---
        with st.container(key="card_arquivo"):
            card_titulo("1. Seleção do arquivo")
            arquivo = st.file_uploader(
                "Carregue aqui o relatório (.xlsx) exportado do Espresso",
                type=["xlsx"],
            )

        if arquivo is None:
            st.session_state.pop("resultado", None)
            return

        # --- Card 2: Processamento ---
        with st.container(key="card_processamento"):
            card_titulo("2. Processamento")
            if st.button("⚡ Processar e Converter Arquivo", type="primary", use_container_width=True):
                with st.spinner("Processando dados e formatando colunas..."):
                    try:
                        st.session_state["resultado"] = processar_arquivo(arquivo)
                    except Exception as e:
                        st.session_state.pop("resultado", None)
                        st.error(f"❌ Ocorreu um erro ao processar o arquivo: {e}")

        resultado = st.session_state.get("resultado")
        if not resultado or resultado["origem"] != f"{arquivo.name}-{arquivo.size}":
            return

        # --- Card 3: Resumo ---
        total_fmt = f"R$ {resultado['total']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        with st.container(key="card_resumo"):
            card_titulo("Resumo da conversão")
            st.success("✅ Arquivo processado com sucesso!")
            c1, c2, c3 = st.columns(3)
            c1.markdown(metrica("Linhas processadas", resultado["linhas"], COR_TEAL, "linhas"), unsafe_allow_html=True)
            c2.markdown(metrica("Valor total", total_fmt, COR_VERDE, "valor"), unsafe_allow_html=True)
            c3.markdown(metrica("Colunas geradas", resultado["colunas"], COR_AZUL, "colunas"), unsafe_allow_html=True)

            with st.expander("🔍 Pré-visualizar dados tratados (Primeiras 5 linhas)"):
                st.dataframe(resultado["previa"], use_container_width=True)

        # --- Card 4: Download ---
        with st.container(key="card_download"):
            card_titulo("3. Download do resultado")
            st.download_button(
                label="📥 Baixar Planilha CSV Tratada",
                data=resultado["csv"],
                file_name=resultado["nome_csv"],
                mime="text/csv",
                type="primary",
                use_container_width=True,
            )


# ==========================================
# 8. FLUXO
# ==========================================
if not st.session_state["autenticado"]:
    tela_login()
else:
    tela_principal()