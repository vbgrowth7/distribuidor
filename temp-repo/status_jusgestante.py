import streamlit as st
import pandas as pd
from datetime import datetime
from db_connection import testar_conexao, obter_dados, executar_query, selecionar_banco

# Configuração da página
st.set_page_config(
    page_title="STATUS JUSGESTANTE",
    page_icon="👩‍⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Implementar cache para melhorar o desempenho
@st.cache_data(ttl=300)  # Cache por 5 minutos
def carregar_dados_jusgestante():
    """Carrega dados da tabela FILA_VENDEDORES_JUSGESTANTE com cache"""
    query = "SELECT * FROM FILA_VENDEDORES_JUSGESTANTE"
    return obter_dados(query)

# Função para atualizar o status com invalidação de cache
def atualizar_status(nome, novo_status):
    """Atualiza o status de um registro na tabela FILA_VENDEDORES_JUSGESTANTE pelo nome"""
    query = "UPDATE FILA_VENDEDORES_JUSGESTANTE SET Status = %s WHERE Name = %s"
    sucesso, mensagem = executar_query(query, (novo_status, nome))
    
    # Invalidar o cache de dados quando houver atualização
    if sucesso:
        carregar_dados_jusgestante.clear()
    
    return sucesso, mensagem

# Estilo personalizado para tema escuro e layout similar ao da imagem
st.markdown("""
<style>
    /* Estilo geral e cores */
    .stApp {
        background-color: #141E33;
        color: white;
    }
    
    .main-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: white;
        padding: 10px 0;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        padding: 5px 0;
    }
    
    /* Estilos para painéis laterais e cards */
    .side-card {
        background-color: #1B2640;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    
    /* Estilos para status */
    .status-disponivel {
        display: inline-block;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 5px 15px;
        border-radius: 20px;
        text-align: center;
        min-width: 120px;
    }
    
    .status-indisponivel {
        display: inline-block;
        background-color: #FF3B3B;
        color: white;
        font-weight: bold;
        padding: 5px 15px;
        border-radius: 20px;
        text-align: center;
        min-width: 120px;
    }
    
    /* Tabela de dados */
    .dataframe {
        width: 100%;
        background-color: #1B2640;
        color: white;
        border-collapse: collapse;
    }
    
    .dataframe th {
        background-color: #141E33;
        color: #8B93A7;
        text-align: left;
        padding: 12px;
    }
    
    .dataframe td {
        padding: 10px;
        border-bottom: 1px solid #2D3958;
    }
    
    /* Botões */
    .primary-button {
        background-color: #1B2640;
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 5px;
        cursor: pointer;
        text-align: center;
        font-weight: bold;
    }
    
    .action-button {
        background-color: #6B50A3;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
        min-width: 100px;
        text-align: center;
        display: inline-block;
        margin: 2px;
    }
    
    .update-button {
        background-color: #1B2640;
        color: white;
        border: 1px solid #2D3958;
        padding: 8px 15px;
        border-radius: 5px;
        cursor: pointer;
        text-align: center;
        font-weight: bold;
        width: 100%;
    }
    
    .update-button:hover {
        background-color: #2D3958;
    }
    
    /* Progress bar personalizada */
    .progress-container {
        width: 100%;
        background-color: #2D3958;
        border-radius: 5px;
        margin: 5px 0;
    }
    
    .progress-disponivel {
        background-color: #4CAF50;
        height: 8px;
        border-radius: 5px;
    }
    
    .progress-indisponivel {
        background-color: #9A3B95;
        height: 8px;
        border-radius: 5px;
    }
    
    /* Campos de busca */
    .stTextInput > div > div > input {
        background-color: #1B2640;
        color: white;
        border: 1px solid #2D3958;
        border-radius: 5px;
    }
    
    /* Estilo para seletores */
    .stSelectbox > div > div > div {
        background-color: #1B2640;
        color: white;
        border: 1px solid #2D3958;
    }
    
    .stSelectbox > div > div > div > div {
        background-color: #1B2640;
        color: white;
    }
    
    /* Barra superior */
    .topnav {
        background-color: #141E33;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        border-bottom: 1px solid #2D3958;
    }
    
    .logo {
        display: flex;
        align-items: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .logo-circle {
        width: 30px;
        height: 30px;
        background-color: #9A3B95;
        border-radius: 50%;
        margin-right: 10px;
    }
    
    .topnav-links {
        display: flex;
    }
    
    .topnav-link {
        color: white;
        margin-left: 20px;
        text-decoration: none;
        padding: 5px 10px;
    }
    
    /* Última atualização */
    .last-update {
        background-color: #1B2640;
        color: white;
        padding: 8px 15px;
        border-radius: 5px;
        font-size: 0.9rem;
    }
    
    /* Estilos para os botões do Streamlit */
    div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
        border-radius: 5px;
        background-color: #1B2640;
        color: white;
        border: 1px solid #2D3958;
        font-weight: bold;
        padding: 10px;
    }
    
    /* Ocultar estilo padrão de botão do Streamlit */
    div.stButton > button {
        width: 100%;
        border-radius: 5px;
        background-color: #1B2640;
        color: white;
        border: 1px solid #2D3958;
        font-weight: bold;
    }
    
    div.stButton > button[data-baseweb="button"] {
        width: 100%;
        background-color: #1B2640 !important;
        color: white !important;
        border: 1px solid #2D3958 !important;
    }
    
    /* Atualizar button */
    div.stButton > button[data-baseweb="button"].css-1cpxqw2 {
        background-color: #1B2640 !important;
        color: white !important;
        border: 1px solid #2D3958 !important;
        margin-top: 15px;
    }
    
    /* Destacar botão selecionado */
    div[data-testid="stHorizontalBlock"] button[kind="secondary"].selected-disponivel {
        background-color: #4CAF50 !important;
        color: white !important;
        border: none !important;
    }
    
    div[data-testid="stHorizontalBlock"] button[kind="secondary"].selected-indisponivel {
        background-color: #FF3B3B !important;
        color: white !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Função auxiliar para formatar status
def formatar_status_html(status):
    status_str = str(status).upper()
    if status_str in ["DISPONÍVEL", "DISPONIVEL"]:
        return f'<div class="status-disponivel">DISPONÍVEL</div>'
    else:
        return f'<div class="status-indisponivel">INDISPONÍVEL</div>'

# Conectar ao banco de dados com cache
@st.cache_resource(ttl=3600)  # Cache por 1 hora
def conectar_banco():
    sucesso, mensagem = testar_conexao()
    if sucesso:
        selecionar_banco("BITRIX24_FILAS_JUSGESTANTE")
    return sucesso, mensagem

# Inicialização do aplicativo - executado apenas uma vez
if 'inicializado' not in st.session_state:
    sucesso, mensagem = conectar_banco()
    if not sucesso:
        st.error(f"Falha na conexão com o banco de dados: {mensagem}")
        st.stop()
    st.session_state.inicializado = True
    st.session_state.atualizar_dados = True

# Barra superior personalizada
st.markdown("""
<div class="topnav">
    <div class="logo">
        <div class="logo-circle"></div>
        STATUS JUSGESTANTE
    </div>
    <div class="topnav-links">
        <div class="topnav-link">Dashboard</div>
        <div class="topnav-link">Configurações</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Layout principal com colunas
col1, col2 = st.columns([1, 3])

# Só carrega os dados quando necessário
if 'dados_df' not in st.session_state or st.session_state.atualizar_dados:
    with st.spinner("Carregando dados..."):
        st.session_state.dados_df = carregar_dados_jusgestante()
        st.session_state.atualizar_dados = False

df = st.session_state.dados_df
if df.empty:
    st.warning("Não foram encontrados registros na tabela FILA_VENDEDORES_JUSGESTANTE.")
    st.stop()

# Coluna 1 (Painel lateral) - Agente, Total, Disponíveis, Indisponíveis
with col1:
    # Card Agente
    st.markdown('<div class="side-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">AGENTE</div>', unsafe_allow_html=True)
    
    # Lista de nomes para selecionar
    names = df['Name'].unique().tolist()
    # names.insert(0, "Selecione um agente") - Removendo opção default para simular a imagem de referência
    selected_name = st.selectbox("", names, label_visibility="collapsed")

    # Se um agente foi selecionado, mostra opções de status e botão atualizar
    if selected_name:
        # Obter o status atual do agente selecionado - usando o DataFrame já em memória
        status_atual = df[df['Name'] == selected_name]['Status'].iloc[0].upper() if not df[df['Name'] == selected_name].empty else "INDISPONÍVEL"
        
        # STATUS
        st.markdown('<div class="section-header" style="margin-top: 15px;">STATUS</div>', unsafe_allow_html=True)
        
        # Define o status inicial baseado no status atual
        if 'status_selecionado' not in st.session_state:
            st.session_state.status_selecionado = status_atual
            
        # Quando o usuário seleciona um novo agente, atualiza o status
        if 'nome_anterior' not in st.session_state:
            st.session_state.nome_anterior = selected_name
        elif st.session_state.nome_anterior != selected_name:
            st.session_state.status_selecionado = status_atual
            st.session_state.nome_anterior = selected_name
            
        # Função para selecionar status via callback
        def selecionar_status(status):
            st.session_state.status_selecionado = status
        
        # Estilo simplificado para os botões de status
        st.markdown("""
        <style>
        /* Estilo para os botões de status */
        div.status-area {
            margin-bottom: 20px;
        }
        
        div.status-button {
            padding: 10px;
            text-align: center;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            background-color: #1B2640;
            color: white;
            border: 1px solid #2D3958;
            margin-bottom: 10px;
        }
        
        div.status-badge {
            display: inline-block;
            background-color: #FF3B3B;
            color: white;
            font-weight: bold;
            padding: 5px 15px;
            border-radius: 15px;
            margin-left: 5px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Implementação com botões nativos do Streamlit separadamente
        status_col1, status_col2 = st.columns(2)
        
        with status_col1:
            disp_btn = st.button("DISPONÍVEL", key="disponivel", 
                               on_click=selecionar_status, 
                               args=("DISPONÍVEL",))
            
        with status_col2:
            indisp_btn = st.button("INDISPONÍVEL", key="indisponivel", 
                                 on_click=selecionar_status, 
                                 args=("INDISPONÍVEL",))
        
        # Aplicar estilos personalizados diretamente via CSS injetado
        st.markdown("""
        <style>
        /* Estilizando os botões Streamlit com fundo escuro */
        div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
            background-color: #1B2640 !important;
            color: white !important;
            border: 1px solid #2D3958 !important;
            border-radius: 5px;
            font-weight: bold;
        }
        
        /* Destacar botão selecionado */
        div[data-testid="stHorizontalBlock"] button[kind="secondary"].selected-disponivel {
            background-color: #4CAF50 !important;
            color: white !important;
            border: none !important;
        }
        
        div[data-testid="stHorizontalBlock"] button[kind="secondary"].selected-indisponivel {
            background-color: #FF3B3B !important;
            color: white !important;
            border: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Aplicar estilo de botão selecionado via JavaScript
        st.markdown(f"""
        <script>
            // Função para encontrar e estilizar botões após o DOM ser carregado
            document.addEventListener('DOMContentLoaded', function() {{
                // Pequeno atraso para garantir que o DOM foi renderizado
                setTimeout(function() {{
                    // Obter todos os botões
                    var buttons = document.querySelectorAll('button[kind="secondary"]');
                    
                    // Aplicar estilos com base no status selecionado
                    buttons.forEach(function(button) {{
                        if (button.innerText === 'DISPONÍVEL') {{
                            if ('{st.session_state.status_selecionado}' === 'DISPONÍVEL') {{
                                button.classList.add('selected-disponivel');
                            }} else {{
                                button.classList.remove('selected-disponivel');
                            }}
                        }}
                        
                        if (button.innerText === 'INDISPONÍVEL') {{
                            if ('{st.session_state.status_selecionado}' === 'INDISPONÍVEL') {{
                                button.classList.add('selected-indisponivel');
                            }} else {{
                                button.classList.remove('selected-indisponivel');
                            }}
                        }}
                    }});
                }}, 200);
            }});
        </script>
        """, unsafe_allow_html=True)
        
        # Status selecionado com badge
        status_color = "#4CAF50" if st.session_state.status_selecionado == "DISPONÍVEL" else "#FF3B3B"
        st.markdown(f"""
        <div style="margin: 10px 0; display: flex; align-items: center;">
            <span>Status selecionado: </span>
            <span style="background-color: {status_color}; color: white; border-radius: 15px; padding: 2px 10px; margin-left: 5px; font-weight: bold;">{st.session_state.status_selecionado}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Botão Atualizar
        if st.button("Atualizar", key="atualizar_btn", use_container_width=True):
            with st.spinner(f"Atualizando status de {selected_name} para {st.session_state.status_selecionado}..."):
                sucesso, mensagem = atualizar_status(selected_name, st.session_state.status_selecionado)
                if sucesso:
                    st.success(f"Status de {selected_name} atualizado para {st.session_state.status_selecionado} com sucesso!")
                    # Marcar que os dados precisam ser atualizados
                    st.session_state.atualizar_dados = True
                    # Rerun otimizado para atualizar apenas o necessário
                    st.rerun()
                else:
                    st.error(f"Erro ao atualizar status: {mensagem}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Otimizações adicionais para consultas SQL
    @st.cache_data(ttl=60)  # Cache por 1 minuto
    def contar_status():
        """Obtém contagens de status diretamente via SQL para melhor desempenho"""
        query_disponiveis = """
        SELECT COUNT(DISTINCT Name) as count 
        FROM FILA_VENDEDORES_JUSGESTANTE 
        WHERE UPPER(Status) IN ('DISPONÍVEL', 'DISPONIVEL')
        """
        
        query_indisponiveis = """
        SELECT COUNT(DISTINCT Name) as count 
        FROM FILA_VENDEDORES_JUSGESTANTE 
        WHERE UPPER(Status) IN ('INDISPONÍVEL', 'INDISPONIVEL')
        """
        
        query_total = """
        SELECT COUNT(DISTINCT Name) as count 
        FROM FILA_VENDEDORES_JUSGESTANTE
        """
        
        disponiveis = obter_dados(query_disponiveis).iloc[0]['count'] if not obter_dados(query_disponiveis).empty else 0
        indisponiveis = obter_dados(query_indisponiveis).iloc[0]['count'] if not obter_dados(query_indisponiveis).empty else 0
        total = obter_dados(query_total).iloc[0]['count'] if not obter_dados(query_total).empty else 0
        
        return total, disponiveis, indisponiveis

    # Cálculos de estatísticas otimizados usando consulta SQL direta
    if 'status_counts' not in st.session_state or st.session_state.atualizar_dados:
        total_agentes, disponiveis, indisponiveis = contar_status()
        porcentagem_disponiveis = int((disponiveis / total_agentes) * 100) if total_agentes > 0 else 0
        porcentagem_indisponiveis = int((indisponiveis / total_agentes) * 100) if total_agentes > 0 else 0
        
        st.session_state.status_counts = {
            'total': total_agentes,
            'disponiveis': disponiveis,
            'indisponiveis': indisponiveis,
            'porcentagem_disponiveis': porcentagem_disponiveis,
            'porcentagem_indisponiveis': porcentagem_indisponiveis
        }
    else:
        total_agentes = st.session_state.status_counts['total']
        disponiveis = st.session_state.status_counts['disponiveis']
        indisponiveis = st.session_state.status_counts['indisponiveis']
        porcentagem_disponiveis = st.session_state.status_counts['porcentagem_disponiveis']
        porcentagem_indisponiveis = st.session_state.status_counts['porcentagem_indisponiveis']
    
    # Card Total de Agentes
    st.markdown('<div class="side-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">Total de Agentes</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 2.5rem; font-weight: bold; text-align: left;">{total_agentes}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Card Disponíveis
    st.markdown('<div class="side-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">Disponíveis</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 2.5rem; font-weight: bold; text-align: left;">{disponiveis}</div>', unsafe_allow_html=True)
    
    # Barra de progresso para disponíveis
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-disponivel" style="width: {porcentagem_disponiveis}%;"></div>
    </div>
    <div style="text-align: right;">{porcentagem_disponiveis}%</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Card Indisponíveis
    st.markdown('<div class="side-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">Indisponíveis</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size: 2.5rem; font-weight: bold; text-align: left;">{indisponiveis}</div>', unsafe_allow_html=True)
    
    # Barra de progresso para indisponíveis
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-indisponivel" style="width: {porcentagem_indisponiveis}%;"></div>
    </div>
    <div style="text-align: right;">{porcentagem_indisponiveis}%</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Coluna 2 (Conteúdo principal) - Tabela e detalhes
with col2:
    # Cabeçalho e última atualização
    col_header1, col_header2 = st.columns([3, 1])
    
    with col_header1:
        st.markdown('<div class="main-header">Controle de Fila</div>', unsafe_allow_html=True)
    
    with col_header2:
        # Formatação da data atual no estilo DD/MM/YYYY HH:MM:SS
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        st.markdown(f'<div class="last-update">Última atualização: {data_atual}</div>', unsafe_allow_html=True)
    
    # Painel principal para a tabela
    st.markdown('<div class="side-card" style="padding-bottom: 25px;">', unsafe_allow_html=True)
    
    # Campo de busca para a tabela
    busca = st.text_input("Buscar agente...", key="busca_agente")
    
    # Otimização: armazenar em cache a busca anterior
    if 'busca_anterior' not in st.session_state:
        st.session_state.busca_anterior = ""
    
    # Otimização: só processa a tabela se os dados ou a busca mudarem
    if 'df_display_html' not in st.session_state or st.session_state.busca_anterior != busca or st.session_state.atualizar_dados:
        # Preparar os dados da tabela
        df_display = df.copy()
        
        # Aplicar filtro de busca se houver
        if busca:
            filtro = busca.lower()
            mask = False
            # Aplicar o filtro em todas as colunas que contêm texto
            for col in df_display.columns:
                try:
                    mask = mask | df_display[col].astype(str).str.lower().str.contains(filtro)
                except:
                    pass
            df_display = df_display[mask]
        
        # Aplicar formatação ao status
        df_display['Status_HTML'] = df_display['Status'].apply(formatar_status_html)
        
        # Substituir a coluna Status original pela versão formatada em HTML
        # Primeiro, vamos identificar todas as colunas exceto a coluna Status original
        colunas_exibir = [col for col in df_display.columns if col != 'Status']
        
        # Garantir que Status_HTML está entre as colunas a exibir
        if 'Status_HTML' not in colunas_exibir:
            colunas_exibir.append('Status_HTML')
        
        # Renomear colunas para exibição mais amigável
        rename_cols = {
            'Name': 'NOME',
            'Status_HTML': 'STATUS',  # Esta será a única coluna de status exibida
            'ID': 'ID',
            # Adicione outros mapeamentos conforme necessário
        }
        
        # Filtrar apenas os mapeamentos que existem no dataframe
        rename_cols_filtered = {k: v for k, v in rename_cols.items() if k in colunas_exibir}
        
        # Renomear colunas para exibição
        df_temp = df_display[colunas_exibir].rename(columns=rename_cols_filtered)
        
        # Exibir a tabela com formatação HTML
        st.session_state.df_display_html = df_temp.to_html(escape=False, index=False)
        st.session_state.busca_anterior = busca
    
    # Usar a tabela HTML em cache
    st.markdown(st.session_state.df_display_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True) 