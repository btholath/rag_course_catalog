# backend/app/retrieval.py
import os
import json
import uuid
import fitz
import numpy as np
from typing import List
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from sentence_splitter import SentenceSplitter
from .bedrock_utils import get_query_embedding

# Load environment
load_dotenv(override=True)

# MongoDB setup
mongo = MongoClient(os.getenv("MONGO_URI"))
collection = mongo["rag"]["documents"]
splitter = SentenceSplitter(language='en')


def normalize(vector: List[float]) -> List[float]:
    norm = np.linalg.norm(vector)
    return list(np.array(vector) / norm) if norm else vector


def retrieve_documents(query: str):
    """Retrieve documents from MongoDB using vector search."""
    matches = list(collection.find({"text": {"$regex": query, "$options": "i"}}, {"text": 1}))
    print(f"🧪 Regex matches found for query '{query}': {len(matches)}")
    for m in matches:
        print("→", m.get("text"))

    query_doc = collection.find_one(
        {"text": {"$regex": query, "$options": "i"}},
        {"embedding": 1}
    )

    if query_doc:
        print("✅ Using cached embedding from MongoDB.")
        embedding = query_doc["embedding"]
    else:
        print("❌ No cached embedding found. Using Bedrock to generate one.")
        embedding = get_query_embedding(query)

    embedding = normalize(embedding)
    expected_dim = 1024
    if len(embedding) != expected_dim:
        print(f"⚠️ Embedding dimension mismatch! Expected {expected_dim}, got {len(embedding)}")
        return []

    cursor = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": embedding,
                "path": "embedding",
                "numCandidates": 100,
                "limit": 10,
                "index": "embedding-index"
            }
        }
    ])

    results = list(cursor)
    print(f"\n🔎 Retrieved {len(results)} results for query: '{query}'")
    for doc in results:
        print(f"- Page {doc.get('page')} from {doc.get('source')}: {doc.get('text')[:80]}...")

    seen_texts = set()
    unique_results = []
    for doc in results:
        if doc["text"] not in seen_texts:
            seen_texts.add(doc["text"])
            unique_results.append(doc)

    return {
        "matches": [
            {
                "text": doc["text"],
                "score": doc.get("score"),
                "source": doc.get("source"),
                "page": doc.get("page")
            }
            for doc in unique_results
        ]
    }


def search_documents_by_keyword(keyword: str):
    """Search documents by keyword match only."""
    docs = collection.find({"text": {"$regex": keyword, "$options": "i"}})
    return [
        {
            "text": doc.get("text"),
            "source": doc.get("source"),
            "page": doc.get("page")
        } for doc in docs
    ]


def get_document_by_id(doc_id: str):
    """Retrieve a document by its ObjectId."""
    try:
        doc = collection.find_one({"_id": ObjectId(doc_id)})
        if doc:
            return {
                "_id": str(doc["_id"]),
                "text": doc.get("text"),
                "source": doc.get("source"),
                "page": doc.get("page")
            }
    except Exception as e:
        print(f"Error retrieving document: {e}")
    return None


def compare_text_embeddings(text1: str, text2: str):
    """Generate embeddings for two texts and compute cosine similarity."""
    emb1 = normalize(get_query_embedding(text1))
    emb2 = normalize(get_query_embedding(text2))
    dot_product = float(np.dot(emb1, emb2))
    return {"similarity": dot_product}


def ingest_pdf(file_path: str):
    """Extract and store normalized embeddings from a PDF into MongoDB."""
    doc = fitz.open(file_path)
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if len(text.strip()) < 100:
            continue
        sentences = splitter.split(text)
        for chunk in sentences:
            if not chunk.strip():
                continue
            emb = normalize(get_query_embedding(chunk))
            record = {
                "_id": str(uuid.uuid4()),
                "text": chunk,
                "embedding": emb,
                "source": os.path.basename(file_path),
                "page": page_num + 1
            }
            collection.insert_one(record)
