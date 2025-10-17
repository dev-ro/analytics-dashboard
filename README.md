# AI-Powered Analytics Dashboard

A learning project demonstrating modern tech stack proficiency with Next.js, FastAPI, BigQuery, SQLModel, and LangGraph.

## Project Overview

This project showcases a complete modern web application stack, implementing best practices from the Modern Tech Stack Interview Study Guide. It demonstrates:

- **Trunk-Based Development** with short-lived feature branches
- **Next.js** with SSG/SSR rendering strategies
- **Tailwind CSS** with component-based architecture
- **FastAPI** with async/await patterns
- **BigQuery** integration with optimized queries
- **SQLModel** for unified data modeling
- **LangGraph** AI agents for intelligent insights

## Technology Stack

- **Frontend**: Next.js (Pages Router) + Tailwind CSS
- **Backend**: FastAPI (Python 3.11+) with async/await
- **Data Warehouse**: Google BigQuery (free public datasets)
- **Local Database**: SQLite with SQLModel
- **Data Validation**: Pydantic
- **AI Layer**: LangGraph with OpenAI/Anthropic API
- **Version Control**: Git with Trunk-Based Development (TBD)

## Project Structure

```
analytics-dashboard/
├── frontend/                 # Next.js application
│   ├── pages/               # SSG/SSR pages
│   ├── components/          # Reusable React components
│   ├── styles/              # Tailwind config
│   └── lib/                 # API client utilities
├── backend/                 # FastAPI application
│   ├── main.py             # FastAPI app entry
│   ├── models/             # SQLModel definitions
│   ├── api/                # API route handlers
│   ├── services/           # Business logic
│   └── agents/             # LangGraph AI agents
├── .github/                # GitHub workflows (optional)
├── .gitignore
├── README.md
└── requirements.txt        # Python dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- GitHub CLI
- Google Cloud Project (for BigQuery)
- OpenAI or Anthropic API key

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export OPENAI_API_KEY="your-api-key"
export GOOGLE_CLOUD_PROJECT="your-gcp-project"
export DATABASE_URL="sqlite:///./analytics.db"
```

4. Run the backend:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Set environment variables:
```bash
export NEXT_PUBLIC_API_URL="http://localhost:8000"
```

3. Run the frontend:
```bash
npm run dev
```

## Key Concepts Demonstrated

- **TBD**: Short-lived feature branches, frequent merges to main
- **Feature Flags**: Simple boolean flags for AI features
- **Async FastAPI**: All I/O operations use `async def`
- **Dependency Injection**: BigQuery client via `Depends()`
- **Query Optimization**: SELECT specific columns, WHERE filters, LIMIT clauses
- **SSG vs SSR**: Marketing page (SSG), dashboard data (SSR/CSR)
- **Tailwind Best Practices**: Component extraction, design system in config
- **SQLModel**: Single source of truth for API and database
- **Pydantic**: Request/response validation
- **LangGraph**: Stateful agent with nodes, edges, and state management

## Development Workflow

This project follows Trunk-Based Development practices:

1. Work on small features in short-lived branches
2. Open PRs with clear descriptions
3. Merge to main frequently (multiple times per day ideally)
4. Keep main branch always deployable
5. Use feature flags for incomplete features

## Architecture

The application follows a modern microservices-inspired architecture:

- **Frontend**: Next.js serves static content and dynamic pages
- **Backend**: FastAPI provides async API endpoints
- **Data Layer**: SQLModel provides unified data modeling
- **AI Layer**: LangGraph agents generate intelligent insights
- **Data Warehouse**: BigQuery provides analytical data processing

## Contributing

This is a learning project. Follow TBD practices:

1. Create short-lived feature branches
2. Make small, focused commits
3. Open PRs for review
4. Merge frequently to main
5. Keep main branch deployable
