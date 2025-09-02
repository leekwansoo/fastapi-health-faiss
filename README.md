Open AI 를 이용하여 Upload된 건강생활 잡지 PDF File 에서부터 Query 를 추출하고 Query file 과 Query-Answer pair file 로 webzine Reader Service를 제공함
app.py:  Streamlit Entry
mainapp.py:  Webzine Service Main Flow 
  Functions: Main Menu
    OpenAI Credential Entry
    Upload PDF File
    Query From Uploaded File

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