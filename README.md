# CodexAssist — AI-Powered Software Engineering Assistant

CodexAssist is an AI-powered software engineering assistant developed as a Final Degree Project at Universidad Pontificia de Salamanca (UPSA) during the 2025–2026 academic year.

The platform helps developers understand and navigate codebases by combining Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG). It retrieves relevant source code from a project and uses that context to generate answers to technical questions, helping developers explore unfamiliar codebases more efficiently.

## Key Features

- Codebase ingestion and source file processing
- Semantic search over code using vector embeddings
- Retrieval-Augmented Generation (RAG) for repository-specific questions
- Context-aware responses grounded in retrieved source code
- Conversational interface for technical queries
- Modular architecture separating ingestion, retrieval, and response generation
- Configurable model and retrieval settings
- Environment-based configuration for credentials
- Docker-based deployment

## Architecture and Workflow

### 1. Code Ingestion

The ingestion pipeline processes project files and prepares source code for semantic retrieval.

- Recursively reads supported project files
- Filters irrelevant files and directories
- Splits source code into manageable chunks
- Preserves file metadata to support source traceability

### 2. Semantic Retrieval

Processed code chunks are converted into vector embeddings and stored in a vector database.

When a developer submits a question, the retrieval component searches for semantically relevant code fragments to provide context for the response.

### 3. Context-Aware Answer Generation

The retrieved code context is passed to the language model to generate an answer relevant to the repository.

The assistant is designed to base its explanations on retrieved source code and provide useful references to the relevant files. Retrieval and source references help users verify responses, although they do not guarantee that every generated statement is correct.

### 4. Conversational Interface

The web interface allows developers to ask questions about a codebase and review generated explanations.

The goal is to make repository exploration more intuitive and reduce the time required to locate and understand relevant implementation details.

### 5. Evaluation and Optimization

RAG systems can be evaluated across several dimensions:

- **Context relevance:** whether retrieved chunks are relevant to the question
- **Groundedness:** whether the answer is supported by the retrieved context
- **Answer relevance:** whether the response addresses the original question

Retrieval parameters, including the number of retrieved chunks (`top-k`), can be tuned to improve the relevance and usefulness of responses.

## Engineering Principles

### Modular Architecture

The ingestion, retrieval, and generation components are separated to make the system easier to maintain and extend.

### Context Optimization

Filtering irrelevant files and splitting source code into chunks helps reduce noise in the retrieval process and makes better use of the model's context window.

### Source Traceability

File metadata and retrieved code snippets help developers trace answers back to the project and independently verify the explanations.

### Credential Management

API credentials and other sensitive configuration values are provided through environment variables rather than hardcoded into application source files.

### Privacy Considerations

Code privacy depends on the configured model provider and application settings. When using a hosted LLM API, the relevant code context may be sent to that provider for processing. Sensitive repositories should only be used in accordance with the provider's terms and the project's data-handling configuration.

## Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Backend / API | FastAPI |
| AI Orchestration | LangChain |
| Language Model | OpenAI |
| Vector Database | ChromaDB |
| Database | SQLite |
| Frontend | Streamlit |
| Containerization | Docker, Docker Compose |
| Configuration | Environment variables, `.env` |

## Project Structure

The project is organized around the main components of the RAG workflow.

```text
app/
├── ingestion/
├── retrieval/
├── generation/
├── api/
└── ...

tests/
data/
.env.example
Dockerfile
docker-compose.yml
requirements.txt
README.md
```

*Adjust this structure to match the actual repository layout.*

## Configuration

Credentials are not intended to be committed to the repository.

1. Create a local `.env` file in the project root.
2. Use `.env.example` as a template.
3. Add the required configuration values, including the API key if the selected model requires one.
4. Keep `.env` excluded from Git.

Never commit real API keys, passwords, or administrative tokens.

## Installation and Deployment

Clone the repository:

```bash
git clone https://github.com/laurariescomartin/codex-assist.git
cd codex-assist
```

Install the Python dependencies:

```bash
python -m venv .venv
```

Activate the virtual environment.

On Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Configure the environment:

```bash
cp .env.example .env
```

On Windows, you can copy the file using:

```powershell
Copy-Item .env.example .env
```

Complete the required values in `.env` before launching the application.

### Docker

If the Docker Compose configuration is ready to use:

```bash
docker compose up --build
```

Consult the application's configuration and startup instructions for the correct service URL and any additional setup requirements.

## Functional Demo

The following video demonstrates the interface and the platform's workflow when analyzing a repository in a local environment.

[Watch the CodexAssist demo](https://github.com/user-attachments/assets/0fb30b1c-d64b-4173-8ee2-cccc7b911cd7)

## Project Context

Developed as a Final Degree Project (*Trabajo de Fin de Grado*) at Universidad Pontificia de Salamanca (UPSA) during the 2025–2026 academic year.
