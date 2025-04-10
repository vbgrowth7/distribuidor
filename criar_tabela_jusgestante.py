import streamlit as st
from db_connection import criar_conexao, executar_query, selecionar_banco

# Título da página
st.title("Criar Tabela JUSGESTANTE")

# Selecione o banco de dados
st.subheader("Selecione o banco de dados")
from db_connection import listar_bancos
bancos = listar_bancos()

banco_selecionado = st.selectbox("Banco de Dados", bancos)

if st.button("Usar este banco"):
    selecionar_banco(banco_selecionado)
    st.success(f"Banco de dados '{banco_selecionado}' selecionado!")

# Script SQL para criar a tabela
sql_criar_tabela = """
CREATE TABLE IF NOT EXISTS JUSGESTANTE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(14),
    email VARCHAR(255),
    telefone VARCHAR(20),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('PENDENTE', 'EM ANDAMENTO', 'CONCLUÍDO', 'CANCELADO') DEFAULT 'PENDENTE',
    observacoes TEXT
);
"""

# Script para inserir dados de exemplo
sql_inserir_exemplos = """
INSERT INTO JUSGESTANTE (nome, cpf, status) VALUES
('Maria da Silva', '123.456.789-00', 'PENDENTE'),
('João Oliveira', '987.654.321-00', 'EM ANDAMENTO'),
('Ana Souza', '456.789.123-00', 'CONCLUÍDO'),
('Pedro Santos', '321.654.987-00', 'CANCELADO'),
('Carla Ferreira', '789.123.456-00', 'PENDENTE');
"""

# Função para criar a tabela
def criar_tabela():
    sucesso, mensagem = executar_query(sql_criar_tabela)
    return sucesso, mensagem

# Função para inserir dados de exemplo
def inserir_exemplos():
    sucesso, mensagem = executar_query(sql_inserir_exemplos)
    return sucesso, mensagem

# Interface para criar a tabela
st.subheader("Criar Tabela JUSGESTANTE")
st.code(sql_criar_tabela, language="sql")

if st.button("Criar Tabela"):
    with st.spinner("Criando tabela..."):
        sucesso, mensagem = criar_tabela()
        if sucesso:
            st.success("Tabela criada com sucesso!")
        else:
            st.error(f"Erro ao criar tabela: {mensagem}")

# Interface para inserir dados de exemplo
st.subheader("Inserir Dados de Exemplo")
st.code(sql_inserir_exemplos, language="sql")

if st.button("Inserir Exemplos"):
    with st.spinner("Inserindo dados de exemplo..."):
        sucesso, mensagem = inserir_exemplos()
        if sucesso:
            st.success("Dados de exemplo inseridos com sucesso!")
        else:
            st.error(f"Erro ao inserir dados: {mensagem}")

# SQL Personalizado
st.subheader("Executar SQL Personalizado")
sql_personalizado = st.text_area("Digite seu comando SQL:", height=150)

if st.button("Executar SQL"):
    if sql_personalizado.strip():
        with st.spinner("Executando SQL..."):
            sucesso, mensagem = executar_query(sql_personalizado)
            if sucesso:
                st.success(f"SQL executado com sucesso! {mensagem}")
            else:
                st.error(f"Erro ao executar SQL: {mensagem}")
    else:
        st.warning("Digite um comando SQL válido.") 