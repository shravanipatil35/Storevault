from app import db
from datetime import datetime
from zoneinfo import ZoneInfo


def india_now():
    return datetime.now(ZoneInfo('Asia/Kolkata')).replace(tzinfo=None)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))

    created_at = db.Column(db.DateTime, default=india_now)
