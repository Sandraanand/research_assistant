"""
Research Orchestrator using Autogen 0.4 with Selector GroupChat
Simple, clean implementation with only GPT-4o
"""
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from typing import Dict, Any, List
import asyncio
from config import config


class ResearchOrchestrator:
    """
    Simplified Research Orchestrator using Autogen 0.4 Selector GroupChat
    - Only GPT-4o model
    - No fallbacks or complicated routing
    - Clean agent coordination
    """
    
    def __init__(self):
        """Initialize orchestrator with all agents and selector group chat"""
        
        # Initialize Azure OpenAI client (single model, no fallbacks)
        self.model_client = AzureOpenAIChatCompletionClient(
            azure_deployment=config.AZURE_OPENAI_DEPLOYMENT,
            api_version=config.AZURE_OPENAI_API_VERSION,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_key=config.AZURE_OPENAI_API_KEY,
            model=config.AZURE_OPENAI_DEPLOYMENT
        )
        
        # Initialize all agents
        self.literature_agent = self._create_literature_agent()
        self.synthesis_agent = self._create_synthesis_agent()
        self.extensions_agent = self._create_extensions_agent()
        self.explainer_agent = self._create_explainer_agent()
        self.advisor_agent = self._create_advisor_agent()
        
        # Create Selector GroupChat
        self.team = SelectorGroupChat(
            participants=[
                self.literature_agent,
                self.synthesis_agent,
                self.extensions_agent,
                self.explainer_agent,
                self.advisor_agent
            ],
            model_client=self.model_client,
            termination_condition=MaxMessageTermination(max_messages=20)
        )
    
    def _create_literature_agent(self) -> AssistantAgent:
        """Create Literature Search Agent"""
        return AssistantAgent(
            name="literature_agent",
            model_client=self.model_client,
            system_message="""You are a Literature Search Agent. 
            
Your job:
1. Search PubMed for academic papers on the given topic
2. Extract: DOI, title, authors, abstract, link
3. Return structured results

Be focused and efficient. Only return relevant papers."""
        )
    
    def _create_synthesis_agent(self) -> AssistantAgent:
        """Create Reading Synthesis Agent"""
        return AssistantAgent(
            name="synthesis_agent",
            model_client=self.model_client,
            system_message="""You are a Reading Synthesis Agent.

Your job:
1. Read and analyze paper abstracts
2. Create concise summaries (2-3 sentences each)
3. Extract key findings
4. Format: "Paper 1: [summary], Paper 2: [summary], ..."

Be clear and concise."""
        )
    
    def _create_extensions_agent(self) -> AssistantAgent:
        """Create Future Research Extensions Agent"""
        return AssistantAgent(
            name="extensions_agent",
            model_client=self.model_client,
            system_message="""You are a Future Research Extensions Agent.

Your job:
1. Analyze paper summaries for gaps
2. Propose future research directions
3. Provide one-line solution approach for each
4. Assess difficulty (Easy/Medium/Hard)

Format each extension with:
- Title
- Description
- Solution approach (one line)
- Difficulty level"""
        )
    
    def _create_explainer_agent(self) -> AssistantAgent:
        """Create Concept Explainer Agent"""
        return AssistantAgent(
            name="explainer_agent",
            model_client=self.model_client,
            system_message="""You are a Concept Explainer Agent.

Your job:
1. Explain complex concepts in simple terms (ELI5)
2. Provide concrete examples
3. Use analogies people can relate to
4. Make research accessible

Be clear, friendly, and avoid jargon."""
        )
    
    def _create_advisor_agent(self) -> AssistantAgent:
        """Create Submission Advisor Agent"""
        return AssistantAgent(
            name="advisor_agent",
            model_client=self.model_client,
            system_message="""You are a Submission Advisor Agent.

Your job:
1. Check paper formatting
2. Validate structure (abstract, intro, methods, results, conclusion)
3. Provide formatting score (0-100)
4. Give improvement recommendations
5. Handle paper submission

Be thorough and constructive."""
        )
    
    async def run_research_workflow(self, topic: str, max_papers: int = 5) -> Dict[str, Any]:
        """
        Run complete research workflow using Selector GroupChat
        
        Args:
            topic: Research topic
            max_papers: Max papers to retrieve
            
        Returns:
            Complete workflow results
        """
        print(f"\n🔬 Starting research workflow for: {topic}\n")
        
        # Step 1: Literature Search
        print("📚 Step 1: Searching literature...")
        lit_prompt = f"""Search for academic papers on: "{topic}"
Find up to {max_papers} relevant papers.
Return DOI, title, authors, abstract, and link for each."""
        
        lit_result = await self.team.run_stream(
            task=TextMessage(content=lit_prompt, source="user")
        )
        
        literature_data = await self._collect_messages(lit_result)
        
        # Step 2: Synthesis
        print("\n📖 Step 2: Synthesizing papers...")
        syn_prompt = f"""Analyze and summarize these papers:
{literature_data}

Create concise summaries with key findings."""
        
        syn_result = await self.team.run_stream(
            task=TextMessage(content=syn_prompt, source="user")
        )
        
        synthesis_data = await self._collect_messages(syn_result)
        
        # Step 3: Research Extensions
        print("\n🔮 Step 3: Generating research extensions...")
        ext_prompt = f"""Based on these summaries:
{synthesis_data}

Propose 5 future research extensions with:
- Title
- Description  
- One-line solution approach
- Difficulty level"""
        
        ext_result = await self.team.run_stream(
            task=TextMessage(content=ext_prompt, source="user")
        )
        
        extensions_data = await self._collect_messages(ext_result)
        
        print("\n✅ Research workflow completed!\n")
        
        return {
            "topic": topic,
            "literature": literature_data,
            "synthesis": synthesis_data,
            "extensions": extensions_data,
            "status": "completed"
        }
    
    async def explain_concept(self, concept: str, context: str = None) -> str:
        """Explain a concept in simple terms"""
        print(f"\n💡 Explaining concept: {concept}\n")
        
        prompt = f"""Explain this concept in simple terms: {concept}"""
        if context:
            prompt += f"\n\nContext: {context}"
        
        prompt += "\n\nProvide: simple explanation, examples, analogies"
        
        result = await self.team.run_stream(
            task=TextMessage(content=prompt, source="user")
        )
        
        explanation = await self._collect_messages(result)
        
        print("\n✅ Explanation generated!\n")
        return explanation
    
    async def check_paper(self, title: str, content: str) -> Dict[str, Any]:
        """Check paper formatting"""
        print(f"\n📝 Checking paper: {title}\n")
        
        prompt = f"""Check this paper's formatting:

Title: {title}

Content:
{content[:2000]}...

Provide:
1. Formatting score (0-100)
2. Missing sections
3. Recommendations
4. Overall assessment"""
        
        result = await self.team.run_stream(
            task=TextMessage(content=prompt, source="user")
        )
        
        feedback = await self._collect_messages(result)
        
        print("\n✅ Formatting check completed!\n")
        return {"feedback": feedback}
    
    async def _collect_messages(self, stream) -> str:
        """Collect messages from async stream"""
        messages = []
        async for message in stream:
            if hasattr(message, 'content'):
                messages.append(str(message.content))
        return "\n".join(messages)


# Global instance
orchestrator = None


def get_orchestrator() -> ResearchOrchestrator:
    """Get or create orchestrator instance"""
    global orchestrator
    if orchestrator is None:
        orchestrator = ResearchOrchestrator()
    return orchestrator
