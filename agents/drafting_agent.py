"""
Drafting Agent for synthesizing research into coherent answers
"""
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
import os
# Load environment variables from .env file if present
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI

import config

logger = logging.getLogger(__name__)

class DraftingAgent:
    """
    Agent responsible for synthesizing research findings
    into a coherent, well-structured answer.
    """
    
    def __init__(self):
        """Initialize the drafting agent with appropriate LLM"""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=config.DEFAULT_TEMPERATURE,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
        self.prompt = self._get_prompt()
        
    def _get_prompt(self) -> str:
        """Create prompt template for the drafting agent"""
        prompt = """You are an expert drafting agent that synthesizes research findings into comprehensive, well-structured answers.
Your task is to analyze the provided research findings and create a coherent answer to the original query.
The answer should:
1. Be well-organized with clear sections and headers
2. Synthesize information from multiple sources
3. Cite sources appropriately
4. Prioritize factual accuracy
5. Be comprehensive yet concise
6. Use Markdown formatting for better readability

Focus on creating a high-quality answer that directly addresses the original query using only the provided research findings.

Original Query: {query}

Research Findings:
{findings}

Please draft a comprehensive answer based on these findings. Use markdown formatting for better readability."""

        return prompt
    
    def draft_answer(self, query: str, findings: List[Dict[str, Any]]) -> str:
        """
        Draft a comprehensive answer based on research findings
        
        Args:
            query: The original research question
            findings: List of research findings with source information
            
        Returns:
            A comprehensive answer in markdown format
        """
        logger.info(f"Drafting answer for query: {query}")
        
        try:
            # Format findings for the prompt
            findings_text = ""
            for i, finding in enumerate(findings, 1):
                findings_text += f"Finding {i}:\n"
                findings_text += f"Title: {finding.get('title', 'Untitled')}\n"
                findings_text += f"Content: {finding.get('content', '')}\n"
                findings_text += f"Source URL: {finding.get('source_url', '')}\n"
                findings_text += f"Source Title: {finding.get('source_title', 'Unknown')}\n\n"
            
            # Invoke the LLM
            response = self.llm.invoke(
                self.prompt.format(
                    query=query,
                    findings=findings_text
                )
            )
            
            # Extract the answer content
            answer = response.content
            
            logger.info("Successfully drafted answer")
            return answer
            
        except Exception as e:
            logger.error(f"Error during drafting: {str(e)}")
            raise RuntimeError(f"Drafting failed: {str(e)}")
