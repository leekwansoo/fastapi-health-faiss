# modules/pdf_parser.py
import json
from pathlib import Path
import os
from PIL import Image
import pytesseract
import csv
from PyPDF2 import PdfReader
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
# 요약문을 작성하기 위한 프롬프트 정의 (직접 프롬프트를 작성하는 경우)
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

model = "gpt-4o-mini"

# CharacterTextSplitter를 사용하여 텍스트를 청크(chunk)로 분할하는 코드
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
)

def parse_pdf(file_path):
    reader = PdfReader(file_path)
    num_page = len(reader.pages)
    #extract text from each page
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
      
def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

def load_pdf_with_page_number(pdf_file):
    reader = PdfReader(pdf_file)
    documents = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        # Get the last non-empty line (likely the page number)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        page_number = lines[-1] if lines else str(i + 1)
        # Remove the page number from the text if needed
        if lines and lines[-1] == page_number:
            text = '\n'.join(lines[:-1])
        # Create a Document with metadata
        doc = Document(page_content=text, metadata={"page_number": page_number})
        documents.append(doc)
    return documents

def load_image_with_page_number(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    # Get the page number from the image file name (assuming format: foldername/filename_pageX.jpg)
    page_number = image_file.split("_")[-1].split(".")[0]
    doc = Document(page_content=text, metadata={"page_number": page_number})
    return [doc]

def check_file_exist(dir, file_name):
    file_name = file_name
    file_list = os.listdir(dir)
    file_exist = False
    for file in file_list:
        if file == file_name:
            file_exist = True
            return file_exist

def generate_question_with_genai(text):
    prompt = f"Please generate questions from the given {text}/,the questionnaire should be in same language as given text/the generated query form should be json format like {{\"question\": \"\"}}/don't generate answer"

    # Set your API key (you can also set it as an environment variable)
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(prompt)
    questions = response.text  # or response.candidates[0].text for some versions
    return questions   

def generate_question_ollama(text):
    llm = ChatOllama(model="llama3.2:latest", temperature = 0.2)
    prompt1 = f"Please generate questions from the given {text}/,the questionnare should be in same language as given text"
    prompt2 = f"You are a helpful questionnare creator. Please generate 10 questionnares that can be used for query from the context of given{text}/n, the questionnare should be in korean language as much possible, but the medical and chemical terminologies should remain in english"
    prompt = ChatPromptTemplate.from_template(
    "Please generate questions from the given {text}/, the questionnaire should be in same language as given text"
    )
    chain = prompt | llm | StrOutputParser()
    questions = chain.invoke({"text": text})
    #print(questions.content)
    return questions

def generate_question(text):
    prompt = f"Please generate questions from the given {text}/,the questionnare should be in same language as given text/the generated query form should be json format like {{\"question\": \"\"}}/don.t generate answer"

    llm = ChatOpenAI(model= model, temperature = 0.2)
    questions = llm.invoke(prompt)
    return questions

def create_query_file(file_name, text):
    file_name = file_name.split('.')[0]
    query_file = "query/" + f"{file_name}" + "_query.txt"
    with open(query_file, "w", encoding="utf-8") as f:
        f.write(text)
    return query_file

def add_qa_file(file_name, qa_pair):
    #print(file_name)
    file_name = file_name.split('.')[0].split('/')[1]
    qa_file = "qa_pair/" + f"{file_name}" + "_qa.txt"

    # Check if the file exists
    if not os.path.exists(qa_file):
        # If the file doesn't exist, create an empty list
        qa_list = []
        with open(qa_file, "w", encoding="utf-8") as f:
            json.dump(qa_list, f, ensure_ascii=False, indent=4)
    # Read the existing data
    with open(qa_file, "r", encoding="utf-8") as f:
        qa_list = json.load(f)
        # Append the new Q&A pair to the list
    qa_list.append(qa_pair)
    # Write the updated list back to the file
    with open(qa_file, "w", encoding="utf-8") as f:
        json.dump(qa_list, f, ensure_ascii=False, indent=4)

    return qa_file

# if query already exist return the query and answer
def check_qafile_exist(file_name, query):
    # convert file_name to qa_file
    file_name = file_name.split('.')[0].split('/')[1]
    qa_file = f"{file_name}" + "_qa.txt"
    qa_files = os.listdir("qa_pair")
    # if file is existing in the qa_files_list then read the json file
    for file in qa_files:
        #print(file)
        if qa_file == file:
            print(file)
            qa_file = "qa_pair/" + f"{qa_file}"
            #print(qa_file)
            qa_pair_list = json.loads(Path(qa_file).read_text(encoding= "utf-8"))
            for qa_pair in qa_pair_list:            
                if query == qa_pair["query"]:
                    #print(qa_pair)
                    return qa_pair
    return None

def extract_text_from_image(image_path):
    print(image_path)
    """
    Extract text from a .jpg image using OCR (pytesseract).
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='eng+kor')
    return text

def save_text_as_csv(image_path, text):
    """
    Save extracted text from image as a CSV file (one row).
    Returns the CSV file path.
    """
    base = os.path.splitext(os.path.basename(image_path))[0]
    csv_path = os.path.join("uploaded", f"{base}.csv")
    with open(csv_path, "w", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["text"])
        writer.writerow([text])
    return csv_path

def save_list_to_file(file_name, data_list):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("\n".join(data_list))  # Join the list with newline and write to the file
    print(f"File '{file_name}' created successfully!")
