import streamlit as st

def show_about_page():
    st.set_page_config(
        page_title="About DocBlinker",
        page_icon="ℹ️",
        layout="wide"
    )

    st.markdown("""
    <style>
        .cyber-header {
            font-family: 'Arial', sans-serif;
            font-size: 2.8rem;
            text-align: center;
            background: linear-gradient(270deg, #ffe600, #ffae00, #fff700, #ffd700);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 10px rgba(255, 230, 0, 0.7);
            margin-bottom: 1.5rem;
            animation: gradient-shift 3s ease infinite, glow-pulse 1.5s ease infinite alternate;
        }

        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes glow-pulse {
            0% { text-shadow: 0 0 10px rgba(255, 230, 0, 0.7); }
            100% { text-shadow: 0 0 20px rgba(255, 230, 0, 0.9),
                             0 0 30px rgba(255, 174, 0, 0.7),
                             0 0 40px rgba(255, 247, 0, 0.5); }
        }

        .main-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 30px;
        }

        .section {
            background: rgba(50, 50, 10, 0.85);
            border: 2px solid #ffe600;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 35px;
            box-shadow: 0 0 25px rgba(255, 230, 0, 0.3);
        }

        .section:hover {
            border: 2px solid #ffae00;
            box-shadow: 0 0 32px 6px rgba(255, 230, 0, 0.7);
        }

        .tech-card {
            background: rgba(60, 60, 20, 0.85);
            border: 1px solid #ffe600;
            border-radius: 20px;
            padding: 20px;
            margin: 15px 0;
            border-left: 6px solid #ffe600;
        }

        .tech-card:hover {
            border: 2px solid #ffae00;
            box-shadow: 0 0 32px 6px rgba(255, 230, 0, 0.7);
            border-left: 8px solid #ffae00;
        }

        .highlight {
            color: #ffe600;
            font-weight: 600;
        }

        .footer {
            text-align: center;
            font-size: 0.95rem;
            margin-top: 40px;
            margin-bottom: 20px;
            color: #ffe600;
        }

        .footer a {
            color: #ffae00;
            text-decoration: none;
            margin: 0 8px;
        }

        .footer a:hover {
            color: #00ff00;
            text-decoration: underline;
        }

        h1, h2, h3 {
            color: #ffe600;
        }

        .feature-list {
            padding-left: 20px;
            margin-top: 10px;
        }

        .feature-list li {
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<div class="cyber-header">DOCBLINKER</div>', unsafe_allow_html=True)

    # --- Overview ---
    st.markdown("""
    <div class="section">
        <h2>📚 What is DocBlinker?</h2>
        <p><strong>DocBlinker</strong> is your personal AI assistant that helps you <strong>chat with PDF and Word documents</strong> effortlessly.</p>
        <p>Whether you're reviewing contracts, reports, research papers, or e-books — just upload the file and ask questions. DocBlinker understands the content and provides instant, accurate answers.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Pipeline ---
    st.markdown("""
    <div class="section">
        <h2>⚙️ How It Works</h2>
        <ol>
            <li><span class="highlight">File Upload</span><br>
                Upload <span class="highlight">.pdf</span> and <span class="highlight">.docx</span> files through a user-friendly interface.<br>
                Supports multiple documents at once (resets existing session on upload).
            </li>
            <li><span class="highlight">Text Extraction</span><br>
                Uses <span class="highlight">PyPDF2</span> for PDFs and <span class="highlight">python-docx</span> for Word files.
            </li>
            <li><span class="highlight">Chunking</span><br>
                Splits documents using <span class="highlight">LangChain’s RecursiveCharacterTextSplitter</span> with:
                <ul class="feature-list">
                    <li><span class="highlight">Chunk size:</span> 1000 tokens</li>
                    <li><span class="highlight">Overlap:</span> 200 tokens</li>
                </ul>
            </li>
            <li><span class="highlight">Embeddings</span><br>
                Each chunk is transformed into vectors using <span class="highlight">GoogleGenerativeAIEmbeddings</span> (<span class="highlight">models/embedding-001</span>).
            </li>
            <li><span class="highlight">Vector Store</span><br>
                Chunks are indexed with <span class="highlight">FAISS</span> for fast and efficient similarity search.
            </li>
            <li><span class="highlight">Query Processing</span><br>
                On user input, top <span class="highlight">3 most relevant chunks</span> are retrieved using semantic similarity.
            </li>
            <li><span class="highlight">Answer Generation</span><br>
                Uses <span class="highlight">Gemini 2.5 Flash</span> via <span class="highlight">ChatGoogleGenerativeAI</span> with a prompt designed to:
                <ul class="feature-list">
                    <li>Ensure <span class="highlight">factual and grounded</span> responses</li>
                    <li>Include <span class="highlight">user query + context chunks</span></li>
                    <li>Use <span class="highlight">temperature: 0.3</span> for stable outputs</li>
                    <li>Return <span class="highlight">"Answer is not available in the provided context"</span> if answer can't be found</li>
                </ul>
            </li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    # --- Tech Stack ---
    st.markdown('<h2>🧠 Technology Stack</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="tech-card">
        <h3>🤖 Google Gemini 2.5 Flash</h3>
        <p>- <span class="highlight">Role:</span> Generates final answers using context-aware reasoning</p>
        <p>- <span class="highlight">Features:</span> Fast generation, stable outputs, context reasoning</p>
        <p>- <span class="highlight">Used via:</span> <span class="highlight">ChatGoogleGenerativeAI</span></p>
    </div>

    <div class="tech-card">
        <h3>🔍 Google Embeddings (models/embedding-001)</h3>
        <p>- <span class="highlight">Role:</span> Converts document chunks into semantic vectors</p>
        <p>- <span class="highlight">Used via:</span> <span class="highlight">GoogleGenerativeAIEmbeddings</span></p>
    </div>

    <div class="tech-card">
        <h3>📦 FAISS</h3>
        <p>- <span class="highlight">Purpose:</span> Local vector similarity search</p>
        <p>- <span class="highlight">Features:</span> Fast retrieval using cosine similarity</p>
    </div>

    <div class="tech-card">
        <h3>🔗 LangChain</h3>
        <p>- <span class="highlight">Key Tools:</span> RecursiveCharacterTextSplitter, FAISS, create_stuff_documents_chain</p>
        <p>- <span class="highlight">Role:</span> Powers document parsing, chunking, embedding, and chain creation</p>
    </div>

    <div class="tech-card">
        <h3>💻 Streamlit</h3>
        <p>- <span class="highlight">UI:</span> Drag-and-drop file upload, chat interface</p>
        <p>- <span class="highlight">Features:</span> Export chat history, reset session, real-time chat with timestamps</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""
    <div class="footer">
        Built by <strong>Sandip Verma</strong> |
        <a href="https://github.com/SandipVermaDev" target="_blank">GitHub</a> |
        <a href="https://www.linkedin.com/in/sandip-verma-dev" target="_blank">LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
