from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

pdf_path = "app/politics.pdf"
faiss_index_path = "faiss_index_"
content = ''
# base_url = 'https://en.wikipedia.org'
url = 'https://en.wikipedia.org/wiki/Politics_of_India'
response = requests.get(url)
if(response.status_code == 200):
  
  soup = BeautifulSoup(response.text, 'html.parser')
  text = (soup.get_text())
  if text :
    print("URL data fetched success")
    content = text
  print(soup.get_text())

 



# loading the embedding model from huggingface
# embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
# model_kwargs = {"device": "cpu"}  #here change cpu with cuda for gpu
# embeddings = HuggingFaceEmbeddings(
#   model_name=embedding_model_name,
#   model_kwargs=model_kwargs
# )


# if os.path.exists(faiss_index_path):
#     print("Loading existing FAISS index...")
#     persisted_vectorstore = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
# else:
#     print("FAISS index not found. Creating a new one...")
#     # Load and process the document
#     loader = PyPDFLoader(pdf_path)
#     documents = loader.load()

#     # Split the document into chunks
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
#     docs = text_splitter.split_documents(documents=documents)

#     # Create a FAISS vectorstore
#     persisted_vectorstore = FAISS.from_documents(docs, embeddings)

#     # Save the FAISS index for future use
#     persisted_vectorstore.save_local(faiss_index_path)
#     print("FAISS index created and saved.")

# # creating a retriever on top of database
# retriever = persisted_vectorstore.as_retriever()

# # Initialize an instance of the Ollama model
# llm = OllamaLLM(model="llama3.1")
# # Invoke the model to generate responses
# # response = llm.invoke("Tell me a joke")
# # print(response)
   



#  #Use RetrievalQA chain for orchestration
# qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# while True:
#   query = input("Type your query if you want to exit type Exit: \n")
#   if query == "Exit" :
#     break
#   result = qa.invoke(query)
#   print(result)