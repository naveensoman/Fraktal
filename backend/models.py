from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

# Future models (Post, Comment) can be added here.
# For example:
# class Post(db.Model):
#     __tablename__ = 'posts'
#     post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     title = db.Column(db.String(255), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     author = db.relationship('User', backref=db.backref('posts', lazy=True))

# class Comment(db.Model):
#     __tablename__ = 'comments'
#     comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     author = db.relationship('User', backref=db.backref('comments', lazy=True))
#     post = db.relationship('Post', backref=db.backref('comments', lazy=True))
