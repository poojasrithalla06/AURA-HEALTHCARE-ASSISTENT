---
description: Standard development and execution workflow for AuraHealth
---

# 🏥 AuraHealth Development Workflow

Follow these steps to run, maintain, and expand the AuraHealth AI Assistant.

## 1. Running the Application
To start the local development server:
// turbo
```powershell
python app.py
```
View the app at: `http://127.0.0.1:5000`

## 2. Installing Dependencies
If you add new libraries to the project, update `requirements.txt` and run:
// turbo
```powershell
python -m pip install -r requirements.txt
```

## 3. Database Management
The app uses SQLite (`aurahealth.db`). To reset or update the database schema:
1. Delete the `instance/aurahealth.db` file (if it exists).
2. Restart `app.py`. The models in `models/database.py` will automatically recreate the tables.

## 4. Expanding AI Logic
To add more languages or medical specialized responses:
1. Open `utils/ai_engine.py`.
2. Add the new keywords to the `intents` dictionary.
3. Add the localized responses to the `responses` dictionary.

## 5. Deployment (Production)
The project is configured for **Render** or **Heroku** via the `Procfile`.
- Ensure `gunicorn` is in `requirements.txt`.
- The entry point is `app:app`.
