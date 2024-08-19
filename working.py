from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()
Groqclient  =   Groq(api_key=os.getenv("GROQ_API_KEY"))
client      =   chromadb.PersistentClient(path="instance")

def get_text_from_pdf(file):
    text        =   ''
    pdf_reader  =   PdfReader(file)
    for page in range(len(pdf_reader.pages)):
        pageText =  pdf_reader.pages[page]
        text    +=  pageText.extract_text()
    return text

def get_text_chunks(text):
    text_splitter   =   RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks          =   text_splitter.split_text(text)
    return chunks

def embeddingStore(chunks):
    collection      =   client.get_or_create_collection(
        name        =   "embeddings",
        metadata    =   {"hnsw:space": "cosine"}
    )
    collection.add(
        documents   =   chunks,
        ids         =   [f'id{i}' for i in range(len(chunks))]
    )

def loadCollection():
    collection      =   client.get_collection(
        name        =   "embeddings"
    )
    return collection

def embeddingsQuery(user_question, collection):
    text            =   collection.query(
        query_texts =   user_question,
        n_results   =   1
    )
    return text['documents'][0][0]

def prompt(revlevantText):
    return f"""
        You are an AI chatbot trained to answer questions based on a given document of text. When provided with a question, you need to look 
        for relevant information in the provided document and give an appropriate answer. If the document does not contain information relevant 
        to the question, respond with "Answer not found in document.\n\n 
        Document:\n{revlevantText}\n
    """

def generate(revlevantText, user_question):
        yield f"<b>Question:</b> {user_question}\n<hr>\n<b>Answer: </b>"
        print(revlevantText)
        prp = prompt(revlevantText)
        print(prp)
        stream = Groqclient.chat.completions.create(
            messages    =   [
                {
                    "role"      :   "system",
                    "content"   :   prp
                },
                {
                    "role"      :   "user",
                    "content"   :   user_question,
                }
            ],
            model       =   "llama3-8b-8192",
            temperature =   0.5,
            max_tokens  =   1024,
            top_p       =   1,
            stop        =   None,
            stream      =   True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield(chunk.choices[0].delta.content.encode('utf-8'))