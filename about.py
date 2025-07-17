import streamlit as st

def show_about_page():
    # Configure page metadata: title, favicon, and layout width
    st.set_page_config(
        page_title="About DocBlinker",
        page_icon="ℹ️",
        layout="wide"
    )

    # Inject custom CSS styles for neon cyberpunk theme and layout styling
    st.markdown("""
    <style>
        /* Animated gradient header for app title */
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

        /* Gradient animation */
        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Text glow pulse animation */
        @keyframes glow-pulse {
            0% { text-shadow: 0 0 10px rgba(0, 238, 255, 0.7); }
            100% { text-shadow: 0 0 20px rgba(0, 238, 255, 0.9),
                             0 0 30px rgba(189, 0, 255, 0.7),
                             0 0 40px rgba(255, 0, 255, 0.5); }
        }

        /* Container for all main content, centers and pads */
        .main-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 30px;
        }

        /* Sections with dark translucent background, rounded corners, and subtle neon shadow */
        .section {
            background: rgba(30, 30, 50, 0.85);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 35px;
            box-shadow: 0 0 25px rgba(0, 238, 255, 0.3);
        }

        /* Cards for each technology description */
        .tech-card {
            background: rgba(20, 20, 40, 0.85);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border-left: 4px solid #00eeff;
        }

        /* Highlights key terms in green */
        .highlight {
            color: #90ee90;
            font-weight: 600;
        }

        /* Footer styling with centered light text and spacing */
        .footer {
            text-align: center;
            font-size: 0.95rem;
            margin-top: 40px;
            margin-bottom: 20px;
            color: #ccc;
        }

        /* Footer links styled neon blue without underline */
        .footer a {
            color: #00eeff;
            text-decoration: none;
            margin: 0 8px;
        }

        /* Headings colored neon blue */
        h1, h2, h3 {
            color: #00eeff;
        }
    </style>
    """, unsafe_allow_html=True)

    # Open main content container
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    # App title with neon animated header
    st.markdown('<div class="cyber-header">DOCBLINKER</div>', unsafe_allow_html=True)

    # --- Overview Section ---
    st.markdown("""
    <div class="section">
        <h2>📚 What is DocBlinker?</h2>
        <p><strong>DocBlinker</strong> is your AI-powered document analyst — built to let you <strong>chat directly with PDFs and Word documents</strong>.</p>
        <p>Instead of reading through large documents manually, you just upload your files and ask questions. The system finds and understands the content for you — powered by cutting-edge natural language processing and vector similarity search.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Workflow Pipeline Section ---
    st.markdown("""
    <div class="section">
        <h2>⚙️ Workflow Pipeline</h2>
        <ol>
            <li><span class="highlight">Document Upload</span><br>
                Users upload <span class="highlight">.pdf</span> or <span class="highlight">.docx</span> files via the interface.
            </li>
            <li><span class="highlight">Text Extraction</span><br>
                - PDFs are processed with <span class="highlight">PyPDF2</span><br>
                - Word files are parsed with <span class="highlight">python-docx</span>
            </li>
            <li><span class="highlight">Chunking</span><br>
                Documents are split into overlapping chunks using <span class="highlight">LangChain’s RecursiveCharacterTextSplitter</span> for optimal context retention.
            </li>
            <li><span class="highlight">Embeddings</span><br>
                Each chunk is vectorized using <span class="highlight">Google’s models/embedding-001</span> through <span class="highlight">GoogleGenerativeAIEmbeddings</span>.
            </li>
            <li><span class="highlight">FAISS Storage</span><br>
                Chunks are stored in a <span class="highlight">FAISS vector database</span> for rapid similarity search.
            </li>
            <li><span class="highlight">Semantic Retrieval</span><br>
                Your query retrieves top-matching chunks from FAISS using cosine similarity.
            </li>
            <li><span class="highlight">Answer Generation</span><br>
                Relevant chunks are passed to <span class="highlight">Gemini 2.5 Flash</span> using <span class="highlight">ChatGoogleGenerativeAI</span> to generate responses.
            </li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    # --- Technology Stack Section ---
    st.markdown('<div class="section"><h2>🧠 Technology Stack</h2>', unsafe_allow_html=True)

    # Each tech card details a key component in your app architecture
    st.markdown("""
    <div class="tech-card">
        <h3>🤖 Google Gemini 2.5 Flash</h3>
        <p>- <span class="highlight">Role:</span> Final response generation</p>
        <p>- <span class="highlight">Why:</span> Fast and highly accurate LLM</p>
        <p>- <span class="highlight">Accessed via:</span> LangChain's <span class="highlight">ChatGoogleGenerativeAI</span></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tech-card">
        <h3>🔍 Google Embeddings - models/embedding-001</h3>
        <p>- <span class="highlight">Purpose:</span> Convert document chunks into dense vectors</p>
        <p>- <span class="highlight">Used with:</span> <span class="highlight">GoogleGenerativeAIEmbeddings</span></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tech-card">
        <h3>🔗 LangChain Framework</h3>
        <p>- Manages text chunking, embedding, and chaining prompts</p>
        <p>- Used modules: <span class="highlight">TextSplitter</span>, <span class="highlight">FAISS Retriever</span>, and <span class="highlight">StuffDocumentsChain</span></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tech-card">
        <h3>📊 FAISS Vector Store</h3>
        <p>- Stores and retrieves top relevant chunks</p>
        <p>- Efficient for semantic similarity search over large docs</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tech-card">
        <h3>🌐 Streamlit Interface</h3>
        <p>- Upload UI, chat interface, session control, and history export</p>
        <p>- Styled using custom CSS with a futuristic neon look</p>
    </div>
    """, unsafe_allow_html=True)

    # Close the technology stack container div
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Footer Section ---
    st.markdown("""
    <div class="footer">
        Developed by <strong>Sandip Verma</strong> |
        <a href="https://github.com/SandipVermaDev" target="_blank">GitHub</a> |
        <a href="https://www.linkedin.com/in/sandip-verma-dev" target="_blank">LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)