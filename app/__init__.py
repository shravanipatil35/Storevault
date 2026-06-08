import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    # Define the base directory relative to this file
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app = Flask(
        __name__,
        template_folder=os.path.join(basedir, 'app', 'templates'),
        static_folder=os.path.join(basedir, 'app', 'static')
    )
    
    # 1. Apply configuration
    app.config.from_object(Config)
    
    # 2. Force Environment Variables
    if os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-hard-coded-dev-key-123')
    
    # 3. Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # 4. Import models and create tables
    with app.app_context():
        from app.models.user import User
        from app.models.category import Category
        from app.models.product import Product
        from app.models.supplier import Supplier
        from app.models.sale import Sale
        db.create_all()

    # 5. Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.product import product_bp
    from app.routes.sale import sale_bp
    from app.routes.supplier import supplier_bp
    from app.routes.reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(sale_bp, url_prefix='/sales')
    app.register_blueprint(supplier_bp, url_prefix='/suppliers')
    app.register_blueprint(reports_bp, url_prefix='/reports')

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))