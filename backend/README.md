# 📚 RAG Course Catalog – Backend

This is the **FastAPI** backend for the RAG (Retrieval-Augmented Generation) Course Catalog Search system. It enables intelligent querying and summarization of university course catalogs using AWS Bedrock embeddings and vector search (MongoDB).

---

## 🚀 Features

- ✅ Query course documents using semantic or keyword-based search.
- 🧠 Embed user input via Amazon Bedrock's Titan model.
- 📄 Upload and index PDFs with vector embeddings.
- 🧪 Debug endpoints to inspect retrieval results.
- 🧰 Cosine similarity comparison between text embeddings.
- 📡 RESTful endpoints with OpenAPI (`/docs`) support.

---

## 🛠️ Tech Stack

- **FastAPI**
- **MongoDB Atlas**
- **AWS Bedrock** (Titan models)
- **Uvicorn** ASGI server

---

## 📦 Setup

### 1. Environment

Create a virtual environment:
```bash
bijut@b:~/rag_course_catalog/backend$ python3 -m venv .venv
bijut@b:~/rag_course_catalog/backend$ source .venv/bin/activate

Install dependencies:
(.venv) bijut@b:~/rag_course_catalog/backend$ pip install -r requirements.txt
```

### 2. Environment Variables
Set the following in .env:
```bash
MONGO_URI=mongodb+srv://rag_user:<password>@cluster0.ihylxvj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
# REDIS For future use
REDIS_HOST="localhost"
REDIS_PORT="6379"
AWS_REGION="us-east-1"
BEDROCK_EMBEDDING_MODEL_ID="amazon.titan-embed-text-v2:0"
BEDROCK_TEXT_MODEL_ID="amazon.titan-text-lite-v1"
BEDROCK_ACCESS_KEY="<aws access key>"
BEDROCK_SECRET_KEY="<aws secret key>"
# S3 for future use
S3_BUCKET_NAME="rag-course-catalogs"
```

### 2.1 Reactivate the virtual environment (optional)
Run below commands:
```bash
(.venv) bijut@b:~/rag_course_catalog/backend$
deactivate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```


### 3. Run the Server
## Start the FastAPI app
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Then visit:
http://localhost:8000/docs


## 4. Run Unit Tests
Make sure you're in the backend virtual environment and run:
```bash
cd backend
source .venv/bin/activate
pytest tests
```
You should see output like:
test_api.py::test_health PASSED

## Run with Docker (Optional)
If you want to run the backend using Docker:
```bash
cd backend
docker build -t rag-backend .
docker run -p 8000:8000 --env-file ../.env rag-backend
Now access: http://localhost:8000/docs
```

To run tests
```bash
pytest tests/test_api.py -v
```

# 🚀 API Documentation

## 📌 Overview
This API provides **Retrieval-Augmented Generation (RAG)** functionality, including text embedding, document retrieval, and metadata extraction.

---

## 🧪 API Endpoints


| **Endpoint**                  | **Description**                                      |
|--------------------------------|------------------------------------------------------|
| `POST /query`                  | Full RAG response (answer + context).               |
| `POST /debug/retrieve`         | Regex + vector search results.                      |
| `POST /query/metadata`         | Returns metadata only.                              |
| `POST /embedding/generate`     | Embed input text for vector representation.         |
| `POST /embedding/compare`      | Compute cosine similarity between two texts.        |
| `POST /upload/pdf`             | Upload a PDF and ingest its contents.               |
| `GET /documents/search?q=`     | Keyword-based document search.                      |
| `GET /documents/{id}`          | Retrieve a specific document by ID.                 |
| `GET /health`                  | API health check endpoint.                          |

---


### 📂 Project Structure
```bash
backend/
├── app/
│   ├── routes.py
│   ├── retrieval.py
│   ├── generation.py
│   ├── bedrock_utils.py
├── ingestion/
│   └── embedder.py
├── requirements.txt
├── main.py
```

## 🔐 AWS & Bedrock Notes
### Ensure IAM user has the following permissions:
```bash
{
  "Action": [
    "bedrock:InvokeModel",
    "bedrock:ListFoundationModels"
  ],
  "Effect": "Allow",
  "Resource": "*"
}
```

## Test with AWS CLI
```bash
#!/bin/bash
INPUT='{"inputText":"Hello from CLI"}'
ENCODED=$(echo -n $INPUT | base64)

aws bedrock-runtime invoke-model \
  --region us-east-1 \
  --model-id "amazon.titan-embed-text-v2:0" \
  --content-type "application/json" \
  --body $ENCODED \
  output.json

cat output.json
```
