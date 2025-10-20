from sqlmodel import create_engine, SQLModel, Session

# Importamos a URL do nosso arquivo de configurações
from settings import DATABASE_URL

# Importamos os modelos para que o SQLModel saiba quais tabelas criar
# Mesmo que 'models' não seja usado diretamente aqui,
# a importação dele "registra" as classes de modelo no metadata do SQLModel.
import models

# 'db_engine' é a nossa conexão principal com o banco.
# 'echo=True' é ótimo para desenvolvimento, pois mostra no console
# todos os comandos SQL que estão sendo executados.
db_engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """
    Cria todas as tabelas no banco de dados que herdam de SQLModel.
    """
    # SQLModel.metadata.create_all() percorre todos os modelos
    # importados (como o RagDocumentChunck) e cria suas tabelas.
    SQLModel.metadata.create_all(db_engine)

def get_session():
    """
    Função auxiliar para obter uma nova sessão com o banco.
    """
    return Session(db_engine)