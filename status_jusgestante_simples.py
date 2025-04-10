import streamlit as st
import pandas as pd
from db_connection import testar_conexao, obter_dados, executar_query

# Configuração da página
st.set_page_config(
    page_title="STATUS JUSGESTANTE",
    page_icon="👩‍⚕️",
    layout="wide",
)

# Estilo personalizado para centralizar títulos e melhorar a aparência
st.markdown("""
<style>
    .main-header {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 30px;
        color: #1E88E5;
    }
    .status-pendente {
        color: #FFA000;
        font-weight: bold;
    }
    .status-andamento {
        color: #1976D2;
        font-weight: bold;
    }
    .status-concluido {
        color: #388E3C;
        font-weight: bold;
    }
    .status-cancelado {
        color: #D32F2F;
        font-weight: bold;
    }
    .dataframe {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='main-header'>STATUS JUSGESTANTE</h1>", unsafe_allow_html=True)

# Função para carregar os dados da tabela JUSGESTANTE
def carregar_dados_jusgestante():
    """Carrega dados da tabela JUSGESTANTE"""
    query = "SELECT id, nome, status FROM JUSGESTANTE ORDER BY nome"
    return obter_dados(query)

# Função para atualizar o status
def atualizar_status(id, novo_status):
    """Atualiza o status de um registro na tabela JUSGESTANTE"""
    query = "UPDATE JUSGESTANTE SET status = %s WHERE id = %s"
    sucesso, mensagem = executar_query(query, (novo_status, id))
    return sucesso, mensagem

# Verifica a conexão com o banco
with st.spinner("Conectando ao banco de dados..."):
    sucesso, mensagem = testar_conexao()
    
    if not sucesso:
        st.error(f"Falha na conexão com o banco de dados: {mensagem}")
        st.stop()

# Carrega os dados
with st.spinner("Carregando dados..."):
    df = carregar_dados_jusgestante()
    
    if df.empty:
        st.warning("Não foram encontrados registros na tabela JUSGESTANTE ou a tabela não existe.")
        st.stop()

# Filtro de pesquisa por nome
filtro_nome = st.text_input("Pesquisar por nome:", "")

# Aplica o filtro se necessário
if filtro_nome:
    df_filtrado = df[df['nome'].str.contains(filtro_nome, case=False)]
else:
    df_filtrado = df

# Define um índice para o status atual
def get_status_index(status):
    status_list = ["PENDENTE", "EM ANDAMENTO", "CONCLUÍDO", "CANCELADO"]
    return status_list.index(status) if status in status_list else 0

# Função para formatar o status com cor
def formatar_status(status):
    if status == "PENDENTE":
        return f"<span class='status-pendente'>{status}</span>"
    elif status == "EM ANDAMENTO":
        return f"<span class='status-andamento'>{status}</span>"
    elif status == "CONCLUÍDO":
        return f"<span class='status-concluido'>{status}</span>"
    elif status == "CANCELADO":
        return f"<span class='status-cancelado'>{status}</span>"
    return status

# Cria tabela de dados com colunas para ações
st.write("### Lista de Cadastros")

# Colunas
colunas = st.columns([3, 2, 2])
with colunas[0]:
    st.write("**Nome**")
with colunas[1]:
    st.write("**Status Atual**")
with colunas[2]:
    st.write("**Alterar Status**")

st.markdown("<hr style='margin: 5px 0px'>", unsafe_allow_html=True)

# Listagem dos registros
for i, row in df_filtrado.iterrows():
    colunas = st.columns([3, 2, 2])
    
    with colunas[0]:
        st.write(row['nome'])
    
    with colunas[1]:
        st.markdown(formatar_status(row['status']), unsafe_allow_html=True)
    
    with colunas[2]:
        status_options = ["PENDENTE", "EM ANDAMENTO", "CONCLUÍDO", "CANCELADO"]
        col1, col2 = st.columns([3, 1])
        
        with col1:
            novo_status = st.selectbox(
                "",
                options=status_options,
                key=f"status_{row['id']}",
                index=get_status_index(row['status'])
            )
        
        with col2:
            if st.button("Atualizar", key=f"btn_{row['id']}"):
                with st.spinner("Atualizando..."):
                    sucesso, mensagem = atualizar_status(row['id'], novo_status)
                    if sucesso:
                        st.success("✓")
                        st.rerun()
                    else:
                        st.error("✗")

# Rodapé
st.markdown("---")
st.caption("© 2024 Time Comercial") 