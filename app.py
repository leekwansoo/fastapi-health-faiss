import http
import streamlit as st 
import os
import json 
import requests
import io
from langchain_community.document_loaders import TextLoader
from doc_handler import check_file_exist
from graph import search_web


from dotenv import load_dotenv
load_dotenv()

st.title("Webzine for SCL Health")

openai_api_key = st.sidebar.text_input("Enter Your OPENAI_API_KEY")
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
    st.sidebar.write("반갑습니다, Welcome to SCL-HEALTH_WEBZINE")
    
st.session_state["DOCUMENT"] = []

st.session_state["DOCUMENT"] = os.listdir("uploaded")

doc_list =[st.session_state["DOCUMENT"]]


if "query_input" not in st.session_state:
    st.session_state["query_input"] = ""

# Move set_query_input to the front part of the code
def set_query_input(q):
    st.session_state['query_input'] = q
    print(st.session_state['query_input'])

st.session_state["query_message"] = []
st.session_state["query_file"] = []

def check_document(value):
    if value not in st.session_state["DOCUMENT"]:
        result = "noexist"
        return(result)
    else:
        result = "exist"
        return(result)
       
def add_document(value):   
    if "DOCUMENT" not in st.session_state: 
        st.session_state["DOCUMENT"] = []     
    st.session_state["DOCUMENT"].append(value)
    st.write(f"Document added: {value}") 

# Example usage # List Document
def list_documents(): 
    if st.session_state["DOCUMENT"]:
        docs = st.session_state["DOCUMENT"]
        return(docs)
    else: st.write("No documents found in 'DOCUMENT'.")
    
def handle_query(file_name, query):
    json_container = {"file_name": file_name, "query": query}
    print(json_container)
    response = requests.post("http://localhost:8080/query_from_documents", json=json_container).json()
 
    if response:
        st.write(response["answer"])
        st.write(response["suffix"])
        

 # Create a sidebar for navigation
st.sidebar.title("Menu")
options = st.sidebar.radio("Select an option", ["Upload File", "Query from Uploaded File", "List Query-Answer from Uploaded File","Web Search"])

if options == "Upload File":
    st.sidebar.header("Upload File")
    uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf", key="pdf_uploader")
    
    if uploaded_file:
        file_name = uploaded_file.name
        dir_name = "uploaded_files"
        check_exist = check_file_exist(dir_name, file_name)
        if check_exist == False:
            # store the file in the uploaded file folder
            uploaded_name = f"{dir_name}/{file_name}"
            with open(uploaded_name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            # upload to main server for processing
            response = requests.post("http://localhost:8080/upload_pdf", files={"file": uploaded_file}, data={"description": "Uploaded via Streamlit"}).json()

            if response:
                print(response)
                file_name = response["query_file"]
                add_document(file_name)    # store it in st.session_state
                st.session_state["query_file"].append(file_name)
                for question in response["query_list"]:
                    st.session_state["query_message"].append(question)
                st.sidebar.markdown(response["query_list"])

                docs = list_documents()
                if docs:
                    for doc in docs:
                        st.sidebar.write(f"Uploaded_Document: {doc}\n")
            else:
                st.sidebar.write("storing PDF file into vector store failed")
        else:
            st.sidebar.write(f"{file_name} is already uploaded\n")     
    else:
        st.sidebar.write("Please upload a PDF and select subject to get started.")
        
            
elif options == "Query from Uploaded File":
      
    st.header("Query from Uploaded File")
    query_file_list = os.listdir("query")
    selected = st.sidebar.selectbox("Select document to query", query_file_list)
    file_name = f"query/{selected}"
    # make query as list in the query_file
    loader = TextLoader(file_name, encoding="utf-8")
    documents = loader.load()
    query_list = documents[0].page_content.split("\n")  # Corrected context

    # Use session_state to allow sidebar button to set the text_input value
    def set_query_input(q):
        st.session_state['query_input'] = q
        print(st.session_state['query_input'])

    query_input = st.text_input(
        "Enter your question for your uploaded documents:",
        key="query_key_0",
        value=st.session_state["query_input"]
    )
    if query_input:
        if st.button("Get Answer", key="get_answer_button"):
            handle_query(file_name, query_input)

    to_delete = None
    i = 0
    for query in query_list:
        i += 1
        query = query.strip().rstrip(',')
        if query.startswith('{') and query.endswith('}'):
            query_dict = json.loads(query)
            st.sidebar.write(query_dict["question"])
            col1, col2 = st.sidebar.columns([1, 1])
            with col1:
                st.button(
                    "Query",
                    key=f"button_{i}",
                    on_click=set_query_input,
                    args=(query_dict["question"],)
                )
            with col2:
                if st.button(f"Delete", key=f"delete_{i}"):
                    to_delete = i - 1
    if to_delete is not None:
        query_list.pop(to_delete)
        st.rerun()
    
    
elif options == "List Query-Answer from Uploaded File":
    qa_file_list = os.listdir("qa_pair")
    selected = st.sidebar.selectbox("Select document to list queries", qa_file_list)
    file_name = f"qa_pair/{selected}"
    st.header(f"List Query-Answer from Uploaded File: {selected}")
    if st.button("List Query-Answer pairs"):
        # make query as list in the query_file
        with open(file_name, "r", encoding="utf-8") as f:
            qa_pair_list = json.load(f)
        st.write(f"Listing Query-Answer pairs from {selected}:")
        for qa_pair in qa_pair_list:
            st.write(f"**Query:** {qa_pair['query']}")
            st.write(f"**Answer:** {qa_pair['answer']}")
            st.write("---")
    

        # Add download button for QA pairs
        if len(qa_pair_list) > 0:
            download_content = json.dumps(qa_pair_list, ensure_ascii=False, indent=2)
            buffer = io.StringIO(download_content)
            st.download_button(
                label="Download QA Pair List",
                data=buffer.getvalue(),
                file_name=f"{selected}",
                mime="application/json"
            )
        
elif options == "Web Search":
    st.header("Web Search")
    query = st.text_input("Enter a search query:")
    if st.button("Search Web"):
        if query:
            data = {"query": query}
            print(data)
            results = requests.post("http://localhost:8080/web_search", json=data).json().get("results", [])
            for result in results:
                st.write(result["content"])
        else:
            st.write("Please enter a search query.")