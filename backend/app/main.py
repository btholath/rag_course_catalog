### backend/app/main.py
from fastapi import FastAPI
from .routes import router

app = FastAPI(title="RAG Course Catalog")

app.include_router(router)
