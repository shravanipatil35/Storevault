from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app import create_app, db
from app.models.product import Product
from app.models.supplier import Supplier
from app.models.sale import Sale

app = create_app()

with app.app_context():
    db.create_all()

    if Supplier.query.count() == 0:
        suppliers = [
            Supplier(name='Prime Supplies', contact_person='Ayesha Khan', phone='+91 98765 43210', email='ayesha@primesupplies.com', address='123 Market Street, Delhi'),
            Supplier(name='Elite Traders', contact_person='Rohan Mehta', phone='+91 91234 56789', email='rohan@elitetraders.com', address='45 Commerce Road, Mumbai'),
            Supplier(name='Urban Wholesale', contact_person='Priya Sharma', phone='+91 99887 66554', email='priya@urbanwholesale.com', address='78 Industrial Area, Bangalore'),
        ]
        db.session.add_all(suppliers)
        db.session.commit()
        print('Inserted sample suppliers.')
    else:
        print('Suppliers already exist; skipping supplier seed.')

    if Product.query.count() == 0:
        supplier = Supplier.query.first()
        products = [
            Product(name='Classic Notebook', price=149.99, stock=42, supplier_id=supplier.id),
            Product(name='Wireless Mouse', price=799.00, stock=18, supplier_id=supplier.id),
            Product(name='LED Desk Lamp', price=1299.50, stock=9, supplier_id=supplier.id),
            Product(name='Office Chair', price=4999.00, stock=6, supplier_id=supplier.id),
        ]
        db.session.add_all(products)
        db.session.commit()
        print('Inserted sample products.')
    else:
        print('Products already exist; skipping product seed.')

    if Sale.query.count() == 0:
        product_ids = [p.id for p in Product.query.limit(4).all()]
        now = datetime.now(ZoneInfo('Asia/Kolkata')).replace(tzinfo=None)
        sales = [
            Sale(product_id=product_ids[0], quantity=2, total_amount=299.98, sale_date=now - timedelta(hours=1)),
            Sale(product_id=product_ids[1], quantity=1, total_amount=799.00, sale_date=now - timedelta(hours=2)),
            Sale(product_id=product_ids[2], quantity=3, total_amount=3898.50, sale_date=now - timedelta(days=1)),
            Sale(product_id=product_ids[3], quantity=1, total_amount=4999.00, sale_date=now - timedelta(days=2)),
        ]
        db.session.add_all(sales)
        db.session.commit()
        print('Inserted sample sales.')
    else:
        print('Sales already exist; skipping sales seed.')

    print('Seed data setup complete.')
