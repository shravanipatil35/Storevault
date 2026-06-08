from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        # Ensure user exists and password is valid
        if user and user.check_password(password):
            login_user(user, remember=True) # remember=True keeps the session alive longer
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid email or password', 'danger')
            
    return render_template('auth/login.html') # Ensure path matches your templates folder

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validation: Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register'))
        
        # Creation: Use a try/except block to catch database commit errors
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Registration failed: {e}")
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')