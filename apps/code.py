import streamlit as st
import os
import PyPDF2
import warnings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI 
import openai
import time

warnings.filterwarnings("ignore")

# Set your OpenAI API Key directly in the code
openai.api_key = 'enter_your_own_API_key'

# Streamlit page configuration
st.set_page_config(page_title="PDF Chatbot", page_icon="📚", layout="wide")

# Custom CSS for a dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stSidebar {
        background-color: #262730;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stProgress > div > div > div {
        background-color: #4CAF50;
    }
    .stSelectbox {
        color: #ffffff;
    }
    .stTextInput>div>div>input {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📚 PDF Chatbot")
st.sidebar.markdown("---")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to chunk the extracted text
def chunk_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=200,
        chunk_overlap=50
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create embeddings
def create_embeddings(chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore

# Function to create conversation chain
def create_conversation_chain(vectorstore):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = ChatOpenAI(model='gpt-4o-mini', openai_api_key=openai.api_key)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever, memory=memory)
    return qa_chain

# Initialize session state
if 'conversations' not in st.session_state:
    st.session_state.conversations = {'Default': {'messages': [], 'pdfs': [], 'chain': None}}
if 'current_conversation' not in st.session_state:
    st.session_state.current_conversation = 'Default'

# Sidebar for conversation management
new_conversation = st.sidebar.text_input("Create new conversation:")
if st.sidebar.button("Create"):
    if new_conversation and new_conversation not in st.session_state.conversations:
        st.session_state.conversations[new_conversation] = {'messages': [], 'pdfs': [], 'chain': None}
        st.session_state.current_conversation = new_conversation

conversation_options = list(st.session_state.conversations.keys())
st.session_state.current_conversation = st.sidebar.selectbox("Select conversation:", conversation_options, index=conversation_options.index(st.session_state.current_conversation))

# Main content area
st.title(f"📚 PDF Chatbot - {st.session_state.current_conversation}")

# File uploader
uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type="pdf")

if uploaded_files:
    if st.button("Process PDFs"):
        current_conv = st.session_state.conversations[st.session_state.current_conversation]
        current_conv['pdfs'] = uploaded_files
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        all_text = ""
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing PDF {i+1}/{len(uploaded_files)}")
            text = extract_text_from_pdf(uploaded_file)
            all_text += text + "\n"
            progress_bar.progress((i + 1) / len(uploaded_files))
            time.sleep(0.1)  # Simulate processing time
        
        status_text.text("Chunking text...")
        chunks = chunk_text(all_text)
        progress_bar.progress(0.8)
        
        status_text.text("Creating embeddings...")
        vectorstore = create_embeddings(chunks)
        progress_bar.progress(0.9)
        
        status_text.text("Setting up conversation chain...")
        current_conv['chain'] = create_conversation_chain(vectorstore)
        progress_bar.progress(1.0)
        
        status_text.text("PDFs processed successfully!")
        time.sleep(1)
        status_text.empty()
        progress_bar.empty()
        
        st.success("PDFs processed successfully!")

# Chat interface
current_conv = st.session_state.conversations[st.session_state.current_conversation]

for message in current_conv.get('messages', []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Your question:"):
    current_conv['messages'].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if current_conv.get('chain'):
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            with st.spinner("Thinking..."):
                response = current_conv['chain']({"question": prompt})
                full_response = response["answer"]
            
            message_placeholder.markdown(full_response)
        
        current_conv['messages'].append({"role": "assistant", "content": full_response})
    else:
        st.warning("Please process PDFs before asking questions.")

# Display information about the current conversation
st.sidebar.markdown("---")
st.sidebar.subheader("Current Conversation Info")
st.sidebar.write(f"PDFs: {len(current_conv.get('pdfs', []))}")
st.sidebar.write(f"Messages: {len(current_conv.get('messages', []))}")
