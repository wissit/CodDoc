# AI-Assisted System Development

This project was developed using an AI-assisted workflow, leveraging LLMs to accelerate development, ensure best practices, and implement complex features.

## Workflow Overview

1. **Planning & Architecture**:
   - Initial problem decomposition using AI.
   - Technology stack selection based on requirements.
   - Comprehensive implementation plan generation.

2. **Code Generation**:
   - **Backend**: Generated FastAPI routes, Pydantic models, and SQLAlchemy schemas.
   - **Frontend**: Created React components, Tailwind styles, and Next.js pages.
   - **Infrastructure**: Generated Dockerfiles, Docker Compose configuration, and CI/CD pipelines.

3. **MCP Integration**:
   - Used Model Context Protocol (MCP) to expose CodDoc AI tools to other agents.
   - Implemented `analyze_code` and `generate_documentation` as MCP tools.

## MCP Usage

The project includes a custom MCP server (`mcp-server/`) that exposes the core functionality of CodDoc AI as tools that can be consumed by other AI assistants (like Claude Desktop or other MCP clients).

### Available Tools

- `analyze_code`: Analyzes code snippet and returns quality score and issues.
- `generate_documentation`: Generates documentation for provided code.

### Available Resources

- `coddoc://history/recent`: Provides access to recent code reviews performed by the system.

## AI Models Used

The system is designed to be model-agnostic but defaults to **Google Gemini** for:
- Cost efficiency
- High context window
- Strong code analysis capabilities

It also supports **OpenAI GPT-4** and **Anthropic Claude** via a flexible `LLMProvider` abstraction.
