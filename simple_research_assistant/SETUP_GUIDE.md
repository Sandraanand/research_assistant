# Complete Setup & Usage Guide

## 🚀 Installation

### Step 1: Create Project Directory

```bash
mkdir simple_research_assistant
cd simple_research_assistant
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: If you get errors with autogen 0.4:

```bash
pip install autogen-agentchat==0.4.0
pip install autogen-ext[openai]==0.4.0
```

### Step 4: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your details:

```env
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

## ▶️ Running the Application

### Option 1: Two Terminals

**Terminal 1 - Backend:**
```bash
python backend.py
```

**Terminal 2 - Frontend:**
```bash
streamlit run frontend.py
```

### Option 2: Background Process

```bash
# Start backend in background
python backend.py &

# Start frontend
streamlit run frontend.py
```

## 🎯 Complete Usage Examples

### Example 1: Research Workflow

**Scenario**: Research machine learning in cancer diagnosis

1. Open frontend at `http://localhost:8501`
2. Navigate to "📚 Research"
3. Enter topic: "machine learning in cancer diagnosis"
4. Select max papers: 5
5. Click "🚀 Start Research"

**What Happens Behind the Scenes:**

```
User Request
     ↓
Selector GroupChat receives request
     ↓
Automatically selects Literature Agent
     ↓
Literature Agent searches PubMed → Returns 5 papers
     ↓
Selector GroupChat automatically continues
     ↓
Selects Synthesis Agent
     ↓
Synthesis Agent summarizes all papers → Returns summaries
     ↓
Selector GroupChat continues
     ↓
Selects Extensions Agent
     ↓
Extensions Agent proposes 5 future research directions
     ↓
Results displayed in frontend
```

**Expected Output:**

```
Literature Results:
- Paper 1: "Deep Learning for Breast Cancer Detection"
  Authors: Smith et al.
  DOI: 10.1234/example
  Link: https://pubmed.ncbi.nlm.nih.gov/12345/

- Paper 2: ...

Summaries:
Paper 1: This study uses CNNs for tumor detection achieving 95% accuracy. 
Key findings: Model outperforms radiologists, works on limited data.

Paper 2: ...

Research Extensions:
1. Multi-Cancer Detection System
   Description: Extend single-cancer models to detect multiple types
   Solution: Use transfer learning with EfficientNet architecture
   Difficulty: Hard

2. Real-time Clinical Integration
   ...
```

### Example 2: Explain a Concept

**Scenario**: Understand "Convolutional Neural Networks"

1. Navigate to "💡 Explain Concept"
2. Enter: "Convolutional Neural Networks"
3. Optional context: "Used in medical imaging"
4. Click "💡 Explain"

**Response:**

```
Simple Explanation:
A Convolutional Neural Network (CNN) is like a smart camera filter 
that learns to recognize patterns in images. Just like you learned 
to recognize your mom's face by seeing it many times, CNNs learn by 
looking at thousands of examples.

Examples:
1. Face recognition on your phone
2. Medical imaging to detect tumors
3. Self-driving cars recognizing pedestrians

Analogies:
- Like a detective examining clues layer by layer
- Similar to how your eyes process images (edges first, then details)

Related Concepts:
- Neural Networks
- Deep Learning
- Image Recognition
- Computer Vision
```

### Example 3: Submit a Paper

**Scenario**: Submit research paper to professor

1. Navigate to "📝 Submit Paper"
2. Click "Check Formatting" tab
3. Enter title: "Novel CNN Architecture for Cancer Detection"
4. Paste paper content
5. Click "📝 Check Formatting"

**Formatting Feedback:**

```
Formatting Score: 85/100

Sections Present:
✓ Abstract
✓ Introduction
✓ Methods
✓ Results
✓ References

Sections Missing:
✗ Discussion
✗ Conclusion

Recommendations:
- Add a Discussion section analyzing your results
- Include a Conclusion summarizing key findings
- Ensure references follow APA format

Overall: Paper needs minor revisions before submission
```

6. Make revisions
7. Go to "Submit Paper" tab
8. Fill in all details
9. Click "📤 Submit Paper"

**Submission Confirmation:**

```
✅ Paper successfully submitted to professor@university.edu

Submission ID: SUB-A7F3B9C1

Save this ID to check status later!
```

### Example 4: Check Submission Status

**Scenario**: Check if professor reviewed your paper

1. Navigate to "🔍 Check Status"
2. Enter: "SUB-A7F3B9C1"
3. Click "🔍 Check Status"

**Status Response:**

```
Submission Details

Status: UNDER_REVIEW

Title: Novel CNN Architecture for Cancer Detection
Submitted: 2024-02-05 10:00:00

Feedback:
Paper shows promise. Good methodology section. 
Please address the missing Discussion section and resubmit.
```

## 🔧 API Examples

### cURL Examples

**Research Workflow:**
```bash
curl -X POST http://localhost:8000/api/research \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "machine learning in healthcare",
    "max_papers": 5
  }'
```

