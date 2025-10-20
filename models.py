from typing import Optional, List
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import Text
from sqlalchemy.dialects.mysql import JSON as MySQL_JSON

# Conforme sua diretriz, a classe está em PascalCase
class RagDocumentChunck(SQLModel, table=True):
    """
    Modelo SQLModel que representa um chunk de documento para o RAG.
    Isso será mapeado para a tabela 'rag_document_chunck'.
    """
    
    # O nome da tabela é em snake_case, como solicitado
    __tablename__ = "rag_document_chuncks"

    # 'id', 'fonte', 'texto', 'vetor' são variáveis (atributos),
    # por isso estão em snake_case.
    id: Optional[int] = Field(default=None, primary_key=True)
    fonte: str = Field(index=True, max_length=255)
    
    # 'texto' pode ser muito longo, então usamos o tipo 'Text'
    texto: str = Field(sa_column=Column(Text))
    
    # 'vetor' é uma lista de floats. Usamos o tipo JSON nativo do MariaDB.
    vetor: List[float] = Field(sa_column=Column(MySQL_JSON))