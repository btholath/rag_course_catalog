cd backend
bijut@b:~/rag_course_catalog/backend$ python3 -m venv .venv
bijut@b:~/rag_course_catalog/backend$ source .venv/bin/activate
(.venv) bijut@b:~/rag_course_catalog/backend$ pip install -r requirements.txt

(.venv) bijut@b:~/rag_course_catalog/backend$ which python
/home/bijut/rag_course_catalog/backend/.venv/bin/python

Check uvicorn Uses the Same Python Environment
(.venv) bijut@b:~/rag_course_catalog/backend$ which uvicorn
/home/bijut/rag_course_catalog/backend/.venv/bin/uvicorn
(.venv) bijut@b:~/rag_course_catalog/backend$ pip install uvicorn --force-reinstall
(.venv) bijut@b:~/rag_course_catalog/backend$ uvicorn app.main:app

Run below commands to reactivate the virtual environment.
(.venv) bijut@b:~/rag_course_catalog/backend$
deactivate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload


(.venv) bijut@b:~/rag_course_catalog/backend$ which python
/home/bijut/rag_course_catalog/backend/.venv/bin/python
(.venv) bijut@b:~/rag_course_catalog/backend$ which uvicorn
/home/bijut/rag_course_catalog/backend/.venv/bin/uvicorn
(.venv) bijut@b:~/rag_course_catalog/backend$ 



# Start the FastAPI app
Option 1: Run Without --reload (Safe for Now)
This bypasses the reloader subprocess issue:
uvicorn app.main:app --host 127.0.0.1 --port 8000

Then visit:
http://localhost:8000/docs

Option 2: Force Uvicorn to Use Your .venv Python
Run with the Python interpreter from your venv:

.venv/bin/python -m uvicorn app.main:app --reload
This ensures the subprocess uses the right interpreter.


uvicorn app.main:app --reload
Once running, visit:

Test API in Swagger
Open your browser:
Swagger UI: http://localhost:8000/docs
Health check: http://localhost:8000/health

You’ll see the Swagger UI:
GET /health – check server status
POST /query – enter a prompt to test retrieval + generation

Test API from CLI
curl http://localhost:8000/health


Next Step (Optional): Enable Live Reload Safely
If you want hot reloading during development:
pip install "uvicorn[standard]"
# This installs the necessary reloader dependencies (watchgod, etc.) which behave more consistently with virtual environments.
.venv/bin/python -m uvicorn app.main:app --reload

(.venv) bijut@b:~/rag_course_catalog/backend$ python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('MONGO_URI'))"
mongodb\x3a//localhost\x3a27017
(.venv) bijut@b:~/rag_course_catalog/backend$ 


Run Unit Tests
Make sure you're in the backend virtual environment and run:

cd backend
source .venv/bin/activate
pytest tests
You should see output like:
test_api.py::test_health PASSED

Run with Docker (Optional)
If you want to run the backend using Docker:


cd backend
docker build -t rag-backend .
docker run -p 8000:8000 --env-file ../.env rag-backend
Now access: http://localhost:8000/docs


