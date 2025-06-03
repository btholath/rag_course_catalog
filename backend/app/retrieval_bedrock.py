### backend/app/retrieval.py
import os
import boto3
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import unquote

#load_dotenv()
# Optional: force UTF-8 encoding if you want to read manually
with open(".env", encoding="utf-8") as f:
    content = f.read()
    print(content)

load_dotenv(override=True)

# Initialize MongoDB connection
#os.environ["MONGO_URI"] = "mongodb://localhost:27017"
mongo = MongoClient(os.environ["MONGO_URI"])

collection = mongo["rag"]["documents"]

# AWS Bedrock Client for embeddings
#bedrock = boto3.client(
#    service_name="bedrock-runtime",
#    region_name=os.getenv("AWS_REGION"),
#    aws_access_key_id=os.getenv("BEDROCK_ACCESS_KEY"),
#    aws_secret_access_key=os.getenv("BEDROCK_SECRET_KEY")
#)

# AWS Bedrock client using profile only
session = boto3.Session(profile_name="ragcli")
bedrock = session.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_REGION")
)

print("Connected to AWS ", bedrock)
print("BEDROCK_EMBEDDING_MODEL_ID =", os.getenv("BEDROCK_EMBEDDING_MODEL_ID"))

def get_query_embedding(query: str):
    print("calling get_query_embedding()", query)
    response = bedrock.invoke_model(
        modelId=os.getenv("BEDROCK_EMBEDDING_MODEL_ID"),
        body=json.dumps({"inputText": query}),
        accept="application/json",
        contentType="application/json"
    )
    print("--RESPONSE--")
    print(response)
    
    print("STARTED embedding...")
    embedding = json.loads(response["body"].read())["embedding"]
    print("embedding = ", embedding)
    return embedding

def retrieve_documents(query: str):
    embedding = get_query_embedding(query)
    cursor = collection.aggregate([
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

    results = list(cursor)  # Force evaluation of the cursor

    print("\n--retrieve_documents1--")
    for doc in results:
        print(f"\nMatch (Page {doc.get('page')} from {doc.get('source')}):")
        print(doc.get("text"))

    print("\n--retrieve_documents2--")
    for doc in results:
        print(f"Match: {doc.get('text')} (Score not shown)")

    return [doc["text"] for doc in results]
