Procedures to download and setup this package

step 1: download zip file from this repository and open in the vs code
step 2: from the vs code terminal create venv with "python -m venv venv"
step 3: change terminal with "venv/Scripts/activate
step 4: install depedncy modules with "pip install -r requirements.txt"
step 5: create .env file with your own credentials
step 6: open new terminal and execute step3
step 7: initaite fastapi server with "python main.py"
        check that FastAPI Server is Running
step 8: from anoyher terminal start streamlit app with "streamlit run app.py"
        you will see an app menu window with localhost:8501 popped up

Open AI 를 이용하여 Upload된 SCL 검사 Catalog PDF File 에서부터 Query 를 추출하고 Query file 과 Query-Answer pair file 로 검사항목 Catalog Reader Service를 제공함

app.py:  Webzine Service Main Flow 
  Functions: Main Menu
    OpenAI Credential Entry
    Upload PDF File
    Query From Uploaded File
main.py FastAPI Server to handle the execution of App_Menu
    upload_pdf
    query_from_documents
    web_search
    
    
modules.pdf_reader.py: Handle PDF file
  Functions:
    parse_pdf: Read the pdf and parse inti pages
    generate_query: generate queries from uploaded PDF File with LLM
    create_query_file: create query_file list of queries
    create_qa_file: create a file with list of question_answer pair for each query_file
    add_to_qa_file: add a qa_pair into a corresponding qa_file

modules.faiss_db.py: Handling of Faiss db
  Functions:
     store-vector data-into faiss_db
     similarty_search
graph.py
  Functions:
    web-search for entered query

## functional diagram
[Client Request]
      |
      v
--------------------------
| FastAPI Application    |
| (main.py / app.py)     |
--------------------------
      |
      v
+-------------------------------+
| @app.get("/")                 |----> welcome() - Returns welcome message
+-------------------------------+
| @app.post("/upload_pdf")      |----> upload_pdf() - Handles PDF upload, parsing, storing, and QA generation
+-------------------------------+
| @app.post("/query_from_documents") |----> query_from_documents() - Handles document QA retrieval and storage
+-------------------------------+
| @app.post("/web_search")      |----> web_search() - Handles web search queries
+-------------------------------+
      |
      v
--------------------------
|   Task Handlers         |
| (modules/...)           |
--------------------------
      |
      v
[PDF Parsing, FAISS DB, QA Generation, Web Search, etc.]