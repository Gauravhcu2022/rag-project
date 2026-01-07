import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import logging

# Paths
DATA_PATH = "./data"
DB_FAISS_PATH = "./vector_store"

def create_vector_db():
    logging.info("Starting Data Ingestion...")

    # 1. Load Documents
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        logging.error(f"Data directory '{DATA_PATH}' missing. Please create it and add PDFs.")
        return False

    loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    
    if not documents:
        logging.warning("No documents found in data/ folder!")
        return False

    logging.info(f"Loaded {len(documents)} document(s).")

    # 2. Chunking (Context-Aware)
    # Overlap ensures sentences aren't cut in half awkwardly
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    texts = text_splitter.split_documents(documents)
    logging.info(f"Split into {len(texts)} chunks.")

    # 3. Embeddings (HuggingFace)
    # using all-MiniLM-L6-v2 which is fast and lightweight
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 4. Create and Save Vector Store
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)
    
    logging.info(f"Vector Store created at {DB_FAISS_PATH}")
    return True

if __name__ == "__main__":
    from src.utils import setup_logging
    setup_logging()
    create_vector_db()