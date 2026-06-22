# 🤖 Adaptive AI Support Agent

An intelligent customer support system powered by Generative AI and Retrieval-Augmented Generation (RAG). This agent dynamically analyzes the user's input, classifies their persona (Technical Expert, Business Executive, or Frustrated User), and adapts its tone and response structure accordingly. 

If the agent cannot confidently resolve the issue using the internal knowledge base, it automatically triggers a safe escalation protocol, generating a structured JSON handoff for human support teams.

## ✨ Core Features
* **Dynamic Persona Classification:** Uses LLMs to detect sentiment, vocabulary, and intent to classify the user in real-time.
* **Context-Aware Responses (RAG):** Grounds all answers in an internal vector database (ChromaDB) built from proprietary troubleshooting guides and policies.
* **Intelligent Escalation:** Automatically calculates a retrieval confidence score and triggers a fallback to human support if the score drops below the safety threshold (0.40).
* **Interactive UI:** Built entirely in Python using Streamlit for a clean, chat-based user experience.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Frontend:** Streamlit
* **AI/LLM:** Google GenAI SDK (Gemini 3.5 Flash & Gemini Embedding 2)
* **Vector Database:** ChromaDB
* **Chunking & Parsing:** LangChain Text Splitters, PyPDF
