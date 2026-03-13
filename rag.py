from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
import os


import os
import pickle

DOCS_DIR = "docs"
DB_PATH = "vectordb.pkl"

def load_vectorstore():
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    docs = []
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DOCS_DIR, filename))
            docs.extend(loader.load())

    # Filtra páginas sin texto
    docs = [doc for doc in docs if doc.page_content.strip()]

    if not docs:
        return None

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    chunks = [chunk for chunk in chunks if chunk.page_content.strip()]

    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


def get_context(query: str, vectorstore, k: int = 3) -> str:
    if not vectorstore:
        return ""
    results = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in results])