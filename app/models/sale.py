from app import db
from datetime import datetime
from zoneinfo import ZoneInfo


def india_now():
    return datetime.now(ZoneInfo('Asia/Kolkata')).replace(tzinfo=None)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, default=india_now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
