import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import pandas as pd

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do banco de dados
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

# Adiciona o banco de dados à configuração apenas se estiver definido
if os.getenv('DB_NAME'):
    DB_CONFIG['database'] = os.getenv('DB_NAME')

def criar_conexao():
    """Cria e retorna uma conexão com o banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def testar_conexao():
    """Testa a conexão com o banco de dados e retorna um status."""
    try:
        conn = criar_conexao()
        if conn.is_connected():
            db_info = conn.get_server_info()
            cursor = conn.cursor()
            # Se não há banco de dados especificado, apenas verificamos a conexão
            if 'database' in DB_CONFIG:
                cursor.execute("SELECT DATABASE();")
                database_name = cursor.fetchone()[0]
                cursor.close()
                conn.close()
                return True, f"Conectado ao MySQL Server versão {db_info}, banco de dados: {database_name}"
            else:
                cursor.execute("SHOW DATABASES;")
                databases = cursor.fetchall()
                databases_str = ', '.join([db[0] for db in databases])
                cursor.close()
                conn.close()
                return True, f"Conectado ao MySQL Server versão {db_info}. Bancos disponíveis: {databases_str}"
        else:
            return False, "Falha ao conectar ao servidor MySQL"
    except Error as e:
        return False, f"Erro: {str(e)}"

def listar_bancos():
    """Lista todos os bancos de dados disponíveis."""
    try:
        conn = criar_conexao()
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES;")
            bancos = cursor.fetchall()
            cursor.close()
            conn.close()
            return [banco[0] for banco in bancos]
        return []
    except Error as e:
        print(f"Erro ao listar bancos de dados: {e}")
        return []

def listar_tabelas():
    """Lista todas as tabelas disponíveis no banco de dados."""
    try:
        conn = criar_conexao()
        if conn.is_connected():
            cursor = conn.cursor()
            # Se não há banco de dados especificado, não podemos listar tabelas
            if 'database' not in DB_CONFIG:
                cursor.close()
                conn.close()
                return []
            cursor.execute("SHOW TABLES;")
            tabelas = cursor.fetchall()
            cursor.close()
            conn.close()
            return [tabela[0] for tabela in tabelas]
        return []
    except Error as e:
        print(f"Erro ao listar tabelas: {e}")
        return []

def selecionar_banco(nome_banco):
    """Seleciona um banco de dados para uso."""
    global DB_CONFIG
    DB_CONFIG['database'] = nome_banco
    return True

def descrever_tabela(nome_tabela):
    """Retorna a estrutura de uma tabela específica."""
    try:
        conn = criar_conexao()
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"DESCRIBE {nome_tabela};")
            colunas = cursor.fetchall()
            cursor.close()
            conn.close()
            return colunas
        return []
    except Error as e:
        print(f"Erro ao descrever tabela: {e}")
        return []

def obter_dados(query):
    """Executa uma consulta SQL e retorna os resultados como um DataFrame."""
    try:
        conn = criar_conexao()
        if conn.is_connected():
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        return pd.DataFrame()
    except Error as e:
        print(f"Erro ao executar consulta: {e}")
        return pd.DataFrame()

def executar_query(query, params=None):
    """Executa uma query SQL (INSERT, UPDATE, DELETE) e retorna o status."""
    try:
        conn = criar_conexao()
        if conn.is_connected():
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            afetadas = cursor.rowcount
            cursor.close()
            conn.close()
            return True, f"{afetadas} linha(s) afetada(s)"
        return False, "Falha na conexão com o banco de dados"
    except Error as e:
        return False, f"Erro ao executar a query: {str(e)}" 