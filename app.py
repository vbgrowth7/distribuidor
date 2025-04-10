import streamlit as st
import pandas as pd
import datetime
import uuid

# Configuração da página
st.set_page_config(
    page_title="Gerenciamento do Time Comercial",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #1E88E5;
        text-align: center;
    }
    .subheader {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #424242;
    }
    .disponivel {
        background-color: #C8E6C9;
        padding: 5px 10px;
        border-radius: 10px;
        font-weight: bold;
        color: #2E7D32;
    }
    .indisponivel {
        background-color: #FFCDD2;
        padding: 5px 10px;
        border-radius: 10px;
        font-weight: bold;
        color: #C62828;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .form-box {
        background-color: #F5F5F5;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #E0E0E0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar dados de exemplo se não existirem na sessão
if 'equipe_comercial' not in st.session_state:
    st.session_state.equipe_comercial = [
        {
            'id': str(uuid.uuid4()),
            'nome': 'João Silva',
            'cargo': 'Gerente Comercial',
            'email': 'joao.silva@empresa.com',
            'telefone': '(11) 98765-4321',
            'disponivel': True,
            'data_cadastro': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            'id': str(uuid.uuid4()),
            'nome': 'Maria Santos',
            'cargo': 'Vendedora Sênior',
            'email': 'maria.santos@empresa.com',
            'telefone': '(11) 91234-5678',
            'disponivel': False,
            'data_cadastro': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            'id': str(uuid.uuid4()),
            'nome': 'Pedro Oliveira',
            'cargo': 'Representante de Vendas',
            'email': 'pedro.oliveira@empresa.com',
            'telefone': '(11) 99876-5432',
            'disponivel': True,
            'data_cadastro': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]

# Funções para manipular os dados
def obter_equipe_comercial():
    """Obtém todos os membros da equipe comercial."""
    return st.session_state.equipe_comercial

def obter_membro_por_id(id_membro):
    """Obtém um membro específico da equipe pelo ID."""
    for membro in st.session_state.equipe_comercial:
        if membro['id'] == id_membro:
            return membro
    return None

def adicionar_membro(nome, cargo, email, telefone, disponivel=True):
    """Adiciona um novo membro à equipe comercial."""
    novo_membro = {
        'id': str(uuid.uuid4()),
        'nome': nome,
        'cargo': cargo,
        'email': email,
        'telefone': telefone,
        'disponivel': disponivel,
        'data_cadastro': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.equipe_comercial.append(novo_membro)
    return True

def atualizar_membro(id_membro, nome, cargo, email, telefone, disponivel):
    """Atualiza os dados de um membro existente."""
    for i, membro in enumerate(st.session_state.equipe_comercial):
        if membro['id'] == id_membro:
            st.session_state.equipe_comercial[i] = {
                'id': id_membro,
                'nome': nome,
                'cargo': cargo,
                'email': email,
                'telefone': telefone,
                'disponivel': disponivel,
                'data_cadastro': membro['data_cadastro']
            }
            return True
    return False

def atualizar_disponibilidade(id_membro, disponivel):
    """Atualiza apenas o status de disponibilidade de um membro."""
    for i, membro in enumerate(st.session_state.equipe_comercial):
        if membro['id'] == id_membro:
            st.session_state.equipe_comercial[i]['disponivel'] = disponivel
            return True
    return False

def remover_membro(id_membro):
    """Remove um membro da equipe comercial."""
    for i, membro in enumerate(st.session_state.equipe_comercial):
        if membro['id'] == id_membro:
            st.session_state.equipe_comercial.pop(i)
            return True
    return False

def equipe_para_dataframe():
    """Converte a lista de membros da equipe em um DataFrame do pandas."""
    equipe = obter_equipe_comercial()
    if not equipe:
        return pd.DataFrame(columns=["id", "nome", "cargo", "email", "telefone", "disponivel", "data_cadastro"])
    
    df = pd.DataFrame(equipe)
    return df

# Função para exibir o cabeçalho
def exibir_cabecalho():
    st.markdown('<div class="main-header">Gerenciamento do Time Comercial</div>', unsafe_allow_html=True)
    st.markdown('---')

# Função para formatar a disponibilidade como badge colorido
def formatar_disponibilidade(disponivel):
    if disponivel:
        return '<span class="disponivel">Disponível</span>'
    return '<span class="indisponivel">Indisponível</span>'

# Função para exibir a lista de membros da equipe
def exibir_lista_equipe():
    st.markdown('<div class="subheader">Membros da Equipe</div>', unsafe_allow_html=True)
    
    # Obtém a lista de membros
    df = equipe_para_dataframe()
    
    if len(df) == 0:
        st.info("Nenhum membro cadastrado. Adicione o primeiro membro usando o formulário.")
        return
    
    # Prepara o dataframe para exibição
    if 'disponivel' in df.columns:
        df['status'] = df['disponivel'].apply(lambda x: formatar_disponibilidade(x))
    else:
        df['status'] = ''
    
    # Seleciona colunas para exibição
    colunas_exibicao = ['nome', 'cargo', 'email', 'telefone', 'status']
    df_exibicao = df[colunas_exibicao].copy() if all(col in df.columns for col in colunas_exibicao) else df
    
    # Renomeia colunas para exibição
    df_exibicao.columns = ['Nome', 'Cargo', 'Email', 'Telefone', 'Disponibilidade']
    
    # Exibe a tabela com formatação HTML para o status
    st.write(df_exibicao.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    # Área para ações (editar/excluir/alterar disponibilidade)
    st.markdown('<div class="subheader">Ações</div>', unsafe_allow_html=True)
    
    # Cria duas colunas: uma para seleção do membro e outra para ações
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if 'id' in df.columns and 'nome' in df.columns:
            opcoes_membros = {f"{row['nome']} ({row['cargo']})": row['id'] for _, row in df.iterrows()}
            membro_selecionado = st.selectbox("Selecione um membro", list(opcoes_membros.keys()))
            id_membro = opcoes_membros[membro_selecionado] if membro_selecionado else None
        else:
            st.error("Estrutura de dados inesperada. Verifique os dados.")
            id_membro = None
    
    with col2:
        if id_membro:
            acao = st.radio("Ação", ["Alterar Disponibilidade", "Editar", "Excluir"])
            
            if st.button("Executar Ação"):
                if acao == "Alterar Disponibilidade":
                    # Busca o membro e seu status atual
                    membro = obter_membro_por_id(id_membro)
                    if membro and 'disponivel' in membro:
                        novo_status = not membro['disponivel']
                        if atualizar_disponibilidade(id_membro, novo_status):
                            status_texto = "disponível" if novo_status else "indisponível"
                            st.success(f"Status alterado para {status_texto} com sucesso!")
                            st.experimental_rerun()
                        else:
                            st.error("Erro ao alterar disponibilidade.")
                
                elif acao == "Editar":
                    # Armazena o ID do membro para edição
                    st.session_state['membro_para_editar'] = id_membro
                    st.experimental_rerun()
                
                elif acao == "Excluir":
                    if remover_membro(id_membro):
                        st.success("Membro excluído com sucesso!")
                        st.experimental_rerun()
                    else:
                        st.error("Erro ao excluir membro.")

# Função para exibir o formulário de cadastro/edição
def exibir_formulario():
    # Verifica se está no modo de edição
    modo_edicao = 'membro_para_editar' in st.session_state
    
    if modo_edicao:
        id_membro = st.session_state['membro_para_editar']
        membro = obter_membro_por_id(id_membro)
        st.markdown(f'<div class="subheader">Editar Membro</div>', unsafe_allow_html=True)
    else:
        membro = None
        st.markdown('<div class="subheader">Adicionar Novo Membro</div>', unsafe_allow_html=True)
    
    with st.form("formulario_membro", clear_on_submit=not modo_edicao):
        st.markdown('<div class="form-box">', unsafe_allow_html=True)
        
        # Campos do formulário
        nome = st.text_input("Nome Completo*", value=membro['nome'] if membro and 'nome' in membro else "")
        cargo = st.text_input("Cargo*", value=membro['cargo'] if membro and 'cargo' in membro else "")
        
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Email*", value=membro['email'] if membro and 'email' in membro else "")
        with col2:
            telefone = st.text_input("Telefone*", value=membro['telefone'] if membro and 'telefone' in membro else "")
        
        disponivel = st.checkbox("Disponível para atendimento", 
                                value=membro['disponivel'] if membro and 'disponivel' in membro else True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            cancelar = st.form_submit_button("Cancelar")
        with col2:
            if modo_edicao:
                confirmar = st.form_submit_button("Salvar Alterações")
            else:
                confirmar = st.form_submit_button("Adicionar Membro")
        
        if cancelar:
            if 'membro_para_editar' in st.session_state:
                del st.session_state['membro_para_editar']
            st.experimental_rerun()
        
        if confirmar:
            # Validação básica
            if not nome or not cargo or not email or not telefone:
                st.error("Todos os campos marcados com * são obrigatórios.")
                return
            
            # Processamento com base no modo
            if modo_edicao:
                if atualizar_membro(id_membro, nome, cargo, email, telefone, disponivel):
                    st.success("Membro atualizado com sucesso!")
                    del st.session_state['membro_para_editar']
                    st.experimental_rerun()
                else:
                    st.error("Erro ao atualizar membro.")
            else:
                if adicionar_membro(nome, cargo, email, telefone, disponivel):
                    st.success("Membro adicionado com sucesso!")
                    st.experimental_rerun()
                else:
                    st.error("Erro ao adicionar membro.")

# Função principal
def main():
    exibir_cabecalho()
    
    # Barra lateral com informações
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/commercial-development-management.png", width=100)
        
        st.markdown("## Navegação")
        opcao = st.radio("Escolha uma opção:", ["Visualizar Equipe", "Adicionar Membro"])
        
        st.markdown("---")
        st.markdown("### Versão de Demonstração")
        st.markdown("Esta é uma versão de demonstração sem banco de dados. Os dados são armazenados temporariamente na sessão e serão perdidos ao reiniciar o aplicativo.")
    
    # Conteúdo principal com base na opção selecionada
    if opcao == "Visualizar Equipe" and 'membro_para_editar' not in st.session_state:
        exibir_lista_equipe()
    else:
        exibir_formulario()

if __name__ == "__main__":
    main() 