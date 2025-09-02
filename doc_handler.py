import streamlit as st
import os

st.title("Webzine for SCL Health")


st.session_state["DOCUMENT"] = []
doc_list =[]
#if st.session_state["DOCUMENT"] is None:
#   st.session_state["DOCUMENT"] = {"key": ""}
    
# Function to add data to DOCUMENT directory 
def check_document(value): 
    if value not in st.session_state["DOCUMENT"]:
        result = "noexist"
        return(result)
    else:
        result = "exist"
        return(result)
       
def add_document(value):         
    st.session_state["DOCUMENT"].append(value)
    st.write(f"Document added: {value}") 
# Function to retrieve data from DOCUMENT directory 
def retrieve_document(doc): 
    if doc in st.session_state["DOCUMENT"]: 
        return doc
    else: st.write(f"Document with key '{doc}' not found.") 
    return None 
# Example usage # List Document
def list_documents(): 
    if st.session_state["DOCUMENT"]:
        docs = st.session_state["DOCUMENT"]
        return(docs)
    else: st.write("No documents found in 'DOCUMENT'.")

def check_file_exist(dir_name, file_path):
    file_exist = False
    file_list = os.listdir(dir_name)
    for file in file_list:
        if file_path == file:
            file_exist = True
    return file_exist

def store_documents(documents):
    for doc in documents:
        if doc.type == "pdf":
            store_pdf_documents(doc)
            return ("Image documents stored successfully.")
        elif doc.type == "text":
            store_text_documents(doc)
            return ("Image documents stored successfully.")
        elif doc.type == "image":
            store_image_documents(doc)
            return ("Image documents stored successfully.")
        else:
            return ("document type is not supported.")