### backend/app/routes.py
from fastapi import APIRouter, Request
from .retrieval import retrieve_documents
from .generation import generate_answer

router = APIRouter()

@router.post("/query")
async def query_handler(request: Request):
    body = await request.json()
    user_query = body.get("query")

    context_chunks = retrieve_documents(user_query)
    answer = generate_answer(user_query, context_chunks)

    return {"answer": answer, "context": context_chunks}