# UMS ChatBot

A University Management System (UMS) chatbot designed to help students ask campus- and academics-related questions using natural-language queries.

**Live application:** https://ums-chat-bot.vercel.app/  
**Repository:** https://github.com/sarfrazcodes/umsChatBot

## Overview

UMS ChatBot combines a web application, a Flask backend, and a Python-based natural-language processing (NLP) module. The NLP module identifies a user's intent, extracts useful entities such as subject codes, and uses limited conversation context to interpret short follow-up questions.

The intent-matching pipeline is based on configured examples and fuzzy string matching. It is not a general-purpose large language model: supported queries depend on the intents and rules defined in the project.

## Key Components

- **Natural-language preprocessing:** Normalizes user input before matching.
- **Intent recognition:** Uses RapidFuzz similarity matching against examples stored in `intents.json`.
- **Entity extraction:** Recognizes information such as subject names/codes, dates, rooms, and maintenance-related categories.
- **Follow-up context:** Reuses the previous intent and subject for certain short follow-up questions.
- **Flask backend:** Provides an application factory and a health-check endpoint at `/api/health`.
- **Database integration:** Uses Flask-SQLAlchemy/SQLAlchemy and a database URL supplied through environment configuration.
- **Web frontend:** The `frontend/` directory contains the user-facing application.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | NLP and backend logic |
| Flask | Backend web framework |
| SQLAlchemy / Flask-SQLAlchemy | Database integration |
| PostgreSQL driver (`psycopg2-binary`) | PostgreSQL connectivity |
| RapidFuzz | Fuzzy intent matching |
| NLTK | NLP-related dependency |
| pandas | Data processing dependency |
| PyJWT | JWT-related backend dependency |
| python-dotenv | Loading environment variables |
| Frontend technologies | Implemented in the `frontend/` directory |

## Repository Structure

```text
umsChatBot/
├── backend/          # Flask backend, configuration, database extensions
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   └── requirements.txt
├── chatbot_logic/    # NLP pipeline and intent configuration
│   ├── chatbot.py
│   ├── matcher.py
│   ├── entities.py
│   ├── preprocessor.py
│   └── intents.json
├── frontend/         # Web interface
└── .gitignore
```

This is a high-level map of the main project components; individual files may change as the project evolves.

## Getting Started

### Prerequisites

- Python 3.10 or newer is recommended.
- pip
- A PostgreSQL database if you are running database-backed features locally.
- Node.js and npm if the frontend uses a Node-based toolchain.

### 1. Clone the repository

```bash
git clone https://github.com/sarfrazcodes/umsChatBot.git
cd umsChatBot
```

### 2. Set up the Python backend

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

### 3. Configure environment variables

The backend reads its database connection from `DATABASE_URL` and its JWT signing secret from `JWT_SECRET`.

Create a local `.env` file in the location from which the backend loads environment variables, and configure values for your environment:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
JWT_SECRET=replace_with_a_long_random_secret
```

Use your own database credentials and a strong secret. Do not commit `.env` files, passwords, database URLs, or tokens to GitHub.

### 4. Start the backend

The Flask application defines a factory in `backend/app.py` and includes a development entry point on port `5000`. From the repository root, run:

```bash
python backend/app.py
```

The health-check endpoint is:

```text
GET http://127.0.0.1:5000/api/health
```

A successful response should look like:

```json
{
  "status": "ok",
  "message": "UMS Backend is running."
}
```

If Python reports an import error when starting the backend from the repository root, run the command from the `backend/` directory instead:

```bash
cd backend
python app.py
```

### 5. Run the NLP module independently

The NLP module includes a terminal runner for testing intent recognition. From the repository root:

```bash
cd chatbot_logic
python chatbot.py
```

Enter a query and inspect the detected intent, query type, extracted entities, confidence score, and whether conversation context was used. Type `exit` or `quit` to leave the runner.

### 6. Start the frontend

The frontend lives in `frontend/`. Install its dependencies and use the development command defined in its package manifest. For a Node-based frontend, the typical workflow is:

```bash
cd frontend
npm install
npm run dev
```

If `npm run dev` is not defined, check the available scripts in `frontend/package.json` and run the appropriate script. The frontend may also need an environment variable pointing to the backend API URL.

## How Intent Recognition Works

At a high level, a user query follows this pipeline:

1. **Normalize:** Clean and normalize the text.
2. **Extract entities:** Identify relevant values, such as recognized subjects or dates.
3. **Match intent:** Compare the normalized query with examples in `chatbot_logic/intents.json` using RapidFuzz.
4. **Check confidence and ambiguity:** Low-confidence or ambiguous queries can be marked as needing clarification.
5. **Use conversation context:** Certain short follow-ups can inherit the previous intent and subject.
6. **Return structured output:** The NLP function returns the intent, query type, entities, confidence, alternatives, clarification flag, and context-use flag.

Example of the *shape* of the NLP result (values are illustrative):

```json
{
  "intent": "EXAMPLE_INTENT",
  "query_type": "example",
  "entities": {
    "subject": "CSE205"
  },
  "confidence": 0.85,
  "alternatives": [],
  "needs_clarification": false,
  "context_used": true
}
```

The actual intent names and supported questions are defined by the project's intent data and entity rules.

## Backend Health Check

The Flask backend exposes:

```http
GET /api/health
```

It returns a JSON status message that can be used to verify that the backend process is running.

## Configuration and Security Notes

- Keep secrets in environment variables, not source code.
- Replace any development-only JWT secret before deployment.
- Restrict database credentials to the minimum permissions the application needs.
- Do not expose database credentials or authentication tokens in logs, screenshots, or public issue reports.
- Use production-appropriate Flask settings when deploying; the built-in `debug=True` entry point is intended for development, not production.

## Current Scope and Limitations

- Intent recognition depends on the examples and rules maintained in `chatbot_logic/intents.json` and the NLP source files.
- Fuzzy matching can misclassify unfamiliar or ambiguous queries; confidence thresholds and clarification handling help reduce this risk but do not eliminate it.
- Follow-up context is rule-based and limited to certain short queries.
- The `/api/health` route confirms that the backend is responding; it does not by itself verify every database query or frontend integration.
- Database-backed features require a correctly configured database and any required schema or seed data.

## Contributing

Contributions and improvements are welcome.

1. Fork the repository.
2. Create a branch for your change.
3. Make and test your changes.
4. Submit a pull request describing what changed and how it was tested.

## License

No license file was visible in the repository root during preparation of this README. Unless a license is added, the repository should not be assumed to grant permission for reuse, redistribution, or modification.
