
import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def search_prompt(question=None):
    prompt_template = PromptTemplate.from_template(PROMPT_TEMPLATE)
    
    # Criar chain que busca contexto e formata prompt
    chain = (
        RunnableLambda(lambda _: get_context_from_db(question)) 
        | prompt_template
    )
    return chain

    
def get_context_from_db(question):
    """Função auxiliar para buscar contexto no banco de dados"""
    embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"), google_api_key=os.getenv("GOOGLE_API_KEY"))
    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
    
    # Fazer busca por similaridade
    results = store.similarity_search(question, k=10)
    
    # Extrair o contexto dos resultados com formatação melhorada
    contexto_formatado = []
    for i, doc in enumerate(results, 1):
        contexto_formatado.append(f"=== DOCUMENTO {i} ===\n{doc.page_content}")
    contexto = "\n\n".join(contexto_formatado)
    # print(f"\nContexto recuperado:\n{contexto}\n")
    return {"contexto": contexto, "pergunta": question}