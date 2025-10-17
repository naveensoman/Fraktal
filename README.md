# Klout

Klout is a minimalist, single-file Twitter-style microblog with a twist: the banner message at the top of the site is always owned by the highest bidder. Every bid decays over time, and higher bids decay faster so no one can monopolise the slot forever.

## Features

- Real-time style timeline for short posts (no authentication required)
- Competitive bidding for the top-of-site announcement with exponential decay that accelerates for large bids
- Server-rendered Flask UI with modern styling
- SQLite persistence with automatic database bootstrapping

## Stack

- Python 3.11+
- Flask 3
- SQLite (bundled with Python)

## Running locally

1. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the development server:

   ```bash
   flask --app app run --debug
   ```

4. Open http://127.0.0.1:5000 in your browser.

The SQLite database file (`klout.db`) will be created automatically on first run.

## Deployment

Because Klout is a regular Flask application with a SQLite backend, you can deploy it anywhere that supports WSGI (Fly.io, Render, Railway, etc.). A minimal production command with Gunicorn would look like:

```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

Remember to set `SECRET_KEY` to a strong random value in production.
