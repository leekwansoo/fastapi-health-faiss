from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import WordTextSplitter
from langchain.text_splitter import SentenceTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def embed_text(text):
    # initialize a Text Splitter
    text_splitter = CharacterTextSplitter(separator="\n", 
                    chunk_size =1000,                           chunk_overlap=200)

    #  Split the text into chunks
    chunks = text_splitter.split_text(text)
    
    # Convert the chunks to into langchain as Document objects
    documents = [Document(text=chunk) for chunk in chunks]
    
    #embedding text(documents):
    # Initialize OpenAI Embeddings 
    embeddings = OpenAIEmbeddings()
    # Create a vectorstore
    vectorstore = FAISS.from_documents(documents, embeddings)
    # Embed the documents
    for doc in documents:
        doc.embedding = embeddings.embed(doc.text)
        
    return documents, vectorstore