import streamlit as st
import os
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import tempfile

# Initialize session state variables
if 'conversation' not in st.session_state:
    st.session_state.conversation = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'api_key_confirmed' not in st.session_state:
    st.session_state.api_key_confirmed = False

# Set up the page
st.set_page_config(page_title="PDF Chat Assistant", page_icon="📄")
st.title("PDF Chat Assistant 📄")
st.subheader("Upload any PDF and chat with its contents!")

# API Key Input Section
if not st.session_state.api_key_confirmed:
    api_key_input = st.text_input("Enter your OpenAI API key:", type="password", key="api_key_input_field")
    if st.button("Submit API Key"):
        if api_key_input:
            os.environ["OPENAI_API_KEY"] = api_key_input
            st.session_state.api_key_confirmed = True
            st.rerun()
        else:
            st.warning("Please enter a valid OpenAI API key.")

# Main Application Logic - only if API key is confirmed
if st.session_state.api_key_confirmed:
    # Initialize OpenAI components
    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=os.environ["OPENAI_API_KEY"],
            show_progress_bar=True
        )
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    except Exception as e:
        st.error(f"Error initializing OpenAI components: {e}")
        st.session_state.api_key_confirmed = False
        st.stop()

    def process_document(uploaded_file):
        """Process the uploaded PDF document and create a vector store."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        try:
            loader = PyPDFLoader(tmp_file_path)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            document_chunks = text_splitter.split_documents(documents)
            vector_store = FAISS.from_documents(document_chunks, embeddings)
            return vector_store
        finally:
            os.unlink(tmp_file_path)

    def initialize_conversation(vector_store):
        """Initialize the conversation chain with the vector store."""
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        conversation = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
            memory=memory,
            return_source_documents=True,
            verbose=True
        )
        return conversation

    # File upload section
    uploaded_file = st.file_uploader("Upload your PDF document", type=['pdf'])

    if uploaded_file and not st.session_state.vector_store:
        with st.spinner("Processing your document..."):
            st.session_state.vector_store = process_document(uploaded_file)
            if st.session_state.vector_store:
                st.session_state.conversation = initialize_conversation(st.session_state.vector_store)
                st.success("Document processed successfully! You can now ask questions about its contents.")
            else:
                st.error("Failed to process the document. Please try again.")

    # Chat interface
    if st.session_state.conversation:
        user_question = st.text_input("What would you like to know about the document?")
        if user_question:
            try:
                with st.spinner("Analyzing document and generating response..."):
                    response = st.session_state.conversation.invoke({
                        "question": user_question,
                        "chat_history": st.session_state.chat_history
                    })
                    
                    if not response.get("source_documents"):
                        st.warning("I couldn't find relevant information in the document to answer your question. Please try asking something else.")
                    else:
                        st.write("Answer:", response["answer"])
                        
                    st.session_state.chat_history.extend([
                        (user_question, response["answer"])
                    ])
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    elif st.session_state.vector_store:
        st.info("Conversation not initialized. This might indicate an issue with document processing or API key.")
    else:
        st.info("👆 Start by uploading a PDF document above.")

elif not st.session_state.api_key_confirmed:
    st.info("Please enter your OpenAI API key and click 'Submit API Key' to begin.") 