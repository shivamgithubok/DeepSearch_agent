"""
Command-line interface for the Deep Research AI Agent System
"""
import os
import sys
import logging
import argparse
import json
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

from workflows.research_workflow import run_research_workflow
from utils.file_utils import save_research_results, save_draft
import config

# Set up rich console
console = Console()
logger = logging.getLogger(__name__)

def display_welcome_message():
    """Display a welcome message to the user"""
    console.print(Panel.fit(
        "[bold blue]Deep Research AI Agent System[/bold blue]\n"
        "A multi-agent system for comprehensive research and answer drafting",
        title="Welcome",
        border_style="blue"
    ))

def get_user_query():
    """Get the research query from the user"""
    console.print("\n[bold cyan]Enter your research query:[/bold cyan]")
    query = console.input("> ")
    return query

def display_results(research_results, draft, query, research_file=None, draft_file=None):
    """Display the research results and draft to the user"""
    # Display research results
    console.print("\n[bold green]Research Results:[/bold green]")
    for i, result in enumerate(research_results, 1):
        console.print(f"[bold]{i}.[/bold] {result['title']}")
        console.print(f"[dim]{result['content'][:200]}...[/dim]")
        console.print(f"[blue]Source:[/blue] {result['source_url']}")
        console.print()
    
    # Display draft
    console.print("\n[bold green]Drafted Answer:[/bold green]")
    console.print(Panel(Markdown(draft), border_style="green"))
    
    # Display saved file paths
    if research_file:
        console.print(f"\n[dim]Research results saved to: {research_file}[/dim]")
    if draft_file:
        console.print(f"[dim]Draft saved to: {draft_file}[/dim]")

def run_cli():
    """Run the command-line interface"""
    parser = argparse.ArgumentParser(description="Deep Research AI Agent System")
    parser.add_argument("--query", type=str, help="Research query to process")
    parser.add_argument("--save", action="store_true", help="Save research results and draft")
    args = parser.parse_args()
    
    display_welcome_message()
    
    # Get query from command line args or prompt
    query = args.query if args.query else get_user_query()
    
    if not query:
        console.print("[bold red]No query provided. Exiting.[/bold red]")
        sys.exit(1)
    
    # Run the research workflow with progress indication
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}[/bold blue]"),
        console=console
    ) as progress:
        task = progress.add_task("[blue]Running research workflow...", total=None)
        
        try:
            research_results, draft = run_research_workflow(query)
            progress.update(task, completed=True, description="[green]Research completed!")
        except Exception as e:
            progress.update(task, completed=True, description="[red]Research failed!")
            console.print(f"\n[bold red]Error running research workflow:[/bold red] {str(e)}")
            logger.exception("Error in research workflow")
            sys.exit(1)
    
    # Save results if requested
    research_file = None
    draft_file = None
    if args.save:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        research_file = save_research_results(research_results, query, timestamp)
        draft_file = save_draft(draft, query, timestamp)
    
    # Display results
    display_results(research_results, draft, query, research_file, draft_file)

if __name__ == "__main__":
    run_cli()
