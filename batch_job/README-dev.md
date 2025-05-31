
## Setup Python virtual environment
bijut@b:~/rag_course_catalog$ python -m venv .venv
bijut@b:~/rag_course_catalog$ chmod +x .venv/bin/activate
bijut@b:~/rag_course_catalog$ source .venv/bin/activate
(.venv) bijut@b:~/rag_course_catalog$ 

pip freeze | grep fake-useragent >> requirements.txt
