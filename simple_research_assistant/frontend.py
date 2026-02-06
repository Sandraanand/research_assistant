"""
Simplified Streamlit Frontend
Clean and user-friendly interface
"""
import streamlit as st
import requests
from config import config

# API URL
API_URL = f"http://localhost:{config.BACKEND_PORT}"

# Page config
st.set_page_config(
    page_title="Research Assistant",
    page_icon="🔬",
    layout="wide"
)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None


def call_api(endpoint: str, data: dict):
    """Call backend API"""
    try:
        response = requests.post(f"{API_URL}{endpoint}", json=data, timeout=300)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None


# ==================== Main App ====================

st.title("🔬 Research Assistant")
st.markdown("### AI-Powered Research Tool with GPT-4o")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Select Page",
        ["🏠 Home", "📚 Research", "💡 Explain Concept", "📝 Submit Paper", "🔍 Check Status"]
    )
    
    st.markdown("---")
    st.info("**Powered by:**\n- Autogen 0.4\n- Selector GroupChat\n- Azure OpenAI GPT-4o")


# ==================== Home Page ====================

if page == "🏠 Home":
    st.header("Welcome!")
    
    st.markdown("""
    This research assistant uses **Autogen 0.4 Selector GroupChat** to coordinate multiple AI agents:
    
    ### 🤖 Agents
    
    1. **Literature Agent** - Searches PubMed for papers
    2. **Synthesis Agent** - Summarizes research papers
    3. **Extensions Agent** - Proposes future research directions
    4. **Explainer Agent** - Explains concepts simply
    5. **Advisor Agent** - Checks paper formatting
    
    ### 🚀 Quick Start
    
    1. **Research**: Enter a topic to find and analyze papers
    2. **Explain**: Get simple explanations of complex concepts
    3. **Submit**: Check your paper and submit it
    4. **Track**: Check submission status anytime
    
    All agents are coordinated automatically by Selector GroupChat!
    """)


# ==================== Research Page ====================

elif page == "📚 Research":
    st.header("Research Workflow")
    
    topic = st.text_input("Research Topic", placeholder="e.g., Machine learning in healthcare")
    max_papers = st.slider("Max Papers", 1, 10, 5)
    
    if st.button("🚀 Start Research", type="primary"):
        if topic:
            with st.spinner("Running research workflow... This may take a few minutes..."):
                results = call_api("/api/research", {
                    "topic": topic,
                    "max_papers": max_papers
                })
                
                if results:
                    st.session_state.results = results
                    st.success("✅ Research completed!")
        else:
            st.error("Please enter a research topic")
    
    # Display results
    if st.session_state.results:
        results = st.session_state.results
        
        st.markdown("---")
        
        # Literature
        with st.expander("📚 Literature Search Results", expanded=True):
            st.markdown(results.get("literature", "No results"))
        
        # Synthesis
        with st.expander("📖 Paper Summaries", expanded=True):
            st.markdown(results.get("synthesis", "No summaries"))
        
        # Extensions
        with st.expander("🔮 Future Research Extensions", expanded=True):
            st.markdown(results.get("extensions", "No extensions"))


# ==================== Explain Concept Page ====================

elif page == "💡 Explain Concept":
    st.header("Concept Explainer")
    
    concept = st.text_input("Concept to Explain", placeholder="e.g., Neural Networks")
    context = st.text_area("Optional Context", placeholder="Add context from your research...")
    
    if st.button("💡 Explain", type="primary"):
        if concept:
            with st.spinner("Generating explanation..."):
                result = call_api("/api/explain", {
                    "concept": concept,
                    "context": context if context else None
                })
                
                if result:
                    st.markdown("### Explanation")
                    st.info(result.get("explanation", ""))
        else:
            st.error("Please enter a concept")


# ==================== Submit Paper Page ====================

elif page == "📝 Submit Paper":
    st.header("Paper Submission")
    
    tab1, tab2 = st.tabs(["Check Formatting", "Submit Paper"])
    
    with tab1:
        st.subheader("Check Paper Formatting")
        
        title = st.text_input("Paper Title")
        content = st.text_area("Paper Content", height=300)
        
        if st.button("📝 Check Formatting"):
            if title and content:
                with st.spinner("Checking formatting..."):
                    result = call_api("/api/check-paper", {
                        "title": title,
                        "content": content
                    })
                    
                    if result:
                        st.markdown("### Feedback")
                        st.info(result.get("feedback", ""))
            else:
                st.error("Please provide title and content")
    
    with tab2:
        st.subheader("Submit Paper")
        
        title = st.text_input("Title", key="submit_title")
        authors = st.text_input("Authors (comma-separated)", placeholder="Dr. Smith, Dr. Jones")
        content = st.text_area("Full Paper Content", height=300, key="submit_content")
        professor_email = st.text_input("Professor Email", placeholder="professor@university.edu")
        
        if st.button("📤 Submit Paper", type="primary"):
            if all([title, authors, content, professor_email]):
                with st.spinner("Submitting paper..."):
                    result = call_api("/api/submit-paper", {
                        "title": title,
                        "authors": [a.strip() for a in authors.split(",")],
                        "content": content,
                        "professor_email": professor_email
                    })
                    
                    if result:
                        st.success(f"✅ {result.get('message')}")
                        st.info(f"**Submission ID:** `{result.get('submission_id')}`\n\nSave this ID to check status later!")
            else:
                st.error("Please fill all fields")


# ==================== Check Status Page ====================

elif page == "🔍 Check Status":
    st.header("Check Submission Status")
    
    submission_id = st.text_input("Submission ID", placeholder="SUB-XXXXXXXX")
    
    if st.button("🔍 Check Status"):
        if submission_id:
            try:
                response = requests.get(f"{API_URL}/api/submission/{submission_id}")
                response.raise_for_status()
                result = response.json()
                
                st.markdown("### Submission Details")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Status", result.get("status", "unknown").upper())
                    st.write(f"**Title:** {result.get('title')}")
                
                with col2:
                    st.write(f"**Submitted:** {result.get('submitted_at')}")
                
                if result.get("feedback"):
                    st.markdown("### Feedback")
                    st.info(result.get("feedback"))
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    st.error("❌ Submission not found")
                else:
                    st.error(f"Error: {str(e)}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please enter a submission ID")
