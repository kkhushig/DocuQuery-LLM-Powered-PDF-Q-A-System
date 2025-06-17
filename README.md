# DocuQuery – LLM-Powered PDF Q&A System

## 🧠 Overview
**DocuQuery** is an intelligent chatbot that allows users to upload one or more PDF files and ask questions based on their contents. The system leverages OpenAI's LLM, LangChain, and FAISS to process, embed, and query document text, delivering context-aware answers in real time via a sleek Streamlit web interface.

This project was built as part of DSCI-560 (Data Science Professional Practicum) at [Your Institution].

---

## 📚 Motivation
Modern information retrieval is often bottlenecked by unstructured documents like PDFs. We wanted to streamline the experience of searching through documents by enabling users to simply "chat" with their files — making research, instruction-following, or document review significantly faster and easier.

---

## ⚙️ Technologies Used
- **Python**
- **Streamlit** – Web interface
- **PyPDF2** – PDF text extraction
- **LangChain** – Text splitting, embedding logic, and conversational memory
- **OpenAI API** – For embeddings and LLM-based Q&A
- **FAISS** – Vector database for efficient similarity search

---

## 📂 Project Structure

```
DocuQuery/
│
├── app/                     
│   ├── code.py              
│   └── chatbot.py             
│
├── data         
└── README.md           
```

---

## 🧱 System Architecture

### 1. 📥 PDF Upload & Text Extraction
- PDF files are uploaded via Streamlit.
- Text is extracted using `PyPDF2`.

### 2. 🧩 Chunking
- The extracted text is split into overlapping 200-character chunks with a 50-character overlap to maintain context.

### 3. 🧠 Embedding
- Each chunk is transformed into a vector using OpenAI embeddings.

### 4. 📦 Vector Storage
- FAISS is used to store and query embeddings.

### 5. 💬 Conversation Chain
- LangChain's `ConversationalRetrievalChain` connects the user query, FAISS-retrieved context, and OpenAI's LLM to produce meaningful answers.

---

## 💻 Web Interface

The chatbot features:
- **Multiple PDF Uploads**
- **Real-time processing status**
- **An intuitive Chat Interface**
- **Modern dark theme UI**

---

## 🛠️ How to Run

### Setup
```bash
# Clone the repo
git clone https://github.com/your-username/DocuQuery.git
cd DocuQuery

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # For Unix
# .venv\Scripts\activate     # For Windows

# Install dependencies
pip install -r requirements.txt
```

### Run the App
```bash
streamlit run code.py
```

---

## 🚀 Features to Improve
- Add multi-user session support
- Integrate document summarization
- Support non-PDF formats (e.g., DOCX, TXT)
- Allow exporting of conversation history
