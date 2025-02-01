# Household Services Platform

A full-stack marketplace for connecting homeowners with vetted service professionals. The platform pairs a Flask API with Celery-based background processing and a Vue 3 (Vite) frontend.

> **Environment note**
> All setup instructions target Linux shells, including Windows Subsystem for Linux (WSL). If you are on native Windows, install WSL (`wsl --install`) and run the commands from your WSL terminal.

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Quick Start](#quick-start)
  - [Backend (Flask)](#backend-flask)
  - [Frontend (Vue 3)](#frontend-vue-3)
  - [Background Workers](#background-workers)
- [Environment & Configuration](#environment--configuration)
- [Useful Commands](#useful-commands)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## Features
- Role-based access for administrators, homeowners, and service professionals
- Service catalogue management with request lifecycles (open -> bidding -> accepted -> closed)
- Admin analytics dashboard with real-time request and user metrics
- Redis-backed Celery workers for asynchronous tasks, exports, and scheduled jobs
- Responsive Vue 3 frontend with rich interactions powered by Vite

## Tech Stack
| Layer | Technology |
|-------|------------|
| API | Python, Flask, SQLAlchemy, JWT |
| Background jobs | Celery, Redis |
| Frontend | Vue 3, Vite, Bootstrap 5 |
| Database | SQLite (dev) |
| Tooling | npm, Node.js 18+, pytest |

## Repository Structure
```
mad2/
|-- Backend/        # Flask app, Celery workers, database models
|-- Frontend/       # Vue 3 client built with Vite
|-- projectenv/     # (optional) Python virtual environment
`-- README.md
```

---

## Quick Start

### Backend (Flask)
```bash
# Create & activate virtual environment
python3 -m venv projectenv
source projectenv/bin/activate

# Install dependencies
cd Backend
pip install -r requirements.txt

# Start the API
python3 main.py
```
The API listens on `http://127.0.0.1:5000` and auto-creates the SQLite database with a seeded admin user (credentials: `admin / 8887832`).

### Frontend (Vue 3)
Open a new WSL terminal and keep the backend running.
```bash
cd ~/path/to/mad2/Frontend
npm install
npm run dev
```
Vite serves the client at `http://127.0.0.1:5173` with hot module replacement.

### Background Workers
The project relies on Redis and Celery for asynchronous tasks.

1. **Install & start Redis (first time):**
   ```bash
   sudo apt update
   sudo apt install redis-server
   sudo service redis-server start
   ```
2. **Celery worker:**
   ```bash
   cd ~/path/to/mad2/Backend
   celery -A main.celery worker --loglevel=info
   ```
3. **Celery beat (optional scheduler):**
   ```bash
   cd ~/path/to/mad2/Backend
   celery -A main.celery beat --loglevel=info
   ```
Run items 2 and 3 in separate terminals after the API is running.

---

## Environment & Configuration
- **Database:** SQLite file at `Backend/householdservices.sqlite3` (auto-created)
- **Cache & Broker:** Redis on `redis://localhost:6379`
- **Celery configuration:** Defined in `Backend/main.py`
- **Admin credentials:** `admin / 8887832`
- **Environment variables:** Adjust secrets (e.g., `SECRET_KEY`, `JWT_SECRET_KEY`) in `Backend/main.py` before deploying beyond local development

---

## Useful Commands
```bash
# Activate Python virtual environment
source projectenv/bin/activate

# Run backend unit tests
test -d Backend && cd Backend && pytest

# Build frontend for production
cd Frontend
npm run build

# Lint Vue project (if eslint configured)
npm run lint
```

---

## Troubleshooting
| Issue | Resolution |
|-------|------------|
| `redis-server: command not found` | Install Redis inside WSL: `sudo apt install redis-server` |
| Celery cannot connect to Redis | Ensure Redis is running: `sudo service redis-server status` |
| Virtualenv fails to activate | Confirm you are inside WSL and using `source projectenv/bin/activate` |
| Frontend API requests fail | Confirm Flask server is running on port 5000 and CORS is enabled |

---

## Next Steps
- Replace development secrets with environment variables for staging/production
- Swap SQLite for a managed database (e.g., PostgreSQL) as the project grows
- Containerise services (Docker + docker-compose) for consistent deployment environments
- Add CI pipelines (GitHub Actions) for automated testing and linting

Happy building!
