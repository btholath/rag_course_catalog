# ingestion/embedder.py
"""
PDF Embedding Pipeline
----------------------
This script extracts text from PDF files, processes it into manageable chunks, and generates 
vector embeddings using Amazon Bedrock's AI models. The embeddings are then stored in 
MongoDB for retrieval and AI-driven applications.

Dependencies:
    - PyMuPDF (fitz)
    - AWS Boto3 (Bedrock API)
    - MongoDB (pymongo)
    - SentenceSplitter
    - dotenv (for environment variables)

Environment Variables:
    - AWS_REGION: AWS region for Bedrock API calls
    - BEDROCK_ACCESS_KEY, BEDROCK_SECRET_KEY: AWS credentials
    - BEDROCK_EMBEDDING_MODEL_ID: Titan model for text embeddings
    - MONGO_URI: MongoDB connection string

Workflow:
    1. Read PDF files from the specified directory.
    2. Extract and process text from each page.
    3. Split text into meaningful sentence chunks.
    4. Generate embeddings using Amazon Bedrock.
    5. Store text and embeddings in MongoDB.

Functions:
    - get_embedding(text: str) -> list[float]
        Calls Amazon Bedrock to generate a numerical embedding for input text.
        Returns a 768-dimensional vector (or a placeholder if text is empty).

    - process_pdf(file_path: str) -> None
        Extracts text from a PDF, splits sentences, generates embeddings, and 
        stores results in MongoDB.

Example Usage:
    ```
    python embedder.py --path ../pdfs
    ```

Notes:
    - Skips pages with minimal content (<100 characters) to reduce noise.
    - Prints text chunks for debugging before embedding generation.
    - Stores each document with a unique ID in MongoDB for retrieval.
"""
import os
import fitz as fitz  # Correct import for Ubuntu/PyMuPDF
import boto3
import argparse
import uuid
from pymongo import MongoClient
from utils import extract_text_chunks_from_pdf
from sentence_splitter import SentenceSplitter
from dotenv import load_dotenv
import json

load_dotenv()

# AWS Bedrock client
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("BEDROCK_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("BEDROCK_SECRET_KEY")
)

mongo = MongoClient(os.getenv("MONGO_URI"))
collection = mongo["rag"]["documents"]
splitter = SentenceSplitter(language='en')

def get_embedding(text):
    response = bedrock.invoke_model(
        modelId=os.getenv("BEDROCK_EMBEDDING_MODEL_ID"),
        body=json.dumps({"inputText": text}),
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response["body"].read())
    if not text.strip():
        return [0.0] * 768  # Example: return a placeholder embedding
    return response_body["embedding"]

def process_pdf(file_path):
    doc = fitz.open(file_path)
    for page_num, page in enumerate(doc):
        text = page.get_text()
        if len(text.strip()) < 100: # Skip low-content pages
            continue
        sentences = splitter.split(text)
        for chunk in sentences:
            if not chunk.strip():  # Skip empty or whitespace-only chunks
                continue
            print(f"Processing chunk: {chunk}")  # Debugging
            emb = get_embedding(chunk)
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