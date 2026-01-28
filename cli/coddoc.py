#!/usr/bin/env python3
"""
CodDoc AI CLI - Command-line interface for code analysis and documentation.
"""

import click
import requests
import json
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

console = Console()

# Default API URL
API_URL = os.getenv('CODDOC_API_URL', 'http://localhost:8000')
DEFAULT_PROVIDER = os.getenv('CODDOC_LLM_PROVIDER', 'gemini')


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """CodDoc AI - AI-Powered Code Review & Documentation Assistant"""
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--language', '-l', help='Programming language (auto-detected if not specified)')
@click.option('--provider', '-p', default=DEFAULT_PROVIDER, help='LLM provider (gemini, openai, anthropic)')
@click.option('--output', '-o', type=click.Path(), help='Save results to file')
def analyze(path, language, provider, output):
    """Analyze code file and get AI-powered review."""
    
    # Read code file
    try:
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        return

    # Auto-detect language if not specified
    if not language:
        ext = Path(path).suffix.lstrip('.')
        language_map = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'java': 'java',
            'go': 'go',
            'rs': 'rust',
            'cpp': 'cpp',
            'cs': 'csharp',
            'rb': 'ruby',
            'php': 'php'
        }
        language = language_map.get(ext, 'python')

    console.print(f"[cyan]Analyzing {path} ({language})...[/cyan]")

    # Make API request
    try:
        response = requests.post(
            f"{API_URL}/api/analyze",
            json={
                "code": code,
                "language": language,
                "filename": os.path.basename(path),
                "llm_provider": provider
            },
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"[red]API Error: {e}[/red]")
        return

    # Display results
    analysis = result['analysis']
    
    # Quality Score
    score = analysis['quality_score']
    score_color = 'green' if score >= 8 else 'yellow' if score >= 6 else 'red'
    console.print(Panel(
        f"[bold {score_color}]Quality Score: {score}/10[/bold {score_color}]",
        title="Code Review Results",
        border_style=score_color
    ))

    # Summary
    console.print("\n[bold]Summary:[/bold]")
    console.print(analysis['summary'])

    # Security Concerns
    if analysis.get('security_concerns'):
        console.print("\n[bold red]🔒 Security Concerns:[/bold red]")
        for concern in analysis['security_concerns']:
            console.print(Panel(
                f"[bold]{concern['title']}[/bold]\n"
                f"{concern['description']}\n\n"
                f"[cyan]Recommendation:[/cyan] {concern['recommendation']}",
                border_style=concern['severity']
            ))

    # Issues
    if analysis.get('issues'):
        console.print("\n[bold yellow]⚠️  Issues Found:[/bold yellow]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Severity", style="dim")
        table.add_column("Category")
        table.add_column("Description")
        table.add_column("Line")
        
        for issue in analysis['issues']:
            table.add_row(
                issue['severity'],
                issue['category'],
                issue['description'][:50] + "..." if len(issue['description']) > 50 else issue['description'],
                str(issue.get('line_number', '-'))
            )
        console.print(table)

    # Suggestions
    if analysis.get('suggestions'):
        console.print("\n[bold green]💡 Suggestions:[/bold green]")
        for i, suggestion in enumerate(analysis['suggestions'], 1):
            console.print(f"\n{i}. [bold]{suggestion['title']}[/bold] ({suggestion['priority']} priority)")
            console.print(f"   {suggestion['description']}")

    # Save to file if requested
    if output:
        try:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            console.print(f"\n[green]✓ Results saved to {output}[/green]")
        except Exception as e:
            console.print(f"\n[red]Error saving results: {e}[/red]")


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--language', '-l', help='Programming language (auto-detected if not specified)')
@click.option('--style', '-s', default='google', help='Documentation style (google, numpy, sphinx, jsdoc, javadoc)')
@click.option('--provider', '-p', default=DEFAULT_PROVIDER, help='LLM provider')
@click.option('--output', '-o', type=click.Path(), help='Save documentation to file')
def document(path, language, style, provider, output):
    """Generate documentation for code file."""
    
    # Read code file
    try:
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        return

    # Auto-detect language
    if not language:
        ext = Path(path).suffix.lstrip('.')
        language_map = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'java': 'java',
            'go': 'go',
        }
        language = language_map.get(ext, 'python')

    console.print(f"[cyan]Generating documentation for {path} ({language})...[/cyan]")

    # Make API request
    try:
        response = requests.post(
            f"{API_URL}/api/document",
            json={
                "code": code,
                "language": language,
                "filename": os.path.basename(path),
                "doc_style": style,
                "llm_provider": provider
            },
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"[red]API Error: {e}[/red]")
        return

    # Display documentation
    doc = result['documentation']
    
    console.print(Panel(
        doc['overview'],
        title="📖 Overview",
        border_style="cyan"
    ))

    # Functions
    if doc.get('functions'):
        console.print("\n[bold]⚡ Functions:[/bold]")
        for func in doc['functions']:
            console.print(f"\n[bold cyan]{func['name']}()[/bold cyan]")
            console.print(f"  {func['description']}")
            
            if func.get('parameters'):
                console.print("\n  Parameters:")
                for param in func['parameters']:
                    console.print(f"    • {param['name']} ({param['type']}): {param['description']}")
            
            if func.get('returns'):
                console.print(f"\n  Returns: {func['returns']['type']} - {func['returns']['description']}")

    # Classes
    if doc.get('classes'):
        console.print("\n[bold]🏗️  Classes:[/bold]")
        for cls in doc['classes']:
            console.print(f"\n[bold magenta]{cls['name']}[/bold magenta]")
            console.print(f"  {cls['description']}")

    # Usage Examples
    if doc.get('usage_examples'):
        console.print("\n[bold]💻 Usage Examples:[/bold]")
        for example in doc['usage_examples']:
            syntax = Syntax(example, language, theme="monokai", line_numbers=True)
            console.print(syntax)

    # Save to file if requested
    if output:
        try:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            console.print(f"\n[green]✓ Documentation saved to {output}[/green]")
        except Exception as e:
            console.print(f"\n[red]Error saving documentation: {e}[/red]")


