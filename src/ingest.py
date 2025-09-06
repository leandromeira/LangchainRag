import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    documents = load_pdf()
    chunks = chunk_pdf(documents)
    enriched = enrich(chunks)
    store(enriched)


def load_pdf():
    if not PDF_PATH:
        print("Caminho do PDF não está definido. Verifique o arquivo .env.")
        return []
    loader = PyPDFLoader(PDF_PATH)
    return loader.load()
    

def chunk_pdf(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, add_start_index=False)

    chunks = text_splitter.split_documents(documents)
    if not chunks:
        raise SystemExit(0)
    return chunks

def enrich(chunks):
    return [
        Document(
            page_content=chunk.page_content,
            metadata={k: v for k, v in chunk.metadata.items() if v not in ("", None)}
        )
        for chunk in chunks
    ]

def store(enriched):
    ids = [f"doc-{i}" for i in range(len(enriched))]

    embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"), google_api_key=os.getenv("GOOGLE_API_KEY"))
    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
    store.add_documents(documents=enriched, ids=ids)



if __name__ == "__main__":
    ingest_pdf()