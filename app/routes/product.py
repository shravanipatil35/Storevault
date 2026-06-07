from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app.models.product import Product
from app.models.supplier import Supplier
from app import db

product_bp = Blueprint('product', __name__)

# SHOW PRODUCTS
@product_bp.route('/')
@login_required
def index():
    products = Product.query.all()
    return render_template('product.html', products=products)


@product_bp.route('/<int:product_id>')
@login_required
def view_product(product_id):
    product = Product.query.get_or_404(product_id)
    supplier = None

    if product.supplier_id:
        supplier = Supplier.query.get(product.supplier_id)

    return render_template('view_product.html', product=product, supplier=supplier)


# ADD PRODUCT (THIS WAS MISSING/NEEDED)
@product_bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':

        name = request.form['name']
        price = float(request.form['price'])   # FIX
        stock = int(request.form['stock'])     # FIX

        new_product = Product(
            name=name,
            price=price,
            stock=stock
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('product.index'))

    return render_template('add_product.html')
