"""
Research Agent for gathering information from the web
"""
import logging
from typing import List, Dict, Any
import json
import os

from langchain_google_genai import ChatGoogleGenerativeAI

from utils.tavily_tools import search_tavily
import config
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()
logger = logging.getLogger(__name__)

class ResearchAgent:
    """
    Agent responsible for gathering information from the web
    using Tavily and other search tools.
    """
    
    def __init__(self):
        """Initialize the research agent with appropriate tools and LLM"""
        # Initialize the LLM with Google Gemini
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-Flash",
            temperature=0.2,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
        
        # Initialize tools - using a custom web search tool
        self.tools = [
            {
                "name": "web_search",
                "description": "Search the web for information on a specific topic or query.",
                "func": search_tavily
            }
        ]
        
        # Create the agent
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create a simplified research agent that calls the search tool"""
        return self.llm
    
    def research(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform research on the given query
        
        Args:
            query: The research question or topic
            
        Returns:
            List of research findings with source information
        """
        logger.info(f"Starting research on query: {query}")
        
        try:
            # First, search for information using Tavily
            search_results = search_tavily(query)
            
            # Process the search results
            try:
                results_dict = json.loads(search_results)
                
                # Format results for the LLM
                context = "Search results:\n\n"
                for i, result in enumerate(results_dict.get("results", [])):
                    context += f"Result {i+1}:\n"
                    context += f"Title: {result.get('title', 'No title')}\n"
                    context += f"URL: {result.get('url', 'No URL')}\n"
                    context += f"Content: {result.get('content', 'No content')}\n\n"
                
                # Now ask the LLM to synthesize the findings
                prompt = f"""
                You are a research expert. Based on the following search results about "{query}", 
                create a comprehensive list of key findings. Format your response as a JSON object with an array
                of 'findings', where each finding has the following structure:
                
                {{
                    "content": "The detailed information and explanation of the finding",
                    "source_url": "The URL where this information was found",
                    "source_title": "The title of the source page"
                }}
                
                Here are the search results:
                
                {context}
                
                Your response should ONLY be a valid JSON object with the 'findings' array.
                """
                
                response = self.llm.invoke(prompt)
                
                # Extract the text content from the response
                response_text = response.content
                
                # Try to parse JSON from the response
                findings = []
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}')
                
                if start_idx != -1 and end_idx != -1:
                    json_str = response_text[start_idx:end_idx+1]
                    results_dict = json.loads(json_str)
                    findings = results_dict.get('findings', [])
                
                # If no findings were parsed, attempt to parse the whole response
                if not findings:
                    try:
                        results_dict = json.loads(response_text)
                        findings = results_dict.get('findings', [])
                    except:
                        pass
                
                # If we still don't have findings, create them from the raw search results
                if not findings:
                    findings = []
                    for result in results_dict.get("results", []):
                        findings.append({
                            "title": result.get("title", "Search Result"),
                            "content": result.get("content", "No content available"),
                            "source_url": result.get("url", ""),
                            "source_title": result.get("title", "Search Result")
                        })
                
                # Ensure all findings have required fields
                for finding in findings:
                    if "title" not in finding:
                        finding["title"] = "Research Finding"
                    if "source_url" not in finding and "source" in finding:
                        finding["source_url"] = finding["source"]
                    if "source_title" not in finding:
                        finding["source_title"] = finding.get("title", "Research Source")
                
                logger.info(f"Research completed with {len(findings)} findings")
                return findings
                
            except Exception as e:
                logger.warning(f"Failed to parse search results: {str(e)}")
                # Fallback to raw search results
                results = []
                try:
                    results_dict = json.loads(search_results)
                    for result in results_dict.get("results", []):
                        results.append({
                            "title": result.get("title", "Search Result"),
                            "content": result.get("content", "No content available"),
                            "source_url": result.get("url", ""),
                            "source_title": result.get("title", "Search Result")
                        })
                except:
                    results = [{
                        "title": "Research Results",
                        "content": search_results,
                        "source_url": "",
                        "source_title": "Search Results"
                    }]
                return results
                
        except Exception as e:
            logger.error(f"Error during research: {str(e)}")
            raise RuntimeError(f"Research failed: {str(e)}")
