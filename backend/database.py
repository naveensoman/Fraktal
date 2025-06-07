from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# This is used by models.py to define models
db = SQLAlchemy()

# For direct session management if needed, though Flask-SQLAlchemy handles much of this.
# Not strictly necessary for this subtask if Flask-SQLAlchemy's session is used directly.
_SessionLocal = None
_engine = None

def init_db(app, db_uri='postgresql://user:password@localhost/mydatabase'):
    """
    Initializes the database with the Flask app.
    Sets up SQLAlchemy and creates tables if they don't exist.
    """
    global _engine, _SessionLocal

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Recommended to disable

    db.init_app(app)

    _engine = db.engine # or create_engine(db_uri)
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    with app.app_context():
        # Import models here to ensure they are registered with SQLAlchemy
        # before creating tables.
        from . import models # noqa
        db.create_all() # Creates tables based on defined models

def get_db_session():
    """
    Provides a database session.
    This might be more relevant if not using Flask-SQLAlchemy's built-in session management.
    For Flask-SQLAlchemy, db.session is typically used directly in routes.
    """
    if not _SessionLocal:
        raise RuntimeError("Database has not been initialized. Call init_db() first.")
    return _SessionLocal()

# Example of how db.session from Flask-SQLAlchemy would be used:
# from .models import User
# user = User(username='test', email='test@example.com', password_hash='...')
# db.session.add(user)
# db.session.commit()
# users = User.query.all()

# This file primarily sets up `db` for Flask-SQLAlchemy and provides an `init_db` function.
# The `get_db_session` is more for manual session handling, which might not be the primary
# way if sticking strictly to Flask-SQLAlchemy patterns.
# Flask-SQLAlchemy's `db.session` is the typical way to interact with the DB in request contexts.
# `init_db` will be called from app.py to set up the database.
