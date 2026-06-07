from app import db
from flask_login import UserMixin
from datetime import datetime
from zoneinfo import ZoneInfo
from werkzeug.security import generate_password_hash, check_password_hash


def india_now():
    return datetime.now(ZoneInfo('Asia/Kolkata')).replace(tzinfo=None)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='staff')  # admin / staff
    created_at = db.Column(db.DateTime, default=india_now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
