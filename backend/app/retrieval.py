### backend/app/retrieval.py
import os
import boto3
import json
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
print("mongo = ", os.getenv("MONGO_URI"))
# Initialize MongoDB connection
mongo = MongoClient(os.getenv("MONGO_URI"))


collection = mongo["rag"]["documents"]

# AWS Bedrock Client for embeddings
bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("BEDROCK_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("BEDROCK_SECRET_KEY")
)

def get_query_embedding(query: str):
    response = bedrock.invoke_model(
        modelId=os.getenv("BEDROCK_EMBEDDING_MODEL_ID"),
        body=json.dumps({"inputText": query}),
        accept="application/json",
        contentType="application/json"
    )
    embedding = json.loads(response["body"].read())["embedding"]
    return embedding

def retrieve_documents(query: str):
    embedding = get_query_embedding(query)
    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": embedding,
                "path": "embedding",
                "numCandidates": 50,
                "limit": 5,
                "index": "embedding-index"
            }
        }
    ])
    return [doc["text"] for doc in results]
