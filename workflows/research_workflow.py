"""
Simplified research workflow orchestration
"""
import logging
from typing import List, Dict, Any, Tuple

from agents.research_agent import ResearchAgent
from agents.drafting_agent import DraftingAgent

logger = logging.getLogger(__name__)

def run_research_workflow(query: str) -> Tuple[List[Dict[str, Any]], str]:
    """
    Run the complete research workflow for a query
    
    Args:
        query: The research question
        
    Returns:
        Tuple containing (research findings, drafted answer)
    """
    logger.info(f"Starting research workflow for query: {query}")
    
    try:
        # Initialize agents
        research_agent = ResearchAgent()
        drafting_agent = DraftingAgent()
        
        # Step 1: Research phase
        logger.info("Executing research step")
        findings = research_agent.research(query)
        logger.info(f"Research completed with {len(findings)} findings")
        
        # Step 2: Drafting phase
        logger.info("Executing drafting step")
        draft = drafting_agent.draft_answer(query, findings)
        logger.info("Draft completed successfully")
        
        return findings, draft
    except Exception as e:
        logger.error(f"Error in research workflow: {str(e)}")
        raise RuntimeError(f"Research workflow failed: {str(e)}")
