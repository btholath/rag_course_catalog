# backend/app/bedrock_utils.py

import os
import json
import numpy as np
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# AWS Bedrock client using a named profile (e.g., 'ragcli')
session = boto3.Session(profile_name=os.getenv("AWS_PROFILE", "ragcli"))
bedrock = session.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_REGION")
)

def normalize(vector):
    """Normalize a vector to unit length."""
    norm = np.linalg.norm(vector)
    return list(np.array(vector) / norm) if norm else vector

def get_query_embedding(query: str) -> list:
    """Generate a normalized embedding for a user query using Amazon Bedrock."""
    print(f"📥 Calling Bedrock embedding for query: {query}")
    try:
        response = bedrock.invoke_model(
            modelId=os.getenv("BEDROCK_EMBEDDING_MODEL_ID"),
            body=json.dumps({"inputText": query}),
            accept="application/json",
            contentType="application/json"
        )
        body = json.loads(response["body"].read())
        embedding = body["embedding"]
        normalized = normalize(embedding)
        print("✅ Received and normalized embedding.")
        return normalized
    except Exception as e:
        print(f"❌ Failed to invoke Bedrock model: {e}")
        return [0.0] * 768  # fallback default
