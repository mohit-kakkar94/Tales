from talesBlogging import db, loginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@loginManager.user_loader
def loadUser(userId):
    return User.query.get(userId)


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    profileImage = db.Column(db.String(64), nullable=False, default="defaultProfile.png")
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    passwordHash = db.Column(db.String(128))

    posts = db.relationship("BlogPost", backref="author", lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.passwordHash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.passwordHash, password)

    def __repr__(self):
        return f"Username {self.username}"

class BlogPost(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("users.id")) #"users.id" refers to primary key "id" in "users"
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, userId):
        self.title = title
        self.text = text
        self.userId = userId

    def __repr__(self):
        return f"Post ID: {self.id} --- Date: {self.date} --- {self.title}"
