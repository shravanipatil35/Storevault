from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.product import Product
from app.models.sale import Sale

sale_bp = Blueprint('sale', __name__)


@sale_bp.route('/pos')
@login_required
def pos():
    products = Product.query.all()

    return render_template('pos.html', products=products)


def _product_payload(product):
    return {
        'id': product.id,
        'name': product.name,
        'price': float(product.price),
        'stock': product.stock,
    }


@sale_bp.route('/api/products')
@login_required
def api_products():
    search = request.args.get('search', '').strip()
    query = Product.query

    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    products = query.order_by(Product.name.asc()).all()
    return jsonify({
        'success': True,
        'products': [_product_payload(product) for product in products],
    })


@sale_bp.route('/api/products/<int:product_id>')
@login_required
def api_product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'success': True,
        'product': _product_payload(product),
    })


@sale_bp.route('/api/checkout', methods=['POST'])
@sale_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    data = request.get_json(silent=True) or {}
    items = data.get('items') or data.get('cart') or []

    if not isinstance(items, list) or not items:
        return jsonify({
            'success': False,
            'message': 'Cart is empty.',
        }), 400

    quantities = {}
    for item in items:
        try:
            product_id = int(item.get('product_id', item.get('id')))
            quantity = int(item.get('quantity', item.get('qty', 1)))
        except (TypeError, ValueError, AttributeError):
            return jsonify({
                'success': False,
                'message': 'Invalid cart item.',
            }), 400

        if quantity <= 0:
            return jsonify({
                'success': False,
                'message': 'Quantity must be greater than zero.',
            }), 400

        quantities[product_id] = quantities.get(product_id, 0) + quantity

    try:
        products = Product.query.filter(Product.id.in_(quantities.keys())).with_for_update().all()
        products_by_id = {product.id: product for product in products}
        missing_ids = [product_id for product_id in quantities if product_id not in products_by_id]

        if missing_ids:
            return jsonify({
                'success': False,
                'message': 'One or more products were not found.',
                'missing_product_ids': missing_ids,
            }), 404

        for product_id, quantity in quantities.items():
            product = products_by_id[product_id]
            if product.stock < quantity:
                return jsonify({
                    'success': False,
                    'message': f'Not enough stock for {product.name}.',
                    'product_id': product.id,
                    'available_stock': product.stock,
                }), 400

        sales = []
        total_amount = 0.0
        for product_id, quantity in quantities.items():
            product = products_by_id[product_id]
            line_total = float(product.price) * quantity
            product.stock -= quantity
            sale = Sale(
                product_id=product.id,
                quantity=quantity,
                total_amount=line_total,
                user_id=current_user.id,
            )
            db.session.add(sale)
            sales.append(sale)
            total_amount += line_total

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Sale completed successfully.',
            'sale_ids': [sale.id for sale in sales],
            'total_amount': round(total_amount, 2),
            'items': [
                {
                    'product_id': sale.product_id,
                    'quantity': sale.quantity,
                    'total_amount': round(sale.total_amount, 2),
                }
                for sale in sales
            ],
        }), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Unable to complete sale. Please try again.',
        }), 500
