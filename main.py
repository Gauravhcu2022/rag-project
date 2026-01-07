import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.rag_engine import get_qa_chain
from src.ingestion import create_vector_db
from src.utils import setup_logging

# Initialize Logging
setup_logging()

app = FastAPI(title="Resume RAG System", description="Context-Aware Q&A over Resume")

class QueryRequest(BaseModel):
    query: str

class UpdateResponse(BaseModel):
    status: str
    message: str

@app.get("/")
def home():
    return {"message": "Welcome to the Context-Aware RAG System. Use /query to ask questions."}

@app.post("/train", response_model=UpdateResponse)
def train_docs():
    try:
        success = create_vector_db()
        if success:
            return {"status": "success", "message": "Vector store updated successfully."}
        else:
            raise HTTPException(status_code=500, detail="Failed to ingest documents.")
    except Exception as e:
        traceback.print_exc()  
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query_docs(request: QueryRequest):
    try:
        chain = get_qa_chain()
        
        # Pass a dictionary, not just a string
        response = chain.invoke({"query": request.query})
        
        # Extract answer and sources
        answer = response['result']
        sources = [doc.metadata.get('source', 'Unknown') for doc in response['source_documents']]
        unique_sources = list(set(sources))
        
        return {
            "answer": answer,
            "sources": unique_sources
        }
    except Exception as e:
        print("!!! ERROR OCCURRED !!!") 
        traceback.print_exc()           
        raise HTTPException(status_code=500, detail=str(e))