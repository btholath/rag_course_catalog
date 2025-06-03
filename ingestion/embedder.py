# ingestion/embedder.py
"""
PDF Embedding Pipeline
----------------------
Extracts text from PDF files, generates normalized vector embeddings using Amazon Bedrock, 
and stores results in MongoDB for retrieval tasks.

Dependencies:
    - PyMuPDF (fitz)
    - AWS Boto3
    - pymongo
    - numpy
    - SentenceSplitter
    - python-dotenv

Environment Variables:
    - AWS_REGION
    - BEDROCK_EMBEDDING_MODEL_ID
    - MONGO_URI

Example Usage:
    python embedder.py --path ../pdfs
"""

import os
import json
import uuid
import fitz
import boto3
import argparse
import numpy as np
from pymongo import MongoClient
from dotenv import load_dotenv
from sentence_splitter import SentenceSplitter

# Load environment variables
load_dotenv(override=True)

# AWS Bedrock client using profile
session = boto3.Session(profile_name="ragcli")
bedrock = session.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_REGION")
)

# MongoDB client
mongo = MongoClient(os.getenv("MONGO_URI"))
collection = mongo["rag"]["documents"]

# Sentence splitter for chunking
splitter = SentenceSplitter(language='en')

def normalize(vector):
    """Normalize a vector to unit length."""
    norm = np.linalg.norm(vector)
    return list(np.array(vector) / norm) if norm else vector

def get_embedding(text: str) -> list:
    """Generate and normalize embedding for given text using Amazon Bedrock."""
    if not text.strip():
        return [0.0] * 768
    try:
        response = bedrock.invoke_model(
            modelId=os.getenv("BEDROCK_EMBEDDING_MODEL_ID"),
            body=json.dumps({"inputText": text}),
            accept="application/json",
            contentType="application/json"
        )
        embedding = json.loads(response["body"].read())["embedding"]
        return normalize(embedding)
    except Exception as e:
        print("❌ Error generating embedding:", e)
        return [0.0] * 768

def process_pdf(file_path: str) -> None:
    """Process PDF file, generate embeddings, and insert into MongoDB."""
    doc = fitz.open(file_path)
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if len(text.strip()) < 100:
            continue

        print(f"\n📄 Processing {file_path}, Page {page_num + 1}")
        print(f"Preview: {text[:200]}")

        sentences = splitter.split(text)
        for chunk in sentences:
            if not chunk.strip():
                continue

            print(f"→ Chunk: {chunk[:100]}...")
            emb = get_embedding(chunk)
            if len(emb) != 768 and len(emb) != 1024:
                print(f"⚠️ Embedding dimension mismatch! Got {len(emb)}")
            
            record = {
                "_id": str(uuid.uuid4()),
                "text": chunk,
                "embedding": emb,
                "source": os.path.basename(file_path),
                "page": page_num + 1
            }
            collection.insert_one(record)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True)
    args = parser.parse_args()

    for filename in os.listdir(args.path):
        if filename.endswith(".pdf"):
            process_pdf(os.path.join(args.path, filename))
