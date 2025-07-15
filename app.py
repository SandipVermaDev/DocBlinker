import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to extract text from uploaded PDFs
def pdf_to_text(pdf_docs):
    text="" 
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    return text_splitter.split_text(text)

# Function to create a vector store from text chunks
def get_vectorstore(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_texts(text_chunks, embeddings)
    vectorstore.save_local("faiss_index")    

# Function to create a conversation chain for question answering
def get_conversation_chain():
    Prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in the provided context, 
    say exactly "Answer is not available in the provided context", don't provide the wrong answer \n\n
    Context:\n{context}?\n 
    Question:\n{question}\n

    Answer:
    """

    # Use "gemini-1.5-flash" or "gemini-2.5-flash" for the best free-tier experience.
    # "gemini-1.5-flash" is very stable. "gemini-2.5-flash" is the latest.
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    # If "gemini-2.5-flash" causes issues (e.g., if it's still a specific preview name),
    # you can try "gemini-1.5-flash" or "gemini-1.5-flash-latest".
    # For a direct model ID, sometimes "models/gemini-2.5-flash" is also used, but
    # "gemini-2.5-flash" often works as an alias in LangChain.

    prompt=PromptTemplate(template=Prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Function to handle user input and generate response
def user_input(user_question):
    if not os.path.exists("faiss_index"):
        st.error("Please upload and process PDF documents first.")
        return

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question, k=3)

    chain = get_conversation_chain()

    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    print(response)
    st.write("Answer:", response['output_text'])

def main():
    st.set_page_config(page_title="PDF Question Answering", page_icon=":book:")
    st.header("PDF Question Answering with LangChain and Google Generative AI")

    user_question = st.text_input("Enter your question about the PDF documents:")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader("Upload PDF documents and Click on the Submit and Process", type=["pdf"], accept_multiple_files=True)
        if st.button("Submit and Process"):
            with st.spinner("Processing..."):
                if pdf_docs:
                    text = pdf_to_text(pdf_docs)
                    text_chunks = get_text_chunks(text)
                    get_vectorstore(text_chunks)
                    st.success("PDF documents processed and vector store created successfully!")
                else:
                    st.error("Please upload at least one PDF document.")

if __name__ == "__main__":
    main()