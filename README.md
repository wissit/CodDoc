# CodDoc AI - AI-Powered Code Review & Documentation Assistant

![CodDoc AI Banner](frontend/public/banner.png)

CodDoc AI is a comprehensive tool that automatically generates human-readable code explanations, suggests improvements, and creates documentation from your codebase using advanced Large Language Models (LLMs). It helps bridge the gap between complex code and team understanding.

## Features

- **🔍 AI Code Analysis**: Instant comprehensive code reviews with quality scores.
- **🛡️ Security Scanning**: Identifies vulnerabilities and provides recommendation fixes.
- **📚 Auto Documentation**: Generates professional documentation in multiple styles (Google, NumPy, etc.).
- **⚡ Multi-Model Support**: Powered by **Google Gemini** (default), OpenAI GPT-4, and Anthropic Claude.
- **💻 CLI Tool**: Powerful command-line interface for local workflows.
- **🌐 Web Interface**: Modern, responsive Next.js frontend with beautiful visualization.
- **🔌 MCP Server**: Model Context Protocol integration for AI agent interoperability.

## System Architecture

The system consists of several integrated components:

- **Backend**: Python FastAPI with SQLAlchemy and Pydantic.
- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, and React Query.
- **Database**: PostgreSQL (Production) / SQLite (Development).
- **CLI**: Python Click-based command-line tool.
- **MCP Server**: FastMCP implementation for AI tool exposure.

## Quick Start

### Prerequisites

- Docker and Docker Compose
- API Key (Google Gemini, OpenAI, or Anthropic)

### Running with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/coddoc.git
   cd coddoc
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. Start the services:
   ```bash
   docker-compose up -d
   ```

4. Access the application:
   - **Web UI**: http://localhost:3000
   - **API Docs**: http://localhost:8000/docs
   - **Database**: Postgres running on port 5432

### CLI Usage

Install the CLI tool:

```bash
cd cli
pip install -r requirements.txt
python coddoc.py --help
```

Analyze a file:
```bash
python coddoc.py analyze ./path/to/file.py
```

Generate documentation:
```bash
python coddoc.py document ./path/to/file.py --style google
```

## Development

See [docs/AI_DEVELOPMENT.md](docs/AI_DEVELOPMENT.md) for details on the AI-assisted development process and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design.

## License

MIT
