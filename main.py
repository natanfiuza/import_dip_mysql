import json
import typer
from typing_extensions import Annotated

# Importamos as funções e a engine do nosso módulo de banco de dados
from database import db_engine, create_db_and_tables

# Importamos o modelo para podermos criar instâncias dele
from models import RagDocumentChunck

# Importamos o Session para interagir com o banco
from sqlmodel import Session

# Criamos a aplicação Typer (em snake_case)
app = typer.Typer(help="CLI para carregar dados do RAG no MariaDB.")

@app.command()
def init_db():
    """
    Inicializa o banco de dados e cria a tabela 'rag_document_chunck'.
    """
    try:
        typer.echo("Criando tabelas no banco de dados...")
        create_db_and_tables() # Função importada de 'database.py'
        typer.secho("Tabelas criadas com sucesso!", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"Erro ao criar tabelas: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def load_data(
    json_file: Annotated[typer.Path(
        exists=True, 
        file_okay=True, 
        dir_okay=False, 
        readable=True
    ),
    typer.Argument(help="Caminho para o arquivo JSON com os chunks.")]
):
    """
    Lê o arquivo JSON e insere os dados na tabela 'rag_document_chunck'.
    """
    typer.echo(f"Iniciando o carregamento do arquivo: {json_file}")

    # 1. Ler o arquivo JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data_from_json = json.load(f)
        
        if not isinstance(data_from_json, list):
            typer.secho("Erro: O JSON não é uma lista de objetos.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
            
        typer.echo(f"Arquivo JSON lido. {len(data_from_json)} registros encontrados.")
        
    except json.JSONDecodeError:
        typer.secho(f"Erro: O arquivo '{json_file}' não é um JSON válido.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"Erro ao ler o arquivo: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # 2. Inserir no Banco de Dados
    total_inserted = 0
    
    # 'with Session(...)' gerencia o ciclo de vida da sessão (abre e fecha)
    with Session(db_engine) as db_session: # Usamos a engine importada
        typer.echo("Iniciando inserção no banco de dados...")
        
        with typer.progressbar(data_from_json, label="Processando chunks") as progress:
            for item in progress:
                try:
                    # Instanciamos a classe (PascalCase) importada de 'models.py'
                    document_chunck = RagDocumentChunck(
                        fonte=item.get("fonte"),
                        texto=item.get("texto"),
                        vetor=item.get("vetor")
                    )
                    db_session.add(document_chunck)
                    total_inserted += 1
                except Exception as e:
                    typer.secho(f"\nErro ao processar o item: {item}. Erro: {e}", fg=typer.colors.YELLOW)
        
        # 3. Commit das mudanças
        try:
            db_session.commit()
            typer.secho(f"\nSucesso! {total_inserted} registros inseridos na tabela 'rag_document_chunck'.", fg=typer.colors.GREEN)
        except Exception as e:
            typer.secho(f"\nErro ao comitar transação: {e}", fg=typer.colors.RED)
            typer.echo("Revertendo mudanças (rollback)...")
            db_session.rollback()

if __name__ == "__main__":
    app()