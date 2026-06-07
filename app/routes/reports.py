from flask import Blueprint, render_template
from flask_login import login_required
from app.models.sale import Sale
from app import db
from sqlalchemy import func

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/')
@login_required
def index():
    total_sales = Sale.query.count()
    total_revenue = db.session.query(func.sum(Sale.total_amount)).scalar() or 0.0
    recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(10).all()
    return render_template('reports.html', total_sales=total_sales, total_revenue=total_revenue, recent_sales=recent_sales)