@cli.command()
@click.option('--page', '-p', default=1, help='Page number')
@click.option('--limit', '-l', default=10, help='Items per page')
def history(page, limit):
    """View review history."""
    
    console.print(f"[cyan]Fetching review history (page {page})...[/cyan]")

    try:
        response = requests.get(
            f"{API_URL}/api/reviews",
            params={"page": page, "limit": limit}
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"[red]API Error: {e}[/red]")
        return

    if not data['reviews']:
        console.print("[yellow]No reviews found[/yellow]")
        return

    # Display reviews
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Language")
    table.add_column("Quality Score")
    table.add_column("Date")
    table.add_column("Filename")

    for review in data['reviews']:
        score = review.get('quality_score', 0)
        score_color = 'green' if score >= 8 else 'yellow' if score >= 6 else 'red'
        table.add_row(
            review['review_id'][:8],
            review['language'],
            f"[{score_color}]{score:.1f}/10[/{score_color}]",
            review['created_at'][:19],
            review.get('filename', '-')
        )

    console.print(table)
    console.print(f"\nPage {data['pagination']['page']} of {data['pagination']['pages']}")


@cli.command()
def config():
    """Show current configuration."""
    
    console.print(Panel(
        f"[bold]API URL:[/bold] {API_URL}\n"
        f"[bold]Default LLM Provider:[/bold] {DEFAULT_PROVIDER}",
        title="CodDoc AI Configuration",
        border_style="cyan"
    ))
    
    console.print("\n[dim]To change configuration, set environment variables:[/dim]")
    console.print("  CODDOC_API_URL - API endpoint URL")
    console.print("  CODDOC_LLM_PROVIDER - Default LLM provider")


if __name__ == '__main__':
    cli()
