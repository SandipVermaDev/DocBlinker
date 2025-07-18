# 🚀 DocBlinker

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-Chat%20App-ff4b4b?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-Document%20QA-00eeff?logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-ffb300?logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/FAISS-Vector%20Search-00ff9d?logo=faiss&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776ab?logo=python&logoColor=white" />
</p>

<h1 align="center">DocBlinker</h1>

<p align="center">
  <b>Chat with your PDF and Word documents using AI!</b><br>
  <i>Upload, ask, and get instant answers from your files.</i>
</p>

---

<!-- ## 🌐 Live Demo

<p align="center">
  <a href="https://your-streamlit-app-link-here" target="_blank">
    <img src="https://img.shields.io/badge/Launch%20App-Streamlit-ff4b4b?logo=streamlit&logoColor=white&style=for-the-badge" alt="Streamlit App" />
  </a>
</p>

> **[👉 Click here to try DocBlinker live!](https://your-streamlit-app-link-here)**

---

## 🎬 Demo GIF

<p align="center">
  <img src="demo/demo.gif" alt="DocBlinker Demo" width="700" />
</p>

--- -->

## ✨ Features

- 📄 **Multi-file Upload:** Supports PDF and DOCX files, multiple at once.
- 🧠 **AI-Powered Q&A:** Ask questions and get context-aware answers from your documents.
- ⚡ **Fast & Accurate:** Uses Google Gemini 2.5 Flash and semantic search for reliable results.
- 🗂️ **Local Vector Store:** Efficient document retrieval with FAISS.
- 🖥️ **Modern UI:** Cyberpunk-inspired Streamlit interface with chat, export, and reset features.
- 🔒 **Privacy First:** All processing is local (except for embedding/LLM API calls).

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/):** Interactive web UI
- **[LangChain](https://python.langchain.com/):** Document parsing, chunking, and chains
- **[Google Gemini 2.5 Flash](https://ai.google.dev/):** LLM for answer generation
- **[Google Generative AI Embeddings](https://ai.google.dev/):** Semantic vector embeddings
- **[FAISS](https://github.com/facebookresearch/faiss):** Local vector similarity search
- **[PyPDF2](https://pypi.org/project/PyPDF2/):** PDF text extraction
- **[python-docx](https://pypi.org/project/python-docx/):** Word document parsing
- **[dotenv](https://pypi.org/project/python-dotenv/):** Environment variable management

---

## 🚀 Getting Started

### 1. **Clone the Repository**
```bash
git clone https://github.com/SandipVermaDev/DocBlinker.git
cd DocBlinker
```

### 2. **Install Dependencies**
It is recommended to use a virtual environment.
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. **Set Up Environment Variables**
Create a `.env` file in the project root and add your Google API key:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. **Run the App**
```bash
streamlit run app.py
```

---

## 💡 Usage

1. **Upload** your PDF or DOCX files using the sidebar.
2. Click **Submit and Process** to index your documents.
3. **Ask questions** in the chat interface about your documents.
4. **Export** or **clear** your chat history as needed.
5. Use the **About** page for more info on the project pipeline and tech.

---

## 📦 Project Structure

```
DocBlinker/
├── app.py           # Main Streamlit app
├── about.py         # About page
├── requirements.txt # Python dependencies
├── faiss_index/     # Vector store (auto-generated)
├── venv/            # Virtual environment (optional)
└── ...
```

---

## 🙋 FAQ

**Q: Is my data safe?**
> Yes! Your documents are processed locally. Only embeddings and queries are sent to Google APIs for LLM/embedding.

**Q: What file types are supported?**
> PDF and DOCX (Word) files.

**Q: Can I upload multiple files?**
> Yes, you can upload and process multiple documents at once.

**Q: How do I reset or clear the chat?**
> Use the sidebar buttons to clear chat or reset the session.

---

## 👨‍💻 Author

Made with ❤️ by [Sandip Verma](https://github.com/SandipVermaDev)

[![GitHub](https://img.shields.io/badge/GitHub-SandipVermaDev-181717?logo=github)](https://github.com/SandipVermaDev)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-sandip--verma--dev-0a66c2?logo=linkedin)](https://www.linkedin.com/in/sandip-verma-dev)

---

## ⭐️ Star this repo if you like it! 