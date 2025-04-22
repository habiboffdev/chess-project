# Chess Tournament Platform

> A full-featured tournament management API built with Django 5.0 and Django REST Framework.

This project provides a backend service for organizing chess tournaments with player registration, Elo-based matchmaking, match result reporting, and JWT-secured user management.

---

## 🌟 Key Features

- **Player Management**: Create and manage player profiles with custom Elo rating fields.
- **Tournament Organizer**: CRUD operations for Tournaments, including Swiss-system and round-robin pairing logic.  
- **Match Recording**: Report match outcomes; automatic Elo rating updates after each match.  
- **Standalone Pairing**: Generate pairings without an active tournament for ad-hoc matches.
- **Authentication & Permissions**: JWT-based authentication; admin (is_staff) users can create tournaments and record matches.
- **Interactive API Docs**: Swagger/OpenAPI UI available at `/docs/` for easy exploration.

---

## 📦 Tech Stack

- **Framework**: Django 5.0, Django REST Framework
- **Authentication**: JSON Web Tokens via `djangorestframework-simplejwt`
- **Database**: PostgreSQL (development uses SQLite3 by default)
- **Testing**: pytest with Django and DRF support
- **Continuous Integration**: (Suggested) GitHub Actions for linting, tests, and coverage

---

## 📂 Project Structure

```
├── Chess/           # Tournament app: models, serializers, views, pairing logic
├── Users/           # User app: custom user model, JWT auth endpoints
├── core/            # Global settings, URL routes, JWT config
├── tests/           # Unit and integration tests
├── manage.py        # Django CLI
├── Pipfile          # Dependency management
├── pytest.ini       # pytest configuration
└── README.md        # Project documentation
```

---

## 🚀 Setup & Run Locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/habiboffdev/chess-project.git
   cd chess-project
   ```
2. **Install dependencies**
   ```bash
   pip install pipenv          # or use virtualenv + requirements.txt
   pipenv install --dev       # or `pip install -r requirements.txt`
   ```
3. **Configure environment**
   - Copy `.env.example` to `.env` and set:
     ```ini
     SECRET_KEY=<your-secret-key>
     DEBUG=True
     ALLOWED_HOSTS=localhost,127.0.0.1
     DATABASE_URL=sqlite:///db.sqlite3  # or your PostgreSQL URI
     ```
4. **Apply database migrations**
   ```bash
   pipenv run python manage.py migrate
   ```
5. **Create superuser**
   ```bash
   pipenv run python manage.py createsuperuser
   ```
6. **Start the development server**
   ```bash
   pipenv run python manage.py runserver 127.0.0.1:8000
   ```
7. **Explore the API**
   - Visit `http://127.0.0.1:8000/docs/` for Swagger UI.
   - Admin panel at `http://127.0.0.1:8000/admin/`.

---

## 🔧 Configuration Details

- **Pairing Constants**: Adjust pairing behavior (e.g., tie-break rules) in `Chess/constants.py`.
- **JWT Settings**: Modify token lifetimes in `core/settings.py` under `SIMPLE_JWT`.
- **CORS & Security**: Update `CORS_ALLOWED_ORIGINS` and `ALLOWED_HOSTS` for production.

---

## 🧪 Testing

Run the full test suite with:
```bash
pipenv run pytest --cov
```
Ensure 100% coverage of models, views, pairing logic, and authentication flows.

---

## 🤝 Contributing Guidelines

1. Fork the repository.  
2. Create a feature branch: `git checkout -b feature/awesome-feature`  
3. Commit changes: `git commit -m "Add awesome feature"`  
4. Push: `git push origin feature/awesome-feature`  
5. Open a pull request and ensure CI checks pass.

---

## 🎯 Roadmap & CI/CD

- **CI Integration**: Add GitHub Actions workflow for automated linting (flake8), formatting (black), and tests on every pull request.
- **Deployment**: Configure Docker and Heroku/Render for one-click deployments.
- **Feature Flags**: Introduce Django Waffle for toggling experimental pairing algorithms.

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

_Last updated: April 22, 2025_

