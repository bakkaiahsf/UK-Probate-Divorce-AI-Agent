# UK Probate Divorce AI Agent Backend

This is the backend for the UK Probate Divorce AI Agent, a FastAPI-based service that leverages CrewAI and LLMs to automate and assist with UK probate and divorce case processing.

## Features
- Modular API with versioned endpoints
- CrewAI-powered legal reasoning and document analysis
- Inheritance tax and GDPR compliance logic
- Easily extensible for new legal workflows

## Project Structure
```
backend/
  app/
    api/v1/endpoints/
    core/
    crews/
    models/
    schemas/
    services/
  data/
  tests/
  main.py
  requirements.txt
```

## Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/bakkaiahsf/UK-Probate-Divorce-AI-Agent.git
   cd UK-Probate-Divorce-AI-Agent/backend
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # Or
   source .venv/bin/activate  # On macOS/Linux
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in your API keys:
     - `OPENAI_API_KEY`
     - `SERPER_API_KEY` (if using web search)

## Running the Server
From the `backend` directory:
```sh
uvicorn app.api.v1.api:app --reload --host 127.0.0.1 --port 8000
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation.

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `SERPER_API_KEY`: Your Serper.dev API key (for web search)

## Testing
```sh
python -m unittest discover tests
```

## Contact
For questions or support, open an issue or contact [Bakkaiah Madipalli](mailto:bakkaiahmadipalli@gmail.com).
