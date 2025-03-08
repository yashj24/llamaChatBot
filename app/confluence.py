from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM

import os

txt_path = "spacedata.txt"
faiss_index_path = "conf_faiss_index_"



#loading the embedding model from huggingface
embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}  #here change cpu with cuda for gpu
embeddings = HuggingFaceEmbeddings(
  model_name=embedding_model_name,
  model_kwargs=model_kwargs
)


if os.path.exists(faiss_index_path):
    print("Loading existing FAISS index...")
    persisted_vectorstore = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
else:
    print("FAISS index not found. Creating a new one...")
    # Load and process the document
    loader = TextLoader(txt_path, encoding="utf-8")  # Replace txt_path with your .txt file path
    documents = loader.load()

    # Split the document into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
    docs = text_splitter.split_documents(documents=documents)

    # Create a FAISS vectorstore
    persisted_vectorstore = FAISS.from_documents(docs, embeddings)

    # Save the FAISS index for future use
    persisted_vectorstore.save_local(faiss_index_path)
    print("FAISS index created and saved.")

# creating a retriever on top of database
retriever = persisted_vectorstore.as_retriever()

# Initialize an instance of the Ollama model
llm = OllamaLLM(model="llama3.1")
# Invoke the model to generate responses
# response = llm.invoke("Tell me a joke")
# print(response)
   



 #Use RetrievalQA chain for orchestration
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

while True:
  query = input("Type your query if you want to exit type Exit: \n")
  if query == "Exit":
    break
  result = qa.invoke(query)
  print(result)