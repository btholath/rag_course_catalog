### backend/app/generation.py
import os
import boto3
import json
from dotenv import load_dotenv

#load_dotenv()
#bedrock = boto3.client(
#    service_name="bedrock-runtime",
#    region_name=os.getenv("AWS_REGION"),
#    aws_access_key_id=os.getenv("BEDROCK_ACCESS_KEY"),
#    aws_secret_access_key=os.getenv("BEDROCK_SECRET_KEY")
#)

#load_dotenv()
# Optional: force UTF-8 encoding if you want to read manually
with open(".env", encoding="utf-8") as f:
    content = f.read()
    print(content)

load_dotenv(override=True)

# AWS Bedrock client using profile only
session = boto3.Session(profile_name="ragcli")
bedrock = session.client(
    service_name="bedrock-runtime",
    region_name=os.getenv("AWS_REGION")
)

def generate_answer(query: str, context: list):
    print("STARTED generate_answer")
    context_text = "\n\n".join(context)
    prompt = f"""
    Answer the following question based only on the context below.

    Context:
    {context_text}

    Question: {query}
    """

    print("STARTED bedrock.invoke_model")
    print("BEDROCK_TEXT_MODEL_ID =", os.getenv("BEDROCK_TEXT_MODEL_ID"))
    response = bedrock.invoke_model(
        modelId=os.getenv("BEDROCK_TEXT_MODEL_ID"),
        body=json.dumps({"inputText": prompt}),
        accept="application/json",
        contentType="application/json"
    )
    print("Received response")
    output = json.loads(response["body"].read())
    print("OUTPUT=", output)
    return output.get("results", [])[0].get("outputText", "No answer generated.")