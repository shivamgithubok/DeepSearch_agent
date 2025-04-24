"""
File utility functions for saving and loading research results
"""
import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

import config

logger = logging.getLogger(__name__)

def save_research_results(results: List[Dict[str, Any]], query: str, timestamp: Optional[str] = None) -> str:
    """
    Save research results to a JSON file
    
    Args:
        results: List of research findings
        query: The original query
        timestamp: Optional timestamp string (defaults to current time)
        
    Returns:
        Path to the saved file
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a safe filename from the query
    safe_query = "".join([c if c.isalnum() else "_" for c in query])
    safe_query = safe_query[:50]  # Limit filename length
    
    # Create the filename
    filename = f"{safe_query}_{timestamp}.json"
    filepath = os.path.join(config.RESEARCH_RESULTS_DIR, filename)
    
    # Prepare data structure
    data = {
        "query": query,
        "timestamp": timestamp,
        "results": results
    }
    
    try:
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Research results saved to {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Error saving research results: {str(e)}")
        return ""

def save_draft(draft: str, query: str, timestamp: Optional[str] = None) -> str:
    """
    Save drafted answer to a markdown file
    
    Args:
        draft: The drafted answer text
        query: The original query
        timestamp: Optional timestamp string (defaults to current time)
        
    Returns:
        Path to the saved file
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a safe filename from the query
    safe_query = "".join([c if c.isalnum() else "_" for c in query])
    safe_query = safe_query[:50]  # Limit filename length
    
    # Create the filename
    filename = f"{safe_query}_{timestamp}.md"
    filepath = os.path.join(config.DRAFT_RESULTS_DIR, filename)
    
    try:
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {query}\n\n")
            f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write(draft)
        
        logger.info(f"Draft saved to {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Error saving draft: {str(e)}")
        return ""

def load_research_results(filepath: str) -> Dict[str, Any]:
    """
    Load research results from a JSON file
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Dictionary containing the loaded research data
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Research results loaded from {filepath}")
        return data
    except Exception as e:
        logger.error(f"Error loading research results: {str(e)}")
        return {"error": str(e), "query": "", "results": []}
