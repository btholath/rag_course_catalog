
(.venv) bijut@b:~/rag_course_catalog$ deactivate
bijut@b:~/rag_course_catalog$ 
(.venv) bijut@b:~/rag_course_catalog$ python -m venv .venv
(.venv) bijut@b:~/rag_course_catalog$ ls .venv/
bin  include  lib  lib64  pyvenv.cfg
(.venv) bijut@b:~/rag_course_catalog$ chmod +x .venv/bin/activate
(.venv) bijut@b:~/rag_course_catalog$ source .venv/bin/activate
(.venv) bijut@b:~/rag_course_catalog$ 
(.venv) bijut@b:~/rag_course_catalog/ingestion$ pip install PyMuPDF
(.venv) bijut@b:~/rag_course_catalog/ingestion$ pip install boto3
(.venv) bijut@b:~/rag_course_catalog/ingestion$ pip install pymongo sentence-splitter boto3 python-dotenv





Run MongoDB shell:
(.venv) bijut@b:~/rag_course_catalog$ mongosh
Current Mongosh Log ID: 683b262d1e571db091a120ba
Connecting to:          mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.0
Using MongoDB:          8.0.9
Using Mongosh:          2.5.0
mongosh 2.5.1 is available for download: https://www.mongodb.com/try/download/shell

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

------
   The server generated these startup warnings when booting
   2025-05-16T09:09:52.527-07:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2025-05-16T09:09:54.034-07:00: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
   2025-05-16T09:09:54.034-07:00: For customers running the current memory allocator, we suggest changing the contents of the following sysfsFile
   2025-05-16T09:09:54.034-07:00: We suggest setting the contents of sysfsFile to 0.
   2025-05-16T09:09:54.034-07:00: We suggest setting swappiness to 0 or 1, as swapping can cause performance problems.
------


Deprecation warnings:
  - Using mongosh with Node.js versions lower than 20.0.0 is deprecated, and support may be removed in a future release.
See https://www.mongodb.com/docs/mongodb-shell/install/#supported-operating-systems for documentation on supported platforms.
test> 
test> use rag
switched to db rag
rag> 

rag> db.createCollection("documents")
{ ok: 1 }
rag>

rag> exit
(.venv) bijut@b:~/rag_course_catalog$ 


Verify MongoDB connection
(.venv) bijut@b:~/rag_course_catalog/ingestion$ python -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017'); print(client.list_database_names())"
['admin', 'config', 'insurance_db', 'life_insurance', 'local', 'plant_monitor', 'rag', 'tholathdb']


Grant IAM user or role you're using has AWS Bedrock full access or explicit permission to bedrock:InvokeModel.
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeModel",
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
    }
  ]
}

for development purposes
{
  "Effect": "Allow",
  "Action": "bedrock:*",
  "Resource": "*"
}

For your RAG setup:
✅ Use Titan Text Embeddings V2 for the retriever/embedding step
✅ Use Titan Text G1 - Lite for the generator/response step


## Ingestion Pipeline

Setup MongoDB Atlas
  - Create a free-tier MongoDB Atlas cluster.
  - Enable "Vector Search" under Atlas Search (Beta).
  - Create a database named rag and a collection documents.

Upload PDFs
  - Place all course catalog PDFs in the pdfs/ directory locally.


Verifying Bedrock Model Access
 - Go to Amazon Bedrock Console
 - Switch to us-east-1 region
 - Click Model Access from the left panel
 - Look for Titan Text Embeddings V2 and Titan Text G1 - Lite
 - If status is Available to request, click Request access
 - Wait a few minutes, then retry embedding script


Reload Environment
After correcting the .env, reload it:
(.venv) bijut@b:~/rag_course_catalog$ export $(cat .env | xargs)


Run your ingestion script
(.venv) bijut@b:~/rag_course_catalog/ingestion$ python embedder.py --path ../pdfs


Verification of above embedder.py script once it's run is completed.
0. Check for Errors in Output
python embedder.py --path ../pdfs
If there are no exceptions or traceback errors, the script likely completed successfully.


1. Check MongoDB documents Collection Count
Run this in the Mongo shell:
mongosh
use rag
rag> db.documents.countDocuments()
2184
rag> 
If the number is > 0, embeddings have been stored.

