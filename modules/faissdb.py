# Initialize FAISS index (change dim to match your embedding size)
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import os
# 임베딩
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
# dimension_size = 1536
# 임베딩 차원 크기를 계산
dimension_size = len(embeddings.embed_query("hello world"))
print(dimension_size)

# define the FAISS DB
# if db is already exist load it from local db
faiss_path = "faiss_db"
if not os.path.exists(faiss_path):
    db = FAISS(
        embedding_function=embeddings,
        index=faiss.IndexFlatL2(dimension_size),
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    
else:
    # 저장된 데이터를 로드
    db = FAISS.load_local(
    folder_path="faiss_db",
    index_name="faiss_index",
    embeddings=embeddings,
    allow_dangerous_deserialization=True,
)
    

# Vector 저장소 생성 (FAISS.from_documents)
#db = FAISS.from_documents(documents=split_doc1, embedding=OpenAIEmbeddings())

# Vector 저장소 생성 (FAISS.from_documents)
def store_pdf_documents(documents):
    # add documents to existing db
    db.add_documents(
    documents = documents)
    # 로컬 Disk 에 저장
    db.save_local(folder_path="faiss_db", index_name="faiss_index")
    response = "documents are stored in faiss)"
    #print(db.index_to_docstore_id)
    return response

def store_text_documents(documents):
    # add documents to existing db
    db.add_documents(
    documents = documents)
    # 로컬 Disk 에 저장
    db.save_local(folder_path="faiss_db", index_name="faiss_index")
    response = "documents are stored in faiss)"
    #print(db.index_to_docstore_id)
    return response

def store_image_documents(documents):
    # add documents to existing db
    db.add_documents(
    documents = documents)
    # 로컬 Disk 에 저장
    db.save_local(folder_path="faiss_db", index_name="faiss_index")
    response = "documents are stored in faiss)"
    #print(db.index_to_docstore_id)
    return response   
   

def search_documents(query, k):
    # return as documents
    results = db.similarity_search(query, k=k)
    #print(results)
    return results
