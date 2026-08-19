import os
import json
import pandas as pd
import streamlit as st

# 1. Configuração da Página
st.set_page_config(
    page_title="Espresso App | Acerpit",
    page_icon="🔄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CARREGAMENTO DINÂMICO DE USUÁRIOS (JSON)
def carregar_usuarios():
    caminho_json = "usuarios.json"
    if os.path.exists(caminho_json):
        try:
            with open(caminho_json, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Erro ao carregar banco de usuários: {e}")
            return {}
    else:
        # Retorna dicionário vazio para não expor credenciais no código público
        return {}

USUARIOS_CADASTRADOS = carregar_usuarios()

# 3. CSS Personalizado (Corrigido para Dark/Light Mode)
st.markdown("""
    <style>
    /* Esconde menus desnecessários */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Controla a largura máxima da aplicação e centraliza */
    .main .block-container {
        max-width: 1000px;
        margin: 0 auto;
        padding-bottom: 80px;
        padding-top: 30px;
    }

    /* FORÇA A COR AZUL NOS BOTÕES PRIMÁRIOS */
    button[kind="primary"] {
        background-color: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
        color: white !important;
        font-weight: 600 !important;
    }

    button[kind="primary"]:hover {
        background-color: #1e40af !important;
        border-color: #1e40af !important;
    }

    /* Form do Login */
    [data-testid="stForm"] {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 2rem;
        background-color: #ffffff;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* AJUSTE DAS CORES DOS TEXTOS/LABELS DENTRO DO FORMULÁRIO */
    [data-testid="stForm"] label p {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* AJUSTE DOS INPUTS DE TEXTO */
    [data-testid="stForm"] input {
        color: #0f172a !important;
        background-color: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
    }

    /* Rodapé fixo corporativo */
    .custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        border-top: none;
        color: #94a3b8;
        text-align: center;
        padding: 12px 0;
        font-size: 13px;
        font-weight: 600;
        z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# 4. GERENCIAMENTO DE SESSÃO E AUTENTICAÇÃO
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'usuario_logado' not in st.session_state:
    st.session_state['usuario_logado'] = ""

def realizar_login(usuario, senha):
    user_key = usuario.strip().lower()
    if user_key in USUARIOS_CADASTRADOS and USUARIOS_CADASTRADOS[user_key] == senha:
        st.session_state['autenticado'] = True
        st.session_state['usuario_logado'] = user_key
        st.rerun()
    else:
        st.error("❌ Usuário ou senha incorretos.")

def realizar_logout():
    st.session_state['autenticado'] = False
    st.session_state['usuario_logado'] = ""
    st.rerun()

def limpar_texto(valor):
    if pd.isna(valor):
        return ""
    return str(valor).replace('\n', ' ').replace('\r', '').replace(';', '-').strip()

# ==========================================
# 5. FLUXO DE TELAS
# ==========================================

# --- TELA 1: LOGIN ---
if not st.session_state['autenticado']:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("##")            
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 30px; margin-top: 10px;'>🔄️ Conversor Espresso para ERP</p>", unsafe_allow_html=True)
        st.write("")

        with st.form("form_login"):
            usuario_input = st.text_input("Usuário")
            senha_input = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar", type="primary", use_container_width=True)

            if submit:
                realizar_login(usuario_input, senha_input)

# --- TELA 2: APLICAÇÃO PRINCIPAL ---
else:
    col_titulo, col_logout = st.columns([5, 1])
    with col_titulo:
        st.title("🔄️ Conversor Espresso para ERP")
        st.caption(f"Usuário ativo: **{st.session_state['usuario_logado']}** | Padronização de arquivos para o ERP")
    with col_logout:
        st.write("##")
        if st.button("Sair", use_container_width=True):
            realizar_logout()

    st.markdown("---")

    st.subheader("1. Seleção do Arquivo")
    arquivo_carregado = st.file_uploader(
        "Carregue aqui o relatório (.xlsx) exportado do Espresso",
        type=["xlsx"]
    )

    if arquivo_carregado is not None:
        st.markdown("---")
        st.subheader("2. Processamento")
        
        if st.button("⚡ Processar e Converter Arquivo", type="primary", use_container_width=True):
            with st.spinner("Processando dados e formatando colunas..."):
                try:
                    df = pd.read_excel(arquivo_carregado, engine='openpyxl', dtype={'CPF': str})

                    colunas_excluir = ['URL DO COMPROVANTE', 'URL DO RELATÓRIO', 'PROJETOS 2']
                    df.drop(columns=colunas_excluir, errors='ignore', inplace=True)

                    mapeamento = {
                        'USUÁRIO': 'USUARIO', 'E-MAIL': 'EMAIL', '# RELATÓRIO': 'NUMRELATORIO',
                        'DESCRIÇÃO': 'DESCRICAO', 'DATA DA DESPESA': 'DATA', 'NÃO REEMBOLSÁVEL': 'TIPO', 
                        'CARTÃO': 'CARTAO', 'DATA DE ENVIO': 'DATAENVIO', 
                        'DATA DE APROVAÇÃO': 'DATAAPROVACAO', 'DATA DE CONCLUSÃO': 'DATACONCLUSAO', 
                        'PROJETOS 1': 'PROJETO1'
                    }
                    df.rename(columns=mapeamento, inplace=True)

                    if 'CPF' in df.columns:
                        df['CPF'] = df['CPF'].astype(str).str.replace(r'[\.\-\s]', '', regex=True)
                        df['CPF'] = df['CPF'].replace('nan', '')
                        df['CPF'] = df['CPF'].apply(lambda x: x.zfill(11) if x != "" else "")

                    for col in df.columns:
                        if col not in ['VALOR', 'CPF']:
                            df[col] = df[col].apply(limpar_texto)

                    valor_total_soma = 0
                    if 'VALOR' in df.columns:
                        df['VALOR'] = pd.to_numeric(df['VALOR'], errors='coerce').fillna(0)
                        valor_total_soma = df['VALOR'].sum()
                        df['VALOR'] = df['VALOR'].apply(lambda x: "{:.2f}".format(x).replace('.', ','))

                    csv_resultado = df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')

                    nome_base = os.path.splitext(arquivo_carregado.name)[0]
                    nome_csv_saida = f"{nome_base} EspressoApp.csv"

                    st.success("✅ Arquivo processado com sucesso!")
                    
                    c1, c2 = st.columns(2)
                    c1.metric("Linhas Processadas", len(df))
                    c2.metric("Valor Total", f"R$ {valor_total_soma:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ','))

                    with st.expander("🔍 Pré-visualizar dados tratados (Primeiras 5 linhas)"):
                        st.dataframe(df.head(5), use_container_width=True)

                    st.markdown("---")
                    st.subheader("3. Download do Resultado")
                    
                    st.download_button(
                        label="📥 Baixar Planilha CSV Tratada",
                        data=csv_resultado,
                        file_name=nome_csv_saida,
                        mime="text/csv",
                        type="primary",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"❌ Ocorreu um erro ao processar o arquivo: {e}")

# --- RODAPÉ FIXO CORPORATIVO ---
st.markdown(
    """
    <div class="custom-footer">
        Desenvolvido por <strong>Acerpit Soluções Tecnológicas</strong>
    </div>
    """, 
    unsafe_allow_html=True
)