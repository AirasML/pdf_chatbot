# PDF Chat Assistant 📄

An intelligent document interaction tool built with Streamlit and LangChain that allows users to have natural conversations with their PDF documents. Upload any PDF and ask questions to get relevant, context-aware responses powered by OpenAI's language models.

## 🌟 Features

- **PDF Processing**: Upload and process any PDF document
- **Interactive Chat**: Ask questions naturally about your document's content
- **Smart Responses**: Get AI-powered answers with context from your document
- **User-Friendly Interface**: Clean and intuitive Streamlit-based UI
- **Secure**: Your OpenAI API key is handled securely

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-chat-assistant.git
cd pdf-chat-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to the provided local URL

## 🔧 Requirements

- Python 3.8+
- OpenAI API key
- Required packages (see requirements.txt)

## 💻 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**: 
  - LangChain for document processing and conversation chains
  - OpenAI's GPT-3.5 for text generation
  - FAISS for vector storage and similarity search
  - OpenAI's text-embedding-ada-002 for document embeddings

## 🔒 Security Note

The application requires an OpenAI API key to function. The key is stored securely in memory during runtime and is never persisted to disk.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License

This project is [MIT](LICENSE) licensed.

---

### 📊 Repository Stats
![GitHub stars](https://img.shields.io/github/stars/yourusername/pdf-chat-assistant?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/pdf-chat-assistant?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/pdf-chat-assistant)
![GitHub license](https://img.shields.io/github/license/yourusername/pdf-chat-assistant)

### Short Description (for GitHub)
> A Streamlit-based application that enables natural conversation with PDF documents using LangChain and OpenAI's GPT models. Upload any PDF and start asking questions! 