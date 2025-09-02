import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
import io
import os
import json 
import shutil
from modules.pdf_reader import parse_pdf, generate_question_with_genai, create_query_file, load_pdf, add_qa_file, check_qafile_exist, load_pdf_with_page_number
from modules.faissdb import store_pdf_documents
from modules.query_handler import query_faiss_db
from langchain_core.documents import Document
from graph import search_web
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

class QueryBody(BaseModel):
    file_name: str
    query: str

class Body(BaseModel):
    query: str

@app.get("/")
def welcome():
    return {"message": "Welcome to the FastAPIApp!"}


@app.post("/upload_pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    description: str = Form(...)
):
    #print(file)
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    file_name = os.path.basename(file.filename)
    print("Uploaded file:", file_name)
    print("Description:", description)
    file_path = os.path.join("uploaded_files", file_name)
    os.makedirs("uploaded_files", exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # process the uploaded file
    text = parse_pdf(file_path)
    documents = load_pdf_with_page_number(file_path)
    #print(documents)
    result = store_pdf_documents(documents)
    if not result:
        return {"description": description, "status": "File upload failed."}
    else:
        query_list= generate_question_with_genai(text)
        query_file = create_query_file(file_name, query_list)
        return {"query_file": query_file, "query_list":query_list}


@app.post("/query_from_documents")
def query_from_documents(body: QueryBody):
    print(body)
    response = check_qafile_exist(body.file_name, body.query)
    if response:
        return {"answer": response["answer"], "suffix": "Get Answer from Home Brewed QA store"}
    else:
        response = query_faiss_db(body.query)
        if response:
            qa_pair = {"query": body.query, "answer": response.content}
            qa_file = add_qa_file(body.file_name, qa_pair)
            return {"answer": response.content, "suffix": f"QA pair is saved in {qa_file}"}

@app.post("/web_search")
def web_search(body: Body):  
    query = body.query
    print(query)
    response = search_web(query) # using the web search module in graph.py
    if response:
        return {"results": response, "suffix": "Get Answer from Web Search"}
    else:
        return {"results": [], "suffix": "No results found"}


import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