**Explain Concept:**
```bash
curl -X POST http://localhost:8000/api/explain \
  -H "Content-Type: application/json" \
  -d '{
    "concept": "Neural Networks",
    "context": "Used in image recognition"
  }'
```

**Submit Paper:**
```bash
curl -X POST http://localhost:8000/api/submit-paper \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Research Paper",
    "authors": ["Dr. Smith", "Dr. Jones"],
    "content": "Full paper content...",
    "professor_email": "prof@university.edu"
  }'
```

**Check Status:**
```bash
curl http://localhost:8000/api/submission/SUB-A7F3B9C1
```

### Python Examples

```python
import requests

# Initialize
API = "http://localhost:8000"

# 1. Research Workflow
research_result = requests.post(f"{API}/api/research", json={
    "topic": "deep learning",
    "max_papers": 3
}).json()

print(research_result["literature"])

# 2. Explain Concept
explanation = requests.post(f"{API}/api/explain", json={
    "concept": "Backpropagation"
}).json()

print(explanation["explanation"])

# 3. Submit Paper
submission = requests.post(f"{API}/api/submit-paper", json={
    "title": "My Paper",
    "authors": ["Author 1"],
    "content": "Content...",
    "professor_email": "prof@email.com"
}).json()

submission_id = submission["submission_id"]

# 4. Check Status
status = requests.get(f"{API}/api/submission/{submission_id}").json()
print(f"Status: {status['status']}")
```

## 🎓 Understanding Selector GroupChat

### How It Works

Selector GroupChat is Autogen 0.4's automatic agent coordination system:

```python
# You create agents
literature_agent = AssistantAgent(name="literature", ...)
synthesis_agent = AssistantAgent(name="synthesis", ...)

# You create the team
team = SelectorGroupChat(
    participants=[literature_agent, synthesis_agent],
    model_client=gpt4o_client
)

# You give a task
result = await team.run_stream(task="Find papers on AI")

# Selector GroupChat automatically:
# 1. Analyzes the task
# 2. Selects the best agent (literature_agent)
# 3. Runs the agent
# 4. Gets the response
# 5. Decides if more agents needed
# 6. Continues until task complete
```

### Why It's Better

**Old Way (Manual Routing):**
```python
if "search" in user_message:
    result = literature_agent.run()
elif "summarize" in user_message:
    result = synthesis_agent.run()
# etc... lots of if/else
```

**New Way (Selector GroupChat):**
```python
result = await team.run_stream(task=user_message)
# Automatically routes to correct agent!
```

## 🐛 Common Issues

### Issue 1: Import Errors

```
ImportError: cannot import name 'SelectorGroupChat'
```

**Solution:**
```bash
pip install autogen-agentchat==0.4.0 --upgrade
```

### Issue 2: Azure OpenAI Errors

```
Error: Invalid API key
```

**Solution:**
1. Check `.env` file exists
2. Verify `AZURE_OPENAI_API_KEY` is correct
3. Ensure `AZURE_OPENAI_ENDPOINT` ends with `/`
4. Confirm deployment name matches Azure portal

### Issue 3: Database Locked

```
sqlite3.OperationalError: database is locked
```

**Solution:**
```bash
# Stop backend
# Delete database file
rm research.db

# Restart backend
python backend.py
```

### Issue 4: PubMed Search Fails

```
PubMed search error: 403 Forbidden
```

**Solution:**
Add email to `.env`:
```env
PUBMED_EMAIL=your-email@example.com
```

## 📊 Performance Tips

1. **Adjust Max Papers**: Start with 3-5 for faster results
2. **Use Specific Topics**: "deep learning in cancer" vs "AI"
3. **Cache Results**: Results are stored in database
4. **Monitor Tokens**: GPT-4o calls count toward quota

## 🔐 Security Notes

- Never commit `.env` file
- Rotate API keys regularly
- Use environment variables in production
- Implement rate limiting for API
- Add authentication for production deployment

## 📚 Additional Resources

- [Autogen 0.4 Documentation](https://microsoft.github.io/autogen/)
- [Selector GroupChat Guide](https://microsoft.github.io/autogen/docs/tutorial/teams)
- [Azure OpenAI Setup](https://learn.microsoft.com/azure/ai-services/openai/)
- [PubMed API Docs](https://www.ncbi.nlm.nih.gov/books/NBK25501/)

## ✅ Verification Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads at localhost:8501
- [ ] Research workflow completes
- [ ] Concept explanation works
- [ ] Paper submission creates database entry
- [ ] Status check retrieves submission
- [ ] All agents respond via Selector GroupChat

## 🎉 Success Indicators

You know it's working when:
1. Backend logs show "✅ Backend initialized"
2. Research workflow completes in 2-5 minutes
3. Agents are automatically selected (check logs)
4. Results display in frontend
5. Submission ID returned after paper submit
6. Status check works with submission ID

---

**You're all set! Enjoy your simplified research assistant!** 🚀
