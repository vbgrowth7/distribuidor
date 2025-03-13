# Sistema de Gerenciamento do Time Comercial - Versão Demo

Esta é uma versão de demonstração do sistema de gerenciamento do time comercial, sem necessidade de conexão com banco de dados MySQL. Os dados são armazenados temporariamente na sessão do navegador.

## Funcionalidades

- Dashboard para visualização da equipe comercial
- Visualização do status de disponibilidade (disponível/indisponível) de cada membro
- Adição, edição e exclusão de membros da equipe
- Alteração rápida da disponibilidade dos membros
- Interface responsiva e amigável

## Requisitos

- Python 3.7+
- Bibliotecas Python (listadas em `requirements.txt`)

## Instalação

1. Clone este repositório ou baixe os arquivos
2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   ```
   
3. Ative o ambiente virtual:
   - Windows:
   ```bash
   venv\Scripts\activate
   ```
   - Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Executando o Aplicativo

1. Execute o aplicativo Streamlit:
   ```bash
   streamlit run app.py
   ```
2. Acesse o aplicativo no navegador (por padrão em http://localhost:8501)

## Importante

Esta é uma versão de demonstração onde:

- Os dados são armazenados temporariamente na sessão do navegador
- Todas as informações serão perdidas ao reiniciar o aplicativo
- Não há persistência em banco de dados

Quando estiver pronto para implementar a versão completa com MySQL, use os arquivos do diretório `time-comercial-streamlit` e configure a conexão com seu banco de dados.

## Como Usar

1. **Visualizar Equipe**: Na página inicial, você verá uma tabela com todos os membros da equipe e seus status.
2. **Adicionar Membro**: Selecione "Adicionar Membro" no menu lateral e preencha o formulário.
3. **Editar/Excluir Membro**: Na visualização da equipe, selecione um membro, escolha a ação desejada e clique em "Executar Ação".
4. **Alterar Disponibilidade**: Selecione um membro, escolha "Alterar Disponibilidade" e execute a ação. 