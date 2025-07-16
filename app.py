import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import shutil
import datetime
from docx import Document

from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to extract text from uploaded files
def extract_text_from_file(uploaded_file):
    text = ""
    if uploaded_file.type == "application/pdf":
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(io.BytesIO(uploaded_file.getvalue()))
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

# Function to process multiple files
def files_to_text(files):
    text = ""
    for file in files:
        text += extract_text_from_file(file)
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

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    prompt=PromptTemplate(template=Prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Function to handle user input and generate response
def user_input(user_question):
    if not os.path.exists("faiss_index"):
        return "Error: Please upload and process documents first."

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question, k=3)

    chain = get_conversation_chain()

    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    return response['output_text']

# Function to export chat with timestamps
def export_chat():
    if not st.session_state.messages:
        return None
    
    chat_text = ""
    for message in st.session_state.messages:
        timestamp = message.get("timestamp", "")
        role = message["role"].capitalize()
        content = message["content"]
        chat_text += f"{timestamp}{role}: {content}\n\n"
    
    return chat_text

def main():
    st.set_page_config(page_title="DocBlinker", page_icon=":book:")
    st.header("Document Question Answering with LangChain and Google Generative AI")

    # Add cyberpunk styling to buttons and sidebar
    st.markdown("""
    <style>
        div.stButton > button:first-child {
            background: linear-gradient(90deg, #00eeff, #bd00ff) !important;
            color: white !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 10px 25px !important;
            font-weight: bold;
            transition: all 0.3s ease;
            width: 100%;
            margin: 8px 0 !important;
            box-shadow: 0 0 10px rgba(0, 238, 255, 0.5) !important;
        }
        
        div.stButton > button:first-child:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 20px rgba(0, 238, 255, 0.8) !important;
        }
        
        div.stDownloadButton > button:first-child {
            background: linear-gradient(90deg, #00eeff, #bd00ff) !important;
            color: white !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 10px 25px !important;
            font-weight: bold;
            transition: all 0.3s ease;
            width: 100%;
            margin: 8px 0 !important;
            box-shadow: 0 0 10px rgba(0, 238, 255, 0.5) !important;
        }
        
        div.stDownloadButton > button:first-child:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 20px rgba(0, 238, 255, 0.8) !important;
        }
        
        .cyber-header {
            font-family: 'Arial', sans-serif;
            font-size: 2.8rem;
            text-align: center;
            background: linear-gradient(270deg, #00eeff, #ff00ff, #00ff9d, #bd00ff);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 10px rgba(0, 238, 255, 0.7);
            margin-bottom: 1.5rem;
            animation: gradient-shift 3s ease infinite, glow-pulse 1.5s ease infinite alternate;
        }
        
        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes glow-pulse {
            0% { text-shadow: 0 0 10px rgba(0, 238, 255, 0.7); }
            100% { text-shadow: 0 0 20px rgba(0, 238, 255, 0.9), 
                             0 0 30px rgba(189, 0, 255, 0.7),
                             0 0 40px rgba(255, 0, 255, 0.5); }
        }
        
        .chat-management-title {
            font-family: 'Arial', sans-serif;
            font-size: 1.4rem;
            color: #00eeff;
            text-align: center;
            letter-spacing: 2px;
            margin: 15px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    #Clear vector store on app start/refresh
    if 'cleared' not in st.session_state:
        if os.path.exists("faiss_index"):
            shutil.rmtree("faiss_index")
        st.session_state.cleared = True
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

     # Input box at bottom (centered)
    if user_question := st.chat_input("Enter your question about the documents:"):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S - ")
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user", 
            "content": user_question,
            "timestamp": timestamp
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_question)
        
        # Get response
        response = user_input(user_question)
        response_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S - ")
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "timestamp": response_timestamp
        })


    with st.sidebar:
        # DocBlinker header with cyberpunk styling
        st.markdown('<div class="cyber-header">DOCBLINKER</div>', unsafe_allow_html=True)
        
        uploaded_files = st.file_uploader("Upload documents (PDF or Word) and click Submit & Process", type=["pdf", "docx"], accept_multiple_files=True)
        
        # Process button with cyberpunk styling
        if st.button("Submit and Process", key="process_btn"):
            with st.spinner("Processing..."):
                if uploaded_files:
                    if os.path.exists("faiss_index"):
                        shutil.rmtree("faiss_index")

                    text = files_to_text(uploaded_files)
                    text_chunks = get_text_chunks(text)
                    get_vectorstore(text_chunks)
                    st.success("Documents processed successfully!")
                else:
                    st.error("Please upload at least one document.")

        # Chat management section
        st.divider()
        st.markdown('<div class="chat-management-title">CHAT MANAGEMENT</div>', unsafe_allow_html=True)

         # Export chat button
        chat_text = export_chat()
        if chat_text:
            st.download_button(
                label="Export Chat",
                data=chat_text,
                file_name=f"chat_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key="download_chat",
                on_click=lambda: st.success("Chat exported successfully!"),
            )
        
        # Clear chat button with cyberpunk styling
        if st.button("Clear Chat", key="clear_chat"):
            st.session_state.messages = []
            st.session_state.chat_cleared = True
            st.rerun()

        # Show success message after rerun
        if st.session_state.get("chat_cleared", False):
            st.success("Chat history cleared!")
            st.session_state.chat_cleared = False 
    
        # Reset session button with cyberpunk styling
        if st.button("Reset Session", key="reset_session"):
            if os.path.exists("faiss_index"):
                shutil.rmtree("faiss_index")
            st.session_state.messages = []
            st.session_state.cleared = True
            st.success("Session reset complete!")

if __name__ == "__main__":
    main()