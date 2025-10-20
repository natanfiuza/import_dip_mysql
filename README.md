# Importador do Pipeline de Ingestão de Dados (DIP) para MySQL

Um script CLI (Interface de Linha de Comando) em Python para carregar dados de vetores (embeddings) de um pipeline de RAG (Retrieval-Augmented Generation) em um banco de dados MariaDB/MySQL, utilizando SQLModel e Typer.

## 🚀 Sobre o Projeto

Este projeto foi criado para resolver uma etapa crucial em sistemas de **RAG**: a *ingestão de dados*.

Em um pipeline de RAG, documentos grandes (livros, artigos, etc.) são quebrados em pequenos "chunks" (pedaços de texto). Cada chunk é então transformado em um "vetor" (ou *embedding*) — uma lista de números que representa o significado semântico daquele texto.

Este script lê um arquivo JSON contendo esses chunks e seus respectivos vetores e os armazena de forma estruturada em um banco de dados MariaDB/MySQL. Isso permite que a aplicação RAG realize buscas semânticas de forma eficiente no futuro.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído com uma stack moderna e robusta de Python:

  * **Python 3.10+**
  * **[Pipenv](https://pipenv.pypa.io/en/latest/)**: Para gerenciamento de dependências e ambientes virtuais.
  * **[SQLModel](https://sqlmodel.tiangolo.com/)**: Como ORM (Mapeador Objeto-Relacional), que combina o melhor do SQLAlchemy e Pydantic para uma interação moderna e segura com o banco de dados.
  * **[Typer](https://typer.tiangolo.com/)**: Para criar a Interface de Linha de Comando (CLI) de forma fácil, robusta e com validação automática.
  * **[python-dotenv](https://pypi.org/project/python-dotenv/)**: Para carregar variáveis de ambiente (como senhas) de um arquivo `.env`, mantendo nosso código seguro.
  * **[mysqlclient](https://pypi.org/project/mysqlclient/)**: O driver Python que permite a comunicação com o banco de dados MariaDB/MySQL.

## ⚙️ Instalação e Configuração

Siga os passos abaixo para executar o projeto localmente.

### 1\. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/import_dip_mysql.git
cd import_dip_mysql
```

### 2\. Instale as Dependências

Usamos o `Pipfile` para gerenciar o projeto. O Pipenv cuidará de criar um ambiente virtual e instalar tudo o que é necessário.

```bash
pipenv install
```

### 3\. Configure o Ambiente

Este projeto lê a string de conexão do banco de dados a partir de um arquivo `.env` para manter as senhas seguras e fora do controle de versão.

**a.** Crie um arquivo chamado `.env` na raiz do projeto:

```bash
touch .env
```

**b.** Abra o arquivo `.env` e adicione sua string de conexão. O formato é:
`"mysql+mysqlclient://USUARIO:SENHA@HOST:PORTA/NOME_DO_BANCO"`

```ini
# Exemplo de arquivo .env
DATABASE_URL="mysql+mysqlclient://root:minha_senha_secreta@127.0.0.1:3306/meu_banco_rag"
```

**⚠️ Importante:** O banco de dados (`meu_banco_rag` no exemplo) já deve existir no seu servidor MariaDB/MySQL. O script cuidará apenas de criar a tabela.

## 🚀 Modo de Uso

Todos os comandos devem ser executados de dentro do ambiente virtual do Pipenv.

### 1\. Ative o Ambiente Virtual

```bash
pipenv shell
```

(O Pipenv também carrega automaticamente as variáveis do seu arquivo `.env` ao ativar o shell).

### 2\. Crie as Tabelas no Banco (Inicialização)

Este comando deve ser executado **apenas uma vez**. Ele irá ler o modelo definido em `models.py` e criar a tabela `rag_document_chuncks` no seu banco de dados.

```bash
python main.py init-db
```

Você verá o log do SQLModel (`echo=True`) mostrando o comando `CREATE TABLE` sendo executado.

### 3\. Carregue os Dados do JSON

Use este comando para ler um arquivo JSON e inserir os dados no banco.

```bash
python main.py load-data /caminho/para/seu_arquivo.json
```

**Exemplo prático:**

```bash
python main.py load-data ./REGRA_DE_VIDA_EM_ADORACAO.example.json
```

Você verá uma barra de progresso indicando o carregamento dos chunks e uma mensagem de sucesso ao final.

## 📂 Estrutura do Projeto (Didática)

Para fins didáticos e para seguir boas práticas, o projeto foi dividido em módulos. Cada arquivo tem uma responsabilidade única, seguindo o **Princípio da Separação de Responsabilidades (SoC)**.

```
importador-dip/
│
├── .env              # (Seu arquivo local, secreto) Armazena a senha do banco
├── Pipfile           # Define as dependências do projeto
├── settings.py       # Carrega o .env e expõe as configurações
├── database.py       # Configura a conexão (engine) com o banco
├── models.py         # Define o "molde" da tabela (a classe RagDocumentChunck)
└── main.py           # Ponto de entrada da CLI (Typer) com os comandos
```

### Explicação de cada arquivo (para estudo)

  * `settings.py`:

      * **Responsabilidade:** Carregar variáveis de ambiente.
      * **Por quê?** Ele usa o `python-dotenv` para ler o `.env`. O resto da aplicação não precisa saber *de onde* vêm as configurações (seja de um arquivo, do sistema, etc.), ele apenas as consome daqui.

  * `models.py`:

      * **Responsabilidade:** Definir a estrutura dos dados.
      * **Por quê?** É o "arquiteto". A classe `RagDocumentChunck` (em `PascalCase`) é o "molde" que o SQLModel usa para entender como deve ser a tabela `rag_document_chunck` (em `snake_case`) e suas colunas (`fonte`, `texto`, `vetor`).

  * `database.py`:

      * **Responsabilidade:** Gerenciar a conexão com o banco.
      * **Por quê?** É o "porteiro". Ele importa a `DATABASE_URL` do `settings.py` para criar a `db_engine` (a "ponte" de conexão). Ele também fornece a função `create_db_and_tables`, que usa os `models.py` para criar as tabelas.

  * `main.py`:

      * **Responsabilidade:** Ser a interface com o usuário (CLI).
      * **Por quê?** É o "chefe de obras". É o único arquivo que o usuário executa. Ele usa o `Typer` para criar os comandos (`init-db`, `load-data`) e importa as "ferramentas" dos outros arquivos (`db_engine`, `RagDocumentChunck`, etc.) para orquestrar as tarefas.

## 🤝 Contribuição

Contribuições são muito bem-vindas\! Se você encontrar um bug ou tiver uma ideia para melhoria, sinta-se à vontade para abrir uma *Issue* ou enviar um *Pull Request*.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.