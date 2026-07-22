# 🔎 AI Search Agent

An intelligent **Agentic AI Search Assistant** built with **LangGraph**, **Qdrant**, **Tavily**, and **Streamlit** that retrieves knowledge from a vector database, performs web search when necessary, summarizes new information, stores it for future retrieval, and generates concise, source-backed answers.

---

## 🚀 Features

- 🤖 Agentic workflow powered by LangGraph
- 🧠 Semantic search using Qdrant Vector Database
- 🌐 Live web search with Tavily
- 📝 Automatic web result summarization before response generation
- 💾 Incremental knowledge storage for future queries
- 🔄 Multi-LLM support (Gemini & Groq)
- 🔑 Bring Your Own API Keys (BYOK)
- 📚 Search history within the session
- 📖 Source-backed responses
- 📊 Telemetry with Logfire
- 🎨 Interactive Streamlit UI
- 🐳 Docker support

---

# 🏗️ Architecture

```
                    User Query
                         │
                         ▼
              Retrieve Knowledge (Qdrant)
                         │
                         ▼
                   Reasoning Agent
                  /               \
                 /                 \
        Enough Context?        Need Web Search?
             │                      │
             ▼                      ▼
      Generate Answer        Tavily Search
                                     │
                                     ▼
                               Summarization
                                     │
                                     ▼
                           Store in Qdrant
                                     │
                                     ▼
                              Generate Answer
```

---

# 🔄 LangGraph Workflow

```
START
   │
   ▼
retrieve_knowledge
   │
   ▼
reasoning
   │
   ├──────────────► generate_answer
   │
   ▼
search
   │
   ▼
summarization
   │
   ▼
store_knowledge
   │
   ▼
generate_answer
   │
   ▼
END
```

---

# 🛠️ Tech Stack

### AI & LLM

- LangGraph
- Google Gemini
- Groq
- Tavily Search API

### Vector Database

- Qdrant Cloud
- Sentence Transformers
- all-MiniLM-L6-v2

### Backend

- Python
- Pydantic v2
- Pydantic Settings

### Frontend

- Streamlit

### Observability

- Logfire
- Portkey AI Gateway

### DevOps

- Docker
- Git
- GitHub

---

# 📂 Project Structure

```
AI-Search-Agent/
│
├── app/
│   ├── agents/
│   ├── graph/
│   ├── llm/
│   ├── qdrant/
│   ├── search/
│   ├── telemetry/
│   ├── ui/
│   ├── utils/
│   └── main.py
│
├── Dockerfile
├── requirements.txt
├── README.md
└── .env.example
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/AI-Search-Agent.git
```

Navigate into the project

```bash
cd AI-Search-Agent
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GOOGLE_API_KEY=
GROQ_API_KEY=
TAVILY_API_KEY=
QDRANT_URL=
QDRANT_API_KEY=
PORTKEY_API_KEY=
```

Run the application

```bash
streamlit run main.py
```

---

# 🐳 Docker

Build the Docker image

```bash
docker build -t ai-search-agent .
```

Run the container

```bash
docker run -p 8501:8501 ai-search-agent
```

---

# 💡 How It Works

1. User submits a query.
2. The agent searches the Qdrant vector database for relevant knowledge.
3. The reasoning node determines whether the retrieved context is sufficient.
4. If sufficient, the agent generates a response.
5. Otherwise, it performs a Tavily web search.
6. Web results are summarized.
7. The summarized knowledge is stored in Qdrant.
8. The final response is generated using both retrieved and newly acquired knowledge.

---

# 📸 Demo

<img width="100%" alt="Demo Screenshot" src="docs/demo.png"/>

_(Replace with your application screenshot.)_

---

# 🔮 Future Improvements

- Streaming responses
- Multi-agent architecture
- Hybrid search
- Persistent chat history
- User authentication
- Citation highlighting
- Evaluation pipeline
- LangSmith integration
- Kubernetes deployment

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Saketh Peri**

- GitHub: https://github.com/perisaketh48
- LinkedIn: https://linkedin.com/in/sakethperi

---

⭐ If you found this project useful, consider giving it a star!
