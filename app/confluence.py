from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA, LLMChain
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_ollama import OllamaLLM
import os


custom_prompt = PromptTemplate(
    template="""You are a helpful assistant. Answer the question strictly based on the following context. 
    If the answer is not found in the context, say "I don't know."
    
    Context:
    {context}
    
    Question:
    {question}
    """,
    input_variables=["context", "question"]
)


embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)


txt_path = "spacedata.txt"
faiss_index_path = "conf_faiss_index_"


if os.path.exists(faiss_index_path):
    print("Loading existing FAISS index...")
    persisted_vectorstore = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
else:
    print("FAISS index not found. Creating a new one...")
   
    loader = TextLoader(txt_path, encoding="utf-8")
    documents = loader.load()

    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents=documents)

    
    persisted_vectorstore = FAISS.from_documents(docs, embeddings)

   
    persisted_vectorstore.save_local(faiss_index_path)
    print("FAISS index created and saved.")


retriever = persisted_vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3} 
)


llm = OllamaLLM(model="llama3.1")

# 🔥 Create LLMChain with the prompt
llm_chain = LLMChain(llm=llm, prompt=custom_prompt)

stuff_chain = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_variable_name="context",
    document_separator="\n\n"
)


combine_documents_chain = MapReduceDocumentsChain(
    llm_chain=llm_chain,  # Correct usage here
    reduce_documents_chain=stuff_chain,  # Reduce the result using StuffDocumentsChain
    document_variable_name="context",
    return_intermediate_steps=False
)


qa = RetrievalQA(
    retriever=retriever,
    combine_documents_chain=combine_documents_chain,
    return_source_documents=True  # Return sources for debugging
)


while True:
    query = input("Type your query (or type 'Exit' to quit): \n")
    if query.lower() == "exit":
       
        break
    
    result = qa.invoke(query)
    print("\nAnswer:", result["result"])
    
    # Show sources if available
    if "source_documents" in result:
        print("\nSources Used:")
        for doc in result["source_documents"]:
            print(f"- {doc.metadata.get('source', 'Unknown')}")
