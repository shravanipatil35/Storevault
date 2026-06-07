from flask import Blueprint, render_template
from flask_login import login_required
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy import func

from app import db
from app.models.product import Product
from app.models.sale import Sale
from app.models.supplier import Supplier

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    total_products = Product.query.count()
    low_stock_count = Product.query.filter(Product.stock < 10).count()
    suppliers_count = Supplier.query.count()
    today = datetime.now(ZoneInfo('Asia/Kolkata')).date()
    today_start = datetime.combine(today, time.min)
    tomorrow_start = today_start + timedelta(days=1)
    today_sales = db.session.query(func.coalesce(func.sum(Sale.total_amount), 0.0)).filter(
        Sale.sale_date >= today_start,
        Sale.sale_date < tomorrow_start
    ).scalar()
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()

    return render_template(
        'dashboard.html',
        total_products=total_products,
        low_stock_count=low_stock_count,
        today_sales=today_sales,
        suppliers_count=suppliers_count,
        recent_products=recent_products,
    )
