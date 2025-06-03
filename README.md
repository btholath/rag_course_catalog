📘 Retrieval-Augmented Generation (RAG) App - Course Catalogs

A production-ready Retrieval-Augmented Generation (RAG) system that enables natural language querying over university course catalogs. Built using FastAPI, ReactJS, MongoDB Atlas Vector Search, Redis, and AWS Bedrock (Titan Embeddings), this application delivers real-time and accurate LLM responses grounded in PDF-based academic catalogs.

Features include PDF ingestion, Titan-based vector embedding, document retrieval, AWS Bedrock-based response generation, S3 integration, semantic search, and chat—all deployable on AWS.

🗂️ Project Structure
```bash
rag_course_catalog/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py             # API entry point
│   │   ├── routes.py           # API routes
│   │   ├── retrieval.py        # Query embedding + MongoDB vector search
│   │   ├── generation.py       # AWS Bedrock LLM call
│   │   └── utils.py            # PDF chunking, embeddings
│   └── requirements.txt
├── frontend/                   # ReactJS frontend
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── ChatBox.jsx
│   │   │   ├── QueryInput.jsx
│   │   └── api.js              # Axios client
│   └── package.json
├── ingestion/                 # PDF embedding scripts
│   ├── embedder.py            # Chunk + embed PDFs using Titan
│   └── utils.py
├── .env.example
├── README.md
└── docker-compose.yml         # For Redis, MongoDB
```


📦 .env.example
```bash
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/rag
REDIS_HOST=localhost
REDIS_PORT=6379
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=amazon.titan-embed-text-v1
BEDROCK_ACCESS_KEY=
BEDROCK_SECRET_KEY=
S3_BUCKET_NAME=rag-course-catalogs
```

🚀 Quickstart Instructions

## 1. Clone Repository
git clone https://github.com/yourusername/rag_course_catalog.git
cd rag_course_catalog

## 2. Setup Backend (WSL Ubuntu)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

## 4. Run Docker Services (MongoDB + Redis)
```bash
docker-compose up -d
```

## 5. Embed PDFs Using Titan Embeddings
```bash
cd ingestion
python embedder.py --path /path/to/pdf_folder
```

## 🧪 Testing

Open React app at http://localhost:5173
Type queries like:
"What are the prerequisites for computer architecture in MIT?"
Backend will fetch documents, query AWS Bedrock with Titan Embeddings, and show results.

## 📤 Deployment

Backend: Package with Dockerfile and deploy on AWS Lambda via API Gateway
Frontend: Deploy with Amplify, S3 static hosting, or Vercel
Data: Store PDFs in AWS S3, vector embeddings in MongoDB Atlas, cache in Redis

## 🔐 Authentication & Logging (Optional)

Add AWS Cognito for sign-in
Enable CloudWatch logs for backend

## 📚 References
MongoDB Atlas Vector Search
AWS Bedrock API
Amazon Titan Embeddings
