# Deep Research AI Agent System

A Python-based multi-agent research system using LangChain and LangGraph to gather web information and generate comprehensive answers.

## Overview

This system implements a multi-agent architecture for performing deep research on any given topic. It consists of:

1. **Research Agent**: Gathers information from the web using Tavily API
2. **Drafting Agent**: Synthesizes research into coherent, comprehensive answers
3. **LangGraph Workflow**: Orchestrates the interaction between agents

## Features

- Multi-agent system with specialized agents
- Web information gathering using Tavily API
- Research synthesis and answer drafting
- LangGraph-based workflow orchestration
- Command-line interface
- Result saving and loading
- Comprehensive error handling
- Detailed logging

## Requirements

- Python 3.9+
- LangChain
- LangGraph
- Google Generative AI (Gemini) Python client
- Rich (for enhanced CLI)

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install langchain langgraph langchain-google-genai rich python-dotenv requests
   ```
3. Set up environment variables:
   ```
   TAVILY_API_KEY=your_tavily_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

## Usage

Run the command-line interface:

```bash
python main.py
