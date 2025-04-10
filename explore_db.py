import streamlit as st
import pandas as pd
from db_connection import testar_conexao, listar_bancos, selecionar_banco, listar_tabelas, descrever_tabela, obter_dados

# Configuração da página
st.set_page_config(
    page_title="Explorador do Banco de Dados",
    page_icon="🔍",
    layout="wide",
)

st.title("Explorador do Banco de Dados MySQL")
st.write("Use esta ferramenta para explorar o banco de dados e verificar a estrutura das tabelas.")

# Teste de conexão
st.header("Status da Conexão")
with st.spinner("Testando conexão..."):
    sucesso, mensagem = testar_conexao()
    
    if sucesso:
        st.success(mensagem)
    else:
        st.error(f"Falha na conexão: {mensagem}")
        st.info("Verifique as configurações no arquivo .env e reinicie o aplicativo.")
        st.stop()

# Lista de bancos de dados
st.header("Bancos de Dados Disponíveis")
with st.spinner("Carregando bancos de dados..."):
    bancos = listar_bancos()
    if bancos:
        banco_selecionado = st.selectbox("Selecione um banco de dados", bancos)
        if st.button("Usar este banco de dados"):
            selecionar_banco(banco_selecionado)
            st.success(f"Banco de dados '{banco_selecionado}' selecionado!")
            st.rerun()
    else:
        st.warning("Nenhum banco de dados encontrado ou erro ao listar bancos.")
        st.stop()

# Lista de tabelas
st.header("Tabelas Disponíveis")
with st.spinner("Carregando tabelas..."):
    tabelas = listar_tabelas()
    if tabelas:
        tabela_selecionada = st.selectbox("Selecione uma tabela", tabelas)
    else:
        st.warning("Nenhuma tabela encontrada no banco de dados selecionado ou nenhum banco selecionado.")
        st.stop()

# Estrutura da tabela
if tabela_selecionada:
    st.header(f"Estrutura da Tabela: {tabela_selecionada}")
    with st.spinner("Carregando estrutura..."):
        colunas = descrever_tabela(tabela_selecionada)
        if colunas:
            df_colunas = pd.DataFrame(colunas)
            st.dataframe(df_colunas)
        else:
            st.warning(f"Não foi possível obter a estrutura da tabela {tabela_selecionada}.")

    # Visualizar dados
    st.header(f"Dados da Tabela: {tabela_selecionada}")
    limite = st.slider("Número de registros", min_value=5, max_value=100, value=20, step=5)
    
    if st.button(f"Visualizar {limite} registros"):
        with st.spinner("Carregando dados..."):
            query = f"SELECT * FROM {tabela_selecionada} LIMIT {limite}"
            df = obter_dados(query)
            if not df.empty:
                st.dataframe(df)
            else:
                st.info(f"A tabela {tabela_selecionada} não contém dados ou ocorreu um erro na consulta.")

    # Consulta personalizada
    st.header("Consulta SQL Personalizada")
    consulta = st.text_area("Escreva sua consulta SQL", 
                          value=f"SELECT * FROM {tabela_selecionada} LIMIT 10", 
                          height=100)
    
    if st.button("Executar Consulta"):
        with st.spinner("Executando consulta..."):
            if consulta:
                df = obter_dados(consulta)
                if not df.empty:
                    st.dataframe(df)
                else:
                    st.info("A consulta não retornou dados ou ocorreu um erro.")
            else:
                st.warning("Digite uma consulta SQL válida.") 