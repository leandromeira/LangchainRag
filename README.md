# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema RAG (Retrieval-Augmented Generation) desenvolvido com LangChain, PostgreSQL + pgvector e Google Generative AI para processamento de documentos PDF e respostas baseadas em contexto.

## Funcionalidades

- **Ingestão de PDF**: Carregamento e processamento de documentos PDF
- **Chunking inteligente**: Divisão do texto em chunks com sobreposição
- **Busca vetorial**: Utiliza embeddings do Google AI para busca por similaridade
- **Chat contextual**: Interface de conversação baseada em contexto recuperado
- **Respostas rigorosas**: Sistema que só responde com base no contexto disponível

## Pré-requisitos

- Python 3.13+
- Docker e Docker Compose
- Chave de API do Google Generative AI

## Configuração do Ambiente

### 1. Clone e Setup Inicial

```bash
# Clone o repositório
git clone <seu-repositorio>
cd LangchainRag

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 2. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o Banco de Dados

```bash
# Inicie o PostgreSQL com pgvector
docker-compose up -d postgres

# Configure a extensão pgvector (opcional)
docker-compose run bootstrap_vector_ext
```

### 4. Configure as Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
GOOGLE_API_KEY=sua_chave_do_google_ai
GOOGLE_EMBEDDING_MODEL=models/embedding-001
OPENAI_API_KEY=
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documents_collection
PDF_PATH=./document.pdf
```

## Execução

### 1. Ingestão do Documento

Primeiro, processe o documento PDF:

```bash
python src/ingest.py
```

Este comando irá:

- Carregar o PDF especificado em `PDF_PATH`
- Dividir em chunks de 1000 caracteres com sobreposição de 150
- Gerar embeddings usando Google AI
- Armazenar no banco PostgreSQL com pgvector

### 2. Iniciar o Chat

Execute a interface de conversação:

```bash
python src/chat.py
```

O sistema irá:

- Solicitar sua pergunta
- Buscar contexto relevante (top-10 similaridade)
- Gerar resposta baseada apenas no contexto encontrado
- Retornar "Não tenho informações necessárias" se não encontrar contexto relevante

## Exemplo de Uso

```bash
$ python src/chat.py
Faça sua pergunta:

PERGUNTA: Qual o faturamento da Empresa Coral Atacado S.A.?
==============================
RESPOSTA: R$ 1.401.199,64
```

## Arquitetura do Sistema

```
src/
├── ingest.py    # Pipeline de ingestão de documentos
├── search.py    # Sistema de busca e recuperação de contexto
└── chat.py      # Interface de chat com o usuário
```

### Componentes Principais

- **ingest.py**: Carrega PDF → Chunking → Embeddings → Armazenamento
- **search.py**: Query → Busca Vetorial → Formatação de Contexto
- **chat.py**: Interface → Recuperação → LLM → Resposta

## Parâmetros Importantes

- **k=10**: Número de chunks recuperados na busca por similaridade
- **Chunk size**: 1000 caracteres com overlap de 150
- **Modelo**: Google Gemini 2.5 Flash Lite (temperatura=0)
- **Embeddings**: Google models/embedding-001

## Troubleshooting

### Erro de conexão com banco

```bash
# Verifique se o container está rodando
docker ps

# Reinicie se necessário
docker-compose down
docker-compose up -d postgres
docker-compose run bootstrap_vector_ext
```

### Erro de API Key

- Verifique se a `GOOGLE_API_KEY` está correta no arquivo `.env`
- Certifique-se de que a chave tem permissões para Generative AI

### Documento não encontrado

- Verifique se o arquivo PDF existe no caminho especificado em `PDF_PATH`
- Certifique-se de que o arquivo não está corrompido

## Tecnologias Utilizadas

- **LangChain**: Framework para aplicações LLM
- **PostgreSQL + pgvector**: Banco vetorial
- **Google Generative AI**: Embeddings e modelo de chat
- **PyPDF**: Processamento de documentos PDF
- **Docker**: Containerização do banco de dados
