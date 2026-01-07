import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQA

load_dotenv()
DB_FAISS_PATH = "./vector_store"

def get_qa_chain():
    # 1. Load Vector DB
    if not os.path.exists(DB_FAISS_PATH):
        raise FileNotFoundError(f"FAISS index not found at {DB_FAISS_PATH}. Run ingestion first.")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)

    # 2. Setup Groq with the NEW Llama 3.1 Model
    # "llama-3.1-8b-instant" is the current active model
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant", 
        temperature=0.1,
        api_key=os.getenv("GROQ_API_KEY")
    )

    # 3. Prompt Engineering
    template = """
    Answer the question based ONLY on the context below.
    
    Context: {context}
    
    Question: {question}
    
    Answer:
    """
    
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    # 4. Create Retrieval Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    
    return qa_chain