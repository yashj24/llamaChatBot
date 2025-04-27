from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
import os

# FastAPI app
app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class QueryRequest(BaseModel):
    query: str

# File and model setup
pdf_path = "app/politics.pdf"
faiss_index_path = "faiss_index_"
embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}  # use "cuda" for GPU
embeddings = HuggingFaceEmbeddings(
    model_name=embedding_model_name,
    model_kwargs=model_kwargs
)

# Load or create FAISS vectorstore
if os.path.exists(faiss_index_path):
    persisted_vectorstore = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
else:
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
    docs = text_splitter.split_documents(documents=documents)
    persisted_vectorstore = FAISS.from_documents(docs, embeddings)
    persisted_vectorstore.save_local(faiss_index_path)

# Setup retriever and LLM
retriever = persisted_vectorstore.as_retriever()
llm = OllamaLLM(model="llama3.1")
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# Endpoint to handle queries
@app.post("/api/query")
async def handle_query(request: Request):
    data = await request.json()  
    print(data)                  
    query = data.get('query')     
    print(query)
    
    response = qa.invoke(query)
    return {"response": response['result']} if isinstance(response, dict) else {"response": str(response)}
