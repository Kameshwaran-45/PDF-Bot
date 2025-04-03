# PDF-Bot

Here's a comprehensive **README.md** file for your **PDF-Bot** repository, along with a **flowchart** to visualize the system architecture:

```markdown
# 📄 PDF-Bot - AI-Powered PDF Assistant

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25.0-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-0.0.200-00ADD8)
[![GitHub stars](https://img.shields.io/github/stars/Kameshwaran-45/PDF-Bot)](https://github.com/Kameshwaran-45/PDF-Bot/stargazers)

An AI chatbot that answers questions from uploaded PDFs using **Ollama (Mistral)** and **ChromaDB**. Perfect for researchers, students, and professionals!

👉 [Live Demo](#) | 📂 [GitHub Repo](https://github.com/Kameshwaran-45/PDF-Bot.git)

![PDF-Bot Screenshot](./assets/screenshot.png) *(Add your screenshot later)*

---

## 🌟 Features
- **Natural Language QA** from PDFs
- **Multi-PDF Support** (process multiple files)
- **Semantic Search** with ChromaDB
- **Conversational Memory** (remembers chat history)
- **Dark/Light Mode** UI

## 🛠️ Tech Stack
- **Backend**: Python, LangChain, Ollama (Mistral)
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers (`all-mpnet-base-v2`)
- **Frontend**: Streamlit

---

## 📥 Installation
1. **Clone the repo**:
   ```bash
   git clone https://github.com/Kameshwaran-45/PDF-Bot.git
   cd PDF-Bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Ollama** (for Mistral LLM):
   ```bash
   ollama pull mistral
   ```

4. **Launch the app**:
   ```bash
   streamlit run app.py
   ```

---

## 🔍 How It Works

```mermaid
flowchart TD
    A[User Uploads PDFs] --> B[Text Extraction]
    B --> C[Chunking\n(1000 chars overlap=200)]
    C --> D[Embedding\nall-mpnet-base-v2]
    D --> E[Store in ChromaDB]
    F[User Query] --> G[Embed Query]
    G --> H[Semantic Search]
    H --> I[Top 3 Relevant Chunks]
    I --> J[Generate Answer\nwith Mistral]
    J --> K[Display Response]
```

### Key Steps:
1. **PDF Processing**: Extract text → Split into chunks → Vectorize
2. **Query Handling**: Embed question → Find similar chunks → Generate answer
3. **UI**: Streamlit interface for seamless interaction

---

## 🚀 Usage
1. Upload PDFs via sidebar
2. Click "Process Documents"
3. Ask questions like:
   - _"What are the key findings?"_
   - _"Summarize page 5"_
   - _"List all references cited"_

---

## 📜 License
MIT © [Kameshwaran](https://github.com/Kameshwaran-45)

```

---

### 📌 **Flowchart Details** (ASCII version for quick reference):
```
┌─────────────┐   ┌──────────────┐   ┌───────────┐   ┌────────────┐
│  PDF Upload │ → │ Text Extract │ → │ Chunking │ → │ Embeddings │
└─────────────┘   └──────────────┘   └───────────┘   └────────────┘
                                      ↓
┌─────────────┐   ┌──────────────┐   ┌───────────────┐   ┌────────────┐
│ User Query  │ → │ Query Embed  │ → │ Semantic Search│ → │ Generate   │
└─────────────┘   └──────────────┘   └───────────────┘   │ Answer     │
                                                         └────────────┘
```

---

### 🖼️ **Assets to Add Later**:
1. Add a `screenshot.png` in `/assets/`
2. Update the demo link when deployed
3. Customize badges (e.g., add PyTorch if needed)

Let me know if you'd like to add **deployment instructions** (e.g., Docker, HuggingFace Spaces)! 🚀
