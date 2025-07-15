import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import shutil 

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
        return "Error: Please upload and process PDF documents first."

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question, k=3)

    chain = get_conversation_chain()

    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    return response['output_text']

def main():
    st.set_page_config(page_title="PDF Question Answering", page_icon=":book:")
    st.header("PDF Question Answering with LangChain and Google Generative AI")

    #Clear vector store on app start/refresh
    if 'cleared' not in st.session_state:
        if os.path.exists("faiss_index"):
            shutil.rmtree("faiss_index")
        st.session_state.cleared = True
        st.session_state.messages = []

    # New chat interface with centered layout
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

     # Input box at bottom (centered)
    if user_question := st.chat_input("Enter your question about the PDF documents:"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_question})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_question)
        
        # Get response
        response = user_input(user_question)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader("Upload PDF documents and Click on the Submit and Process", type=["pdf"], accept_multiple_files=True)
        if st.button("Submit and Process"):
            with st.spinner("Processing..."):
                if pdf_docs:
                    # Clear previous data
                    if os.path.exists("faiss_index"):
                        shutil.rmtree("faiss_index")

                    text = pdf_to_text(pdf_docs)
                    text_chunks = get_text_chunks(text)
                    get_vectorstore(text_chunks)
                    st.success("PDF documents processed and vector store created successfully!")
                else:
                    st.error("Please upload at least one PDF document.")

        # Add chat management buttons
        st.divider()
        st.subheader("Chat Management")

         # Export chat button
        if st.button("Export Chat"):
            if st.session_state.messages:
                chat_text = "\n\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                st.download_button(
                    label="Download Chat History",
                    data=chat_text,
                    file_name="chat_history.txt",
                    mime="text/plain"
                )
            else:
                st.warning("No chat history to export")
        
        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.success("Chat history cleared!")
        
        # Reset session button
        if st.button("Reset Session"):
            if os.path.exists("faiss_index"):
                shutil.rmtree("faiss_index")
            st.session_state.messages = []
            st.session_state.cleared = True
            st.success("Session reset complete!")

if __name__ == "__main__":
    main()