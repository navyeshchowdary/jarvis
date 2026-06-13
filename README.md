# 🤖 Jarvis AI - Intelligent Web Search Chatbot

A Perplexity-like AI chatbot that answers any question using live web search results.

## 🚀 Features
- 🔍 Live web search using SerpAPI
- 🤖 AI-powered answers using Groq (LLaMA 3.3)
- 💬 Chat history with memory
- 📚 Sources sidebar with clickable links
- 🗑️ Clear chat button

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **AI Model**: LLaMA 3.3 70B via Groq API
- **Web Search**: SerpAPI (Google Search)
- **Language**: Python

## ⚙️ How It Works
1. User asks a question
2. Jarvis searches Google using SerpAPI
3. Top 5 results are sent to LLaMA AI model
4. AI generates a clean, accurate answer
5. Sources are displayed in the sidebar

## 🔧 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/jarvis.git
cd jarvis
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add API keys
Create a `.env` file:
GROQ_API_KEY=your_groq_key_here

SERPAPI_KEY=your_serpapi_key_here

### 5. Run the app
```bash
streamlit run app.py
```

## 📸 Demo
Ask Jarvis anything:
- "Latest IPL 2026 news"
- "Who is the Prime Minister of India?"
- "Best places to visit in India"
- "Virat Kohli recent matches"

## 🌐 Live Demo
[Click here to try Jarvis](https://your-app-url.streamlit.app)

## 👨‍💻 Author
Made by Navyesh chowdary
