"""
Tavily API integration tools
"""
import os
import logging
import requests
import json
from typing import Dict, Any, List, Optional

import config

logger = logging.getLogger(__name__)

def search_tavily(query: str, search_depth: str = "moderate", max_results: int = 5) -> str:
    """
    Search the web using Tavily API
    
    Args:
        query: The search query
        search_depth: The depth of the search (quick, moderate, comprehensive)
        max_results: Maximum number of results to return
        
    Returns:
        JSON string containing search results
    """
    logger.info(f"Searching Tavily for: {query}")
    
    # Validate parameters
    if search_depth not in ["quick", "moderate", "comprehensive"]:
        search_depth = "moderate"
    
    if max_results < 1 or max_results > 10:
        max_results = 5
    
    try:
        # Get API key from config
        api_key = config.TAVILY_API_KEY
        
        # Check if we're using a dummy key for development
        if api_key == "dummy_tavily_api_key":
            logger.warning("Using dummy Tavily API key. Returning mock results.")
            return _mock_tavily_results(query)
        
        # Prepare the API request
        url = "https://api.tavily.com/search"
        headers = {
            "content-type": "application/json",
            "x-api-key": api_key
        }
        payload = {
            "query": query,
            "search_depth": search_depth,
            "max_results": max_results,
            "include_domains": [],
            "exclude_domains": []
        }
        
        # Make the request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Process response
        results = response.json()
        
        # Format results as a string for the agent
        formatted_results = json.dumps(results, indent=2)
        
        logger.info(f"Tavily search returned {len(results.get('results', []))} results")
        return formatted_results
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Tavily API request failed: {str(e)}")
        error_message = f"Tavily search failed: {str(e)}"
        
        # If we're hitting rate limits or the API is down, use mock results as fallback
        if isinstance(e, requests.exceptions.HTTPError) and (e.response.status_code == 429 or e.response.status_code >= 500):
            logger.warning("Using mock results as fallback due to API error")
            return _mock_tavily_results(query)
        
        return json.dumps({"error": error_message, "results": []})
    except Exception as e:
        logger.exception(f"Unexpected error in Tavily search: {str(e)}")
        return json.dumps({"error": str(e), "results": []})

def _mock_tavily_results(query: str) -> str:
    """Generate mock Tavily results for development/testing"""
    mock_results = {
        "query": query,
        "results": [
            {
                "title": f"Information about {query}",
                "url": "https://example.com/article1",
                "content": f"This is some mock content about {query}. This is provided as a development placeholder when the Tavily API is not available.",
                "score": 0.95
            },
            {
                "title": f"{query} research and analysis",
                "url": "https://example.com/article2",
                "content": f"Here is a detailed analysis of {query}. This is mock content for development purposes only.",
                "score": 0.85
            },
            {
                "title": f"Understanding {query}: A comprehensive guide",
                "url": "https://example.com/guide",
                "content": f"A comprehensive guide to understanding {query} and its implications. This is mock content for development purposes.",
                "score": 0.75
            }
        ],
        "metadata": {
            "search_depth": "moderate",
            "max_results": 3,
            "search_id": "mock-search-id"
        }
    }
    
    return json.dumps(mock_results, indent=2)
