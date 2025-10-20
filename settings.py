import os
import typer
from dotenv import load_dotenv

# Esta função mágica procura por um arquivo .env na raiz
# e carrega suas variáveis para o os.getenv()
load_dotenv()

# 'DATABASE_URL' é uma constante, por isso está em maiúsculo
DATABASE_URL = os.getenv("DATABASE_URL")

# Verificação para garantir que o .env foi configurado
if not DATABASE_URL:
    typer.secho(
        "Erro: A variável de ambiente 'DATABASE_URL' não foi definida.",
        fg=typer.colors.RED
    )
    typer.secho("Por favor, crie um arquivo .env com a string de conexão.", fg=typer.colors.YELLOW)
    raise typer.Exit(code=1)