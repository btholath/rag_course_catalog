# backend/app/routes.py
from fastapi import APIRouter, Request, Body, UploadFile, File
from pydantic import BaseModel
from .retrieval import (
    retrieve_documents,
    search_documents_by_keyword,
    get_document_by_id,
    compare_text_embeddings,
    ingest_pdf
)
from .generation import generate_answer

router = APIRouter()

class EmbedRequest(BaseModel):
    text: str

class CompareRequest(BaseModel):
    text1: str
    text2: str

@router.post("/query")
async def query_handler(request: Request):
    print("STARTED /query")
    body = await request.json()
    user_query = body.get("query")
    print("RECIEVED user_query", user_query)
    
    if not user_query:
        return {"error": "Query is required."}
    
    context_chunks = retrieve_documents(user_query)
    print("Derived context chunks")
    context_texts = [doc["text"] for doc in context_chunks["matches"]]
    print("Derived context_texts")

    unique_context = list({doc['text'] for doc in context_chunks["matches"]})
    answer = generate_answer(user_query, unique_context)

    print("Received answer")
    
    return {
        "query": user_query,
        "answer": answer,
        "context": context_chunks["matches"]
    }


@router.post("/debug/retrieve")
async def debug_retrieve(query: str = Body(..., embed=True)):
    print("STARTED debug_retrieve...")
    docs = retrieve_documents(query)
    return {"matches": docs["matches"]} if docs else {"info": "No matching documents found."}

@router.post("/query/metadata")
async def query_metadata(request: Request):
    body = await request.json()
    query = body.get("query")
    results = retrieve_documents(query)
    return {
        "metadata": [
            {"source": doc["source"], "page": doc["page"]}
            for doc in results["matches"]
        ]
    }

@router.post("/embedding/generate")
async def generate_embedding_only(payload: EmbedRequest):
    from .bedrock_utils import get_query_embedding
    embedding = get_query_embedding(payload.text)
    return {"embedding": embedding, "dimension": len(embedding)}

@router.get("/documents/search")
async def keyword_search(q: str):
    return search_documents_by_keyword(q)

@router.get("/documents/{doc_id}")
async def fetch_document(doc_id: str):
    doc = get_document_by_id(doc_id)
    return doc if doc else {"error": "Document not found"}

@router.post("/embedding/compare")
async def compare_embeddings(request: CompareRequest):
    return compare_text_embeddings(request.text1, request.text2)

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    ingest_pdf(file_path)
    return {"message": f"PDF '{file.filename}' processed and ingested."}

@router.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running smoothly!"}