## View a Sample Document
rag> db.documents.findOne()
... 
{
  _id: 'c701e0b9-f9f4-49f4-a17d-03e7ffeef11f',
  text: 'Fall Addendum 2002',
  embedding: [
      -0.05692437291145325,  -0.012583297677338123,    0.04363153874874115,
      0.002838154323399067,    0.01948215253651142,    0.03511504456400871,
      0.006557302083820105,  -0.010580520145595074,   -0.04067343473434448,
       0.04034814611077309,    0.00754045695066452,  -0.037240270525217056,
      0.012899098917841911,  -0.046955596655607224,  -0.015443136915564537,
     -0.006408210843801498,   -0.02265779674053192,  -0.023526592180132866,
     -0.024913815781474113,   -0.04373251646757126,    0.08311563730239868,
     0.0024200212210416794,    0.04077644273638725,   0.016774116083979607,
      -0.05737368017435074,  -0.026687324047088623,   0.016573520377278328,
        -0.039444450289011,    0.03343980386853218,   -0.02033332921564579,
       0.04637685418128967,   0.029243560507893562,   0.045426733791828156,
     -0.044402070343494415,    0.05315236747264862,    0.03867967799305916,
      -0.00227702921256423,    0.06934095919132233,  -0.020615248009562492,
      0.001827044878154993,    0.07242783159017563,   0.059204794466495514,
    -0.0022564444225281477,    0.00888583529740572,   0.017156332731246948,
       0.01688254624605179,   0.006381103303283453,   0.011981002986431122,
       0.03049829788506031,    0.06336647272109985,    0.02320129983127117,
       0.02527502365410328,  -0.025439023971557617,   0.006810756865888834,
      -0.01579553633928299,    0.07497389614582062,  -0.009728031232953072,
      0.005966920405626297,   0.023838328197598457,  -0.054426416754722595,
     -0.008004842326045036,   -0.02129090204834938, -0.0030926258768886328,
        0.0446866974234581,   0.004578455351293087,   -0.06126835197210312,
      -0.07468114048242569,  -0.020144931972026825,   -0.02677677758038044,
     -0.011554906144738197,    0.03603703901171684,    -0.0082569420337677,
      0.009446960873901844, -0.0006397368269972503,   -0.02728775516152382,
      -0.03623051941394806,  -0.014025416225194931,   0.011135756969451904,
       0.02329482138156891,   0.047703761607408524,   -0.06474895030260086,
     -0.041089534759521484,  0.0024374716449528933,   0.046107809990644455,
       0.03717521205544472,  -0.013437183573842049,   0.006761963479220867,
     -0.004636058583855629,   -0.03238803148269653,   -0.06428270787000656,
      0.019796602427959442,   0.009123026393353939,  -0.018582524731755257,
      0.004936274141073227,   -0.05909975245594978,   -0.04452676698565483,
      -0.07256675511598587,   -0.05914583429694176,  -0.020861247554421425,
      -0.02380967326462269,
    ... 924 more items
  ],
  source: 'catalog_02_Fall_Addendum.pdf',
  page: 2
}
rag> 

--Count Per Source
To see how many chunks per PDF were embedded:
rag> db.documents.aggregate([
...   { $group: { _id: "$source", count: { $sum: 1 } } },
...   { $sort: { count: -1 } }
... ])
... 
[ { _id: 'catalog_02_Fall_Addendum.pdf', count: 2184 } ]
rag> 


Explore the MongoDB wih MongoDB Compass (GUI)
https://www.mongodb.com/try/download/compass
Download MongoDB Compass
Connect using:
mongodb://localhost:27017


## backend code for the rag_course_catalog
## FastAPI app has been generated and is now saved in the canvas as Backend Fastapi Code. It includes:

main.py: FastAPI app entry
routes.py: Handles /query
retrieval.py: Embedding + MongoDB vector search
generation.py: Titan model via Bedrock
utils.py: PDF chunking
requirements.txt: Dependencies
 a Dockerfile, unit tests with pytest, and OpenAPI annotations in main.py for the FastAPI backend.
