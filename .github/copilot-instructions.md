# Project Guidelines

## Code Style
- Python: Follow PEP 8 standards, use descriptive variable names
- JavaScript: Use modern ES6+ features, consistent indentation
- Reference: [src/app.py](src/app.py) for Python patterns, [src/static/app.js](src/static/app.js) for JS patterns

## Architecture
- Backend: FastAPI application with REST endpoints for activities management
- Frontend: Vanilla JavaScript with fetch API for API calls
- Data: In-memory storage (resets on restart) - suitable for demo/learning purposes
- Components: API server ([src/app.py](src/app.py)), static web interface ([src/static/](src/static/))

## Build and Test
- Install: `pip install -r requirements.txt`
- Run: `python src/app.py` (starts server on localhost:8000)
- Test: `pytest` (framework configured, add tests as needed)
- Docs: API at http://localhost:8000/docs, web interface at http://localhost:8000

## Conventions
- Activity names as URL paths: Use `encodeURIComponent()` for special characters
- Signup via query parameter: `POST /activities/{name}/signup?email=user@domain.com`
- No data persistence: Changes lost on server restart
- Participant limits defined but not enforced: Add validation in signup endpoint
- No duplicate signup prevention: Implement email uniqueness check