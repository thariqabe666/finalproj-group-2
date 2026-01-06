# 🛡️ AI Career Hub: Your Intelligent Career Co-Pilot

[![Standard](https://img.shields.io/badge/Status-Beta-blue.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-navy.svg)](https://langchain.com/)

**AI Career Hub** is a premium, multi-agent AI platform designed to bridge the gap between job seekers and their dream roles. By combining advanced Large Language Models (LLMs) with specialized agents, the platform offers a comprehensive suite of tools for career planning, job matching, and interview preparation.

---

## 🌟 Key Features

### 🚀 Career Co-Pilot
Upload your CV and let our intelligence engine do the heavy lifting.
- **Semantic Job Matching**: Uses RAG (Retrieval-Augmented Generation) via Qdrant to find jobs that match your skills, not just keywords.
- **Deep Match Analysis**: Get a compatibility score, detailed gap analysis, and actionable recommendations to improve your profile.
- **Automated CV Parsing**: Instantly extracts core skills and experience levels.

### 🎙️ Interactive Interview Simulator
Experience realistic interviews with our voice-enabled simulator.
- **Voice-to-Text Integration**: Speak your answers naturally using our OpenAI Whisper integration.
- **Dynamic Questioning**: The AI adapts to your responses, asking challenging follow-up questions tailored to the job description.
- **Comprehensive Evaluation**: Receive a detailed performance report with scores, strengths, and areas for improvement after every session.

### 💬 Smart Chat & Career Insights
A centralized hub for all your career-related queries.
- **Agent Orchestrator**: Intelligently routes your questions to specialized SQL or RAG agents.
- **Advanced Data Lookups**: Get real-time salary benchmarks and market trends from our structured SQLite database.

### 📝 Tailored Cover Letter Generator
Say goodbye to generic applications. Generate professional, role-specific cover letters that highlight your unique value proposition in seconds.

---

## 🤖 Meet the Agents

The system is powered by a coordinated team of specialized AI agents:

| Agent | Responsibility |
| :--- | :--- |
| **The Orchestrator** | The "Brain" – routing queries and managing the ReAct reasoning loop. |
| **The Advisor** | Your personal career coach – analyzing CVs and providing strategic advice. |
| **The Interviewer** | The expert recruiter – simulating high-stakes interviews with logic and empathy. |
| **SQL Agent** | The data scientist – querying structured job databases for precision analytics. |
| **RAG Agent** | The librarian – searching through unstructured job descriptions using vector embeddings. |
| **Cover Letter Expert** | The copywriter – crafting compelling narratives for your applications. |

---

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom Glassmorphism UI
- **Orchestration**: LangChain & LangGraph
- **Vector Database**: Qdrant (for semantic search)
- **Relational Database**: SQLite (for structured job data)
- **AI Models**: OpenAI GPT-4o / GPT-4-turbo, Whisper (for Speech-to-Text)
- **Observability**: Langfuse (for tracing and monitoring)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/thariqabe666/finalproj-group-2.git
cd finalproj-group-2
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory and add your API keys:
```env
OPENAI_API_KEY=your_openai_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

### 4. Initialize Databases
Run the setup scripts to populate your local databases with job data:
```bash
python src/database/setup_sql.py
python src/database/setup_qdrant.py
```

### 5. Launch the Application
```bash
streamlit run app.py
```

---

## 📸 Interface Preview

The application features a modern, high-performance UI including:
- **Glassmorphism Design Tokens**
- **Vibrant Gradient Typography**
- **Fluid Micro-animations**
- **Responsive Mobile-first Layout**

---

## 📈 Monitoring and Observability
We use **Langfuse** for enterprise-grade tracing. Every agent interaction, LLM call, and tool execution is recorded for performance tuning and quality assurance.

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

---

*Built with ❤️ by Final Project Group 2*
