# 🤖 Agent Professional Career Assistant

A multi-agent AI system that analyzes job offers, compares them with your resume, and automatically generates a personalized cover letter.

---

## 📋 Description

This project implements a **multi-agent system** built with LangGraph and DeepAgents to automate the job application process. The agent:

1. Reads and indexes your PDF resume into a vector database
2. Scrapes the content of a job offer from a given URL
3. Calculates a match score between the resume and the job offer
4. Generates a professional, personalized cover letter in French

---

## 🏗️ Architecture

The system consists of a **coordinator agent** that orchestrates 4 specialized sub-agents:

```
Coordinator (DeepAgent)
├── retrieve-agent   → Extracts resume information via RAG
├── offer-agent      → Scrapes the job offer from URL
├── match-agent      → Calculates the CV/offer match score
└── writer-agent     → Writes the cover letter
```

### Execution Flow

```
[PDF Resume] → [ChromaDB (Vector Store)]
                        ↓
[Job offer URL] → [offer-agent] → [match-agent] → [writer-agent]
                                        ↑
                               [retrieve-agent]
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM (local inference) | Ollama — `mistral:7b-instruct` |
| Embeddings | MistralAI — `mistral-embed` |
| Agent orchestration | LangGraph + DeepAgents |
| Vector database | ChromaDB (Chroma) |
| Document loading | LangChain (PyPDFLoader, WebBaseLoader) |
| Environment variables | python-dotenv |

---

## 📁 Project Structure

```
Agent-Professional-career-assistant/
├── career_agent.py                  # Main agent (base version)
├── career_agent_rate_limit_safe.py  # Version with rate limit protection
├── app.py                           # Application interface
├── requirements.txt                 # Python dependencies
├── data/
│   ├── EDILENECV.pdf                # PDF resume (not included in the repository)
│   └── db/                          # Persisted vector store (auto-generated)
├── skills/
│   └── career-matching/             # Agent skills
└── .gitignore
```

---

## ⚙️ Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai/) installed and running locally
- A [MistralAI](https://console.mistral.ai/) API key (for embeddings)
- The `mistral:7b-instruct` model pulled in Ollama:

```bash
ollama pull mistral:7b-instruct
```

---

## 🚀 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/EdileneSilva/Agent-Professional-career-assistant.git
cd Agent-Professional-career-assistant
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

Create a `.env` file at the root of the project:

```env
MISTRALAI_API_KEY=your_api_key_here
```

4. **Add your resume:**

Place your PDF resume in the `data/` folder named `EDILENECV.pdf`.  
> ⚠️ On the first run, the vector store will be created automatically in `data/db/`.

---

## ▶️ Usage

Run the main agent with a job offer URL:

```bash
python career_agent.py
```

By default, the script uses the URL set in the `url_offre` variable inside the `__main__` block. To analyze a different offer, edit it directly in the code:

```python
url_offre = "https://www.welcometothejungle.com/fr/..."
```

### Example Output

```
Match score: 78%

Strengths:
Python, Machine Learning, SQL, Communication, Teamwork

Areas to improve:
Power BI, GDPR compliance, Advanced database management

---
[Automatically generated cover letter]
```

---

## 🔧 Sub-agents in Detail

### `retrieve-agent`
Uses **RAG (Retrieval-Augmented Generation)** to search for relevant information from the indexed resume in ChromaDB. Retrieves up to 5 chunks per query using semantic similarity.

### `offer-agent`
Scrapes the content of a job offer from the provided URL using LangChain's `WebBaseLoader`.

### `match-agent`
Compares the skills extracted from the resume against the job offer requirements and calculates a **match score** (0–100%), identifying strengths and skill gaps.

### `writer-agent`
Using the resume information, job offer content, and match analysis, writes a **professional cover letter** in French — structured, relevant, and tailored to the position.

---

## 📝 Notes

- `career_agent_rate_limit_safe.py` contains an alternative version with protections against MistralAI API rate limits.
- The `data/db/` folder is created automatically on the first run and reused on subsequent runs to avoid reprocessing the resume.
- The LLM can be switched to the MistralAI cloud API by uncommenting the corresponding line in `career_agent.py`.

---

## 👩‍💻 Author

**Edilene Silva**  
Developer in training — AI Data Dev specialization  
[GitHub](https://github.com/EdileneSilva)
