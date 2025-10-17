import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from flask import Flask, g, redirect, render_template, request, flash, url_for

DATABASE_PATH = Path("klout.db")

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-change-me"
app.config["DATABASE"] = str(DATABASE_PATH)


# --- Database helpers ------------------------------------------------------

def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(
            app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            check_same_thread=False,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception: Optional[BaseException]) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = get_db()
    with db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                handle TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS bids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bidder_name TEXT NOT NULL,
                message TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )


# --- Bid ranking logic -----------------------------------------------------

BASE_DECAY_RATE = 0.02  # base decay multiplier per hour

def current_effective_amount(amount: float, created_at: datetime) -> float:
    """Calculate the decayed effective amount for a bid."""
    now = datetime.now(timezone.utc)
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    elapsed_hours = (now - created_at).total_seconds() / 3600
    decay_rate = BASE_DECAY_RATE * max(amount, 0)
    return amount * math.exp(-decay_rate * elapsed_hours)


def fetch_leading_bid() -> Optional[sqlite3.Row]:
    db = get_db()
    bids = db.execute("SELECT * FROM bids ORDER BY created_at DESC").fetchall()
    if not bids:
        return None

    leading = None
    highest_effective = -1.0
    for bid in bids:
        created_at = datetime.fromisoformat(bid["created_at"]) if isinstance(bid["created_at"], str) else bid["created_at"]
        effective = current_effective_amount(bid["amount"], created_at)
        if effective > highest_effective:
            highest_effective = effective
            leading = {
                "id": bid["id"],
                "bidder_name": bid["bidder_name"],
                "message": bid["message"],
                "amount": bid["amount"],
                "created_at": created_at,
                "effective_amount": effective,
            }
    return leading


# --- Routes ----------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    init_db()
    db = get_db()

    posts = db.execute(
        "SELECT id, handle, content, created_at FROM posts ORDER BY created_at DESC"
    ).fetchall()

    leading_bid = fetch_leading_bid()
    return render_template("index.html", posts=posts, leading_bid=leading_bid)


@app.route("/posts", methods=["POST"])
def create_post():
    init_db()
    handle = request.form.get("handle", "").strip()
    content = request.form.get("content", "").strip()

    if not handle:
        flash("Display name is required to post.", "error")
    elif not content:
        flash("Post cannot be empty.", "error")
    else:
        db = get_db()
        with db:
            db.execute(
                "INSERT INTO posts (handle, content, created_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (handle, content),
            )
        flash("Your post has been shared with the Klout feed!", "success")
    return redirect(url_for("index"))


@app.route("/bids", methods=["POST"])
def place_bid():
    init_db()
    bidder_name = request.form.get("bidder_name", "").strip()
    message = request.form.get("message", "").strip()
    amount_raw = request.form.get("amount", "").strip()

    error = None
    try:
        amount = float(amount_raw)
    except ValueError:
        error = "Bid amount must be a number."
        amount = 0.0

    if not bidder_name:
        error = "Bidder name is required."
    elif not message:
        error = "A message is required to bid."
    elif amount <= 0:
        error = "Bid amount must be greater than zero."

    leading = fetch_leading_bid()
    leading_effective = leading["effective_amount"] if leading else 0.0

    if error is None and amount <= leading_effective:
        error = "Bid must exceed the current decayed winning amount (%.2f)." % leading_effective

    if error:
        flash(error, "error")
        return redirect(url_for("index"))

    db = get_db()
    with db:
        db.execute(
            "INSERT INTO bids (bidder_name, message, amount, created_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
            (bidder_name, message, amount),
        )
    flash("You are now at the top of Klout!", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
