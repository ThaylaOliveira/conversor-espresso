import os
import pandas as pd
import streamlit as st

# 1. Configuração da Página (Mudamos para 'wide' para aproveitar melhor a tela)
st.set_page_config(
    page_title="Espresso App | Acerpit",
    page_icon="🔄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS Personalizado (Largura expandida + Botões Azuis)
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

    /* Rodapé fixo corporativo */
    .custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        border-top: none;
        color: #64748b;
        text-align: center;
        padding: 12px 0;
        font-size: 13px;
        font-weight: 600;
        z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
st.title("🔄️ Conversor Espresso para ERP")
st.caption("Converta e padronize seus arquivos Excel (.xlsx) para CSV em instantes.")
st.markdown("---")

# --- FUNÇÃO DE LIMPEZA DE TEXTO ---
def limpar_texto(valor):
    if pd.isna(valor):
        return ""
    return str(valor).replace('\n', ' ').replace('\r', '').replace(';', '-').strip()

# --- ÁREA DE UPLOAD ---
st.subheader("1. Seleção do Arquivo")
arquivo_carregado = st.file_uploader(
    "Carregue aqui o relatório (.xlsx) exportado do Espresso",
    type=["xlsx"]
)

if arquivo_carregado is not None:
    st.markdown("---")
    st.subheader("2. Processamento")
    
    # Botão de ação
    if st.button("⚡ Processar e Converter Arquivo", type="primary", use_container_width=True):
        with st.spinner("Processando dados e formatando colunas..."):
            try:
                # Lendo o Excel garantindo CPF como string
                df = pd.read_excel(arquivo_carregado, engine='openpyxl', dtype={'CPF': str})

                # 1. Remoção de colunas específicas
                colunas_excluir = ['URL DO COMPROVANTE', 'URL DO RELATÓRIO', 'PROJETOS 2']
                df.drop(columns=colunas_excluir, errors='ignore', inplace=True)

                # 2. Mapeamento de Colunas
                mapeamento = {
                    'USUÁRIO': 'USUARIO', 'E-MAIL': 'EMAIL', '# RELATÓRIO': 'NUMRELATORIO',
                    'DESCRIÇÃO': 'DESCRICAO', 'DATA DA DESPESA': 'DATA', 'NÃO REEMBOLSÁVEL': 'TIPO', 
                    'CARTÃO': 'CARTAO', 'DATA DE ENVIO': 'DATAENVIO', 
                    'DATA DE APROVAÇÃO': 'DATAAPROVACAO', 'DATA DE CONCLUSÃO': 'DATACONCLUSAO', 
                    'PROJETOS 1': 'PROJETO1'
                }
                df.rename(columns=mapeamento, inplace=True)

                # 3. Tratamento de CPF (11 dígitos)
                if 'CPF' in df.columns:
                    df['CPF'] = df['CPF'].astype(str).str.replace(r'[\.\-\s]', '', regex=True)
                    df['CPF'] = df['CPF'].replace('nan', '')
                    df['CPF'] = df['CPF'].apply(lambda x: x.zfill(11) if x != "" else "")

                # 4. Limpeza Geral dos Textos
                for col in df.columns:
                    if col not in ['VALOR', 'CPF']:
                        df[col] = df[col].apply(limpar_texto)

                # Guarda o valor numérico para métricas
                valor_total_soma = 0
                if 'VALOR' in df.columns:
                    df['VALOR'] = pd.to_numeric(df['VALOR'], errors='coerce').fillna(0)
                    valor_total_soma = df['VALOR'].sum()
                    df['VALOR'] = df['VALOR'].apply(lambda x: "{:.2f}".format(x).replace('.', ','))

                # 5. Converte o Dataframe em CSV em memória
                csv_resultado = df.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')

                nome_base = os.path.splitext(arquivo_carregado.name)[0]
                nome_csv_saida = f"{nome_base} EspressoApp.csv"

                st.success("✅ Arquivo processado com sucesso!")
                
                # RÉGUA DE MÉTRICAS (KPIs)
                c1, c2 = st.columns(2)
                c1.metric("Linhas Processadas", len(df))
                c2.metric("Valor Total", f"R$ {valor_total_soma:,.2f}".replace('.', 'X').replace(',', '.').replace('X', ','))

                # PRÉ-VISUALIZAÇÃO DA TABELA NATIVA
                with st.expander("🔍 Pré-visualizar dados tratados (Primeiras 5 linhas)"):
                    st.dataframe(df.head(5), use_container_width=True)

                st.markdown("---")
                st.subheader("3. Download do Resultado")
                
                # BOTÃO DE DOWNLOAD
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