Setup MongoDB Atlas
https://cloud.mongodb.com/v2/6835fa9838c0a0503900c9b4#/overview

Option 1: Use MongoDB Atlas with Vector Search Enabled
Create a free cluster on MongoDB Atlas.
Enable Vector Search.

Update your .env:

MONGO_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/rag"

Make sure your vector index is created on the documents collection:
{
"mappings": {
"dynamic": false,
"fields": {
"embedding": {
"type": "knnVector",
"dimensions": 1536, // match your Titan embedding dim
"similarity": "cosine"
}
}
}
}
======================================================
Step-by-Step: MongoDB Atlas + Vector Search
🟢 1. Create an Atlas Account
Visit: https://www.mongodb.com/cloud/atlas/register

Sign up or log in.

🏗 2. Create a Free Cluster
Click “Build a Database”

Choose Shared (free) plan

Select AWS & a region close to your app (e.g., us-east-1)

Cluster name: rag-cluster

🔐 3. Create a Database User
Go to Database > Database Access

Add new user:

Username: rag_user

Password: StrongPassword123!

Role: Atlas Admin (for now)

🌐 4. Allow IP Access
Go to Network Access > IP Access List

Click Add IP Address

Choose Allow Access from Anywhere (0.0.0.0/0) or your IP

📦 5. Connect to Cluster
Go to Clusters > Connect > Connect Your Application

Copy your connection string:

bash
Copy
Edit
mongodb+srv://rag_user:StrongPassword123@rag-cluster.xxxxx.mongodb.net/rag
Update your .env:

env
Copy
Edit
MONGO_URI=mongodb+srv://rag_user:StrongPassword123@rag-cluster.xxxxx.mongodb.net/rag
📁 6. Create documents Collection
You can use MongoDB Atlas UI:

Go to Browse Collections

Create a new database: rag

Create a collection: documents

🧠 7. Create a Vector Search Index
Go to:

Clusters > Browse Collections > rag > documents

Click Search Indexes > Create Search Index

Choose JSON editor and paste:

json
Copy
Edit
{
"mappings": {
"dynamic": false,
"fields": {
"embedding": {
"type": "knnVector",
"dimensions": 1536,
"similarity": "cosine"
},
"text": {
"type": "string"
}
}
}
}
Name: default
Vector field: embedding

✅ 8. Restart Backend & Ingest
bash
Copy
Edit

# In backend/

uvicorn app.main:app --reload

# In ingestion/

python embedder.py --path ../pdfs
🧪 9. Test Retrieval
From Swagger UI:

POST /debug/retrieve
{
"query": "What are the courses offered in AI?"
}
Should return relevant PDF chunks from MongoDB Atlas vector search.

# Let me know if you want a script to automate the MongoDB Atlas setup using Terraform or Atlas CLI, or if you prefer a visual walkthrough.
