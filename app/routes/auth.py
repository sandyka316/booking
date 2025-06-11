from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Please check your login details and try again.', 'danger')
            return render_template('auth/login.html')
            
        if not user.is_active:
            flash('This account has been deactivated. Please contact support.', 'danger')
            return render_template('auth/login.html')
            
        login_user(user, remember=remember)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
            
        flash('Logged in successfully!', 'success')
        return redirect(next_page)
        
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Form validation
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('auth/register.html')
            
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash('Email address already registered!', 'danger')
            return render_template('auth/register.html')
            
        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash('Username already taken!', 'danger')
            return render_template('auth/register.html')
        
        # Create new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    if request.method == 'POST':
        # Update user profile
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        
        # Password update (optional)
        if request.form.get('new_password'):
            if check_password_hash(current_user.password_hash, request.form.get('current_password')):
                current_user.password_hash = generate_password_hash(request.form.get('new_password'))
            else:
                flash('Current password is incorrect!', 'danger')
                return redirect(url_for('auth.profile'))
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('auth.profile'))
        
    return render_template('auth/profile.html')