from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional, List
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = os.getenv("CODDOC_API_URL", "http://localhost:8000")

# Initialize MCP server
mcp = FastMCP("CodDoc AI")


class AnalyzeParams(BaseModel):
    code: str = Field(..., description="The code to analyze")
    language: str = Field(..., description="Programming language")
    filename: Optional[str] = Field(None, description="Optional filename")


class DocumentParams(BaseModel):
    code: str = Field(..., description="The code to document")
    language: str = Field(..., description="Programming language")
    style: Optional[str] = Field("google", description="Documentation style (google, numpy, sphinx, etc.)")


@mcp.tool()
async def analyze_code(params: AnalyzeParams) -> str:
    """
    Analyze code quality and security using CodDoc AI.
    Returns a textual summary of issues and suggestions.
    """
    try:
        response = requests.post(
            f"{API_URL}/api/analyze",
            json={
                "code": params.code,
                "language": params.language,
                "filename": params.filename,
                "llm_provider": "gemini"
            }
        )
        response.raise_for_status()
        data = response.json()
        
        analysis = data.get("analysis", {})
        summary = analysis.get("summary", "No summary provided.")
        quality_score = analysis.get("quality_score", 0)
        
        issues_count = len(analysis.get("issues", []))
        security_count = len(analysis.get("security_concerns", []))
        
        result = f"""
# Code Analysis Result

**Quality Score:** {quality_score}/10
**Summary:** {summary}

**Issues Found:** {issues_count}
**Security Concerns:** {security_count}

Use detailed view in CodDoc UI for full report.
"""
        return result
    except Exception as e:
        return f"Error analyzing code: {str(e)}"


@mcp.tool()
async def generate_documentation(params: DocumentParams) -> str:
    """
    Generate documentation for code using CodDoc AI.
    Returns the generated documentation content.
    """
    try:
        response = requests.post(
            f"{API_URL}/api/document",
            json={
                "code": params.code,
                "language": params.language,
                "doc_style": params.style,
                "llm_provider": "gemini"
            }
        )
        response.raise_for_status()
        data = response.json()
        
        doc = data.get("documentation", {})
        
        result = f"""
# Generated Documentation

**Overview:** {doc.get("overview", "")}

## Functions
"""
        for func in doc.get("functions", []):
            result += f"- `{func['name']}`: {func['description']}\n"
            
        return result
    except Exception as e:
        return f"Error generating documentation: {str(e)}"


@mcp.resource("coddoc://history/recent")
async def get_recent_reviews() -> str:
    """
    Get a list of recent code reviews.
    """
    try:
        response = requests.get(f"{API_URL}/api/reviews?limit=5")
        response.raise_for_status()
        data = response.json()
        
        result = "# Recent Code Reviews\n\n"
        for review in data.get("reviews", []):
            result += f"- **{review.get('filename', 'Unknown')}** ({review.get('language')}) - Quality: {review.get('quality_score', 'N/A')}/10 - {review.get('created_at')}\n"
            
        return result
    except Exception as e:
        return f"Error fetching history: {str(e)}"


if __name__ == "__main__":
    mcp.run()
