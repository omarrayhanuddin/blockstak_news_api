# Blockstak News API

A production-ready FastAPI backend application that integrates with NewsAPI to fetch and store news articles, featuring OAuth2 authentication, SQLite database, comprehensive testing, and Docker support.

## Project Description

This project implements a news aggregation API using FastAPI with the following features:
- OAuth2 client credentials authentication
- NewsAPI integration for fetching news articles
- SQLite database for storing news
- Pagination support
- Unit tests with >80% coverage
- Docker containerization
- Proper logging and error handling
- Environment variable configuration
- Code linting with Ruff

## Project Structure

Below is the folder structure of the project:

```
blockstak_news_api/
├── .gitignore              # Specifies files and directories to ignore in version control
├── Dockerfile              # Defines the Docker image for containerizing the application
├── README.md               # Project documentation (this file)
├── requirements.txt        # Lists Python dependencies
├── .env.example            # Template for environment variable configuration
├── improvements.md         # Suggestions for future codebase enhancements
├── src/                    # Source code directory
│   ├── __init__.py         # Marks src as a Python package
│   ├── main.py             # Main application entry point with FastAPI setup
│   ├── config.py           # Configuration settings using Pydantic, including hardcoded client credentials
│   ├── auth/               # Authentication-related code
│   │   ├── __init__.py     # Marks auth as a Python package
│   │   └── oauth2.py       # OAuth2 client credentials authentication logic
│   ├── models/             # SQLAlchemy database models
│   │   ├── __init__.py     # Marks models as a Python package
│   │   └── news.py         # News model definition
│   ├── schemas/            # Pydantic schemas for request/response validation
│   │   ├── __init__.py     # Marks schemas as a Python package
│   │   └── news.py         # News-related Pydantic schemas
│   ├── services/           # Business logic for news operations
│   │   ├── __init__.py     # Marks services as a Python package
│   │   └── news_service.py # NewsAPI integration and database operations
│   ├── database/           # Database configuration and session management
│   │   ├── __init__.py     # Marks database as a Python package
│   │   └── database.py     # SQLAlchemy engine and session setup
│   ├── routes/             # API route definitions
│   │   ├── __init__.py     # Marks routes as a Python package
│   │   ├── auth.py         # Endpoint for obtaining access tokens using hardcoded client credentials
│   │   └── news.py         # NewsAPI endpoints for fetching and saving news articles
│   └── tests/              # Unit tests
│       ├── __init__.py     # Marks tests as a Python package
│       ├── test_auth.py    # Tests for authentication logic
│       ├── test_news.py    # Tests for news endpoints
│       └── conftest.py     # Pytest fixtures for testing
```

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/omarrayhanuddin/blockstak_news_api.git
cd blockstak_news_api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy .env.example to .env and configure:
```bash
cp .env.example .env
```
Edit .env with your NewsAPI key, client ID, client secret, and other configurations.

## Running the Server

```bash
uvicorn src.main:app --reload
```

The server will be available at `http://localhost:8000`.

## Running Tests

```bash
pytest --cov=src --cov-report=html
```

This generates a coverage report in the `htmlcov/` directory.

## Using Docker

1. Build the Docker image:
```bash
docker build -t blockstak-news-api .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 --env-file .env blockstak-news-api
```

## Generating Access Tokens

To access protected endpoints, obtain a token using the hardcoded `client_id` and `client_secret` specified in your `.env` file:

```bash
curl -X POST "http://localhost:8000/token" \
-H "Content-Type: application/json" \
-d '{"client_id": "your_client_id", "client_secret": "your_client_secret"}'
```

Response:
```json
{
  "access_token": "your-jwt-token",
  "token_type": "Bearer"
}
```

Use the token in the Authorization header for protected endpoints:
```
Authorization: Bearer your-jwt-token
```

Note: The `client_id` and `client_secret` are configured in the `.env` file and must match the values set in the environment for authentication to succeed.

## API Endpoints

1. **GET /news**
   - Description: Fetch paginated news articles
   - Query Parameters: `page` (default: 1), `page_size` (default: 10)
   - Example:
     ```bash
     curl -H "Authorization: Bearer <token>" "http://localhost:8000/news?page=1&page_size=10"
     ```

2. **POST /news/save-latest**
   - Description: Fetch and save top 3 latest news articles
   - Example:
     ```bash
     curl -X POST -H "Authorization: Bearer <token>" "http://localhost:8000/news/save-latest"
     ```

3. **GET /news/headlines/country/{country_code}**
   - Description: Fetch top headlines by country
   - Example:
     ```bash
     curl -H "Authorization: Bearer <token>" "http://localhost:8000/news/headlines/country/us"
     ```

4. **GET /news/headlines/source/{source_id}**
   - Description: Fetch top headlines by source
   - Example:
     ```bash
     curl -H "Authorization: Bearer <token>" "http://localhost:8000/news/headlines/source/bbc-news"
     ```

5. **GET /news/headlines/filter**
   - Description: Fetch headlines filtered by country and/or source
   - Query Parameters: `country`, `source`
   - Example:
     ```bash
     curl -H "Authorization: Bearer <token>" "http://localhost:8000/news/headlines/filter?country=us&source=bbc-news"
     ```

## Code Improvements

See `improvements.md` for suggestions on enhancing the codebase.
