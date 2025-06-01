### backend/app/generation.py
import os
import boto3
import json
from dotenv import load_dotenv

load_dotenv()

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("BEDROCK_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("BEDROCK_SECRET_KEY")
)

def generate_answer(query: str, context: list):
    context_text = "\n\n".join(context)
    prompt = f"""
    Answer the following question based only on the context below.

    Context:
    {context_text}

    Question: {query}
    """

    response = bedrock.invoke_model(
        modelId=os.getenv("BEDROCK_TEXT_MODEL_ID"),
        body=json.dumps({"inputText": prompt}),
        accept="application/json",
        contentType="application/json"
    )
    output = json.loads(response["body"].read())
    return output.get("results", [])[0].get("outputText", "No answer generated.")