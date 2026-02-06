# Simple Research Assistant

A clean, simplified multi-agent research assistant using **Autogen 0.4** with **Selector GroupChat** and **Azure OpenAI GPT-4o**.

## ✨ Key Features

- ✅ **Autogen 0.4** with Selector GroupChat for agent coordination
- ✅ **Single Model** - Only GPT-4o, no fallbacks or complicated configs
- ✅ **5 Specialized Agents** coordinated automatically
- ✅ **Simple Codebase** - Easy to understand and modify
- ✅ **Persistent Storage** - SQLite database for submissions

## 🏗️ Architecture

```
User Request
     ↓
Selector GroupChat (Autogen 0.4)
     ↓
Automatically selects appropriate agent:
     ├── Literature Agent (PubMed search)
     ├── Synthesis Agent (Summarization)
     ├── Extensions Agent (Future research)
     ├── Explainer Agent (Simple explanations)
     └── Advisor Agent (Paper checking)
```

### How Selector GroupChat Works

```python
team = SelectorGroupChat(
    participants=[
        literature_agent,
        synthesis_agent,
        extensions_agent,
        explainer_agent,
        advisor_agent
    ],
    model_client=model_client,  # GPT-4o
    termination_condition=MaxMessageTermination(20)
)

# Selector automatically routes to the right agent!
result = await team.run_stream(task=user_message)
```

## 📁 Project Structure

```
simple_research_assistant/
├── config.py              # Configuration (Azure OpenAI)
├── database.py            # SQLAlchemy models
├── orchestrator.py        # Selector GroupChat + Agents
├── backend.py             # FastAPI server
├── frontend.py            # Streamlit UI
├── requirements.txt       # Dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your Azure OpenAI credentials:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

### 3. Start Backend

```bash
python backend.py
```

Backend runs on: `http://localhost:8000`

### 4. Start Frontend

In a new terminal:

```bash
streamlit run frontend.py
```

Frontend opens at: `http://localhost:8501`

## 🎯 Usage

### Research Workflow

1. Navigate to "Research" page
2. Enter a research topic
3. Select max papers (1-10)
4. Click "Start Research"

The workflow automatically:
- Searches PubMed for papers
- Synthesizes findings
- Proposes research extensions

### Explain Concepts

1. Go to "Explain Concept"
2. Enter a concept (e.g., "Neural Networks")
3. Optionally add context
4. Get simple explanation with examples

### Submit Papers

1. Go to "Submit Paper"
2. Check formatting first (optional)
3. Fill in all fields
4. Submit to professor (stored in database)
5. Save your submission ID

### Check Status

1. Go to "Check Status"
2. Enter your submission ID
3. View current status and feedback

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/research` | POST | Run research workflow |
| `/api/explain` | POST | Explain a concept |
| `/api/check-paper` | POST | Check paper formatting |
| `/api/submit-paper` | POST | Submit paper |
| `/api/submission/{id}` | GET | Check submission status |

## 💡 Key Differences from Complex Version

### Simplified:
- ✅ Only Autogen 0.4 (not 0.2)
- ✅ Only GPT-4o (no fallback models)
- ✅ Direct Selector GroupChat (no manual routing)
- ✅ Single file per component
- ✅ No complicated agent hierarchies
- ✅ Cleaner async/await handling

### Removed Complexity:
- ❌ No fallback LLM configurations
- ❌ No manual agent routing logic
- ❌ No complex state management
- ❌ No multiple configuration layers
- ❌ No unnecessary abstractions

## 📚 How It Works

### Selector GroupChat Flow

```python
# User asks about research topic
task = "Find papers on machine learning"

# Selector GroupChat automatically:
# 1. Analyzes the request
# 2. Selects Literature Agent
# 3. Agent searches PubMed
# 4. Returns results

# Next step automatically triggered:
# 5. Selector chooses Synthesis Agent
# 6. Agent summarizes papers
# 7. Returns summaries

# And so on...
```

### Agent Structure

Each agent is simply:

```python
agent = AssistantAgent(
    name="agent_name",
    model_client=gpt4o_client,  # Single model!
    system_message="What this agent does..."
)
```

No complicated configs, no fallbacks, just clean and simple.

## 🎓 Example Usage

### Python API Example

```python
import requests

# Start research
response = requests.post("http://localhost:8000/api/research", json={
    "topic": "deep learning in healthcare",
    "max_papers": 5
})

results = response.json()
print(results["literature"])
print(results["synthesis"])
print(results["extensions"])
```

### Submit Paper Example

```python
response = requests.post("http://localhost:8000/api/submit-paper", json={
    "title": "My Research Paper",
    "authors": ["Dr. Smith", "Dr. Jones"],
    "content": "Full paper content...",
    "professor_email": "prof@university.edu"
})

submission_id = response.json()["submission_id"]
print(f"Submission ID: {submission_id}")

# Check status later
status = requests.get(f"http://localhost:8000/api/submission/{submission_id}")
print(status.json())
```

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Invalid API key"
Check your `.env` file has correct Azure OpenAI credentials

### "Database locked"
Close other connections, restart backend

### Agents not responding
Check Azure OpenAI quota and deployment name matches `.env`

## 📝 Requirements

- Python 3.9+
- Azure OpenAI account with GPT-4o deployment
- Internet connection (for PubMed search)

## 🔐 Environment Variables

Required:
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_DEPLOYMENT` (defaults to "gpt-4o")

Optional:
- `BACKEND_PORT` (default: 8000)
- `FRONTEND_PORT` (default: 8501)
- `PUBMED_EMAIL` (recommended for PubMed)
- `DATABASE_URL` (default: sqlite:///./research.db)

## 🎯 Key Advantages

1. **Simple**: One model, one configuration, easy to understand
2. **Automatic**: Selector GroupChat handles agent coordination
3. **Modern**: Uses Autogen 0.4 (latest version)
4. **Fast**: No fallback attempts, direct GPT-4o calls
5. **Clean**: Minimal code, maximum functionality

## 📖 Documentation

- **Autogen 0.4**: https://microsoft.github.io/autogen/
- **Selector GroupChat**: https://microsoft.github.io/autogen/docs/tutorial/teams
- **Azure OpenAI**: https://learn.microsoft.com/en-us/azure/ai-services/openai/

## 🤝 Contributing

This is a simplified reference implementation. Feel free to:
- Add more agents
- Customize agent behaviors
- Extend API endpoints
- Improve UI

## 📄 License

MIT License

## 🙏 Acknowledgments

- Microsoft Autogen team for the framework
- Azure OpenAI for GPT-4o
- Streamlit for the UI framework

---

**Simple. Clean. Powerful.**

Built with Autogen 0.4 Selector GroupChat + Azure OpenAI GPT-4o
