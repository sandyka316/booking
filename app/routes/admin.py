from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Space, Booking, Review
from app import db
from app.utils.decorators import admin_required
from datetime import datetime, timedelta
from sqlalchemy import func
import json

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with key statistics"""
    # Get summary statistics
    total_users = User.query.count()
    total_spaces = Space.query.count()
    total_bookings = Booking.query.count()
    total_reviews = Review.query.count()
    
    # Calculate revenue
    revenue_today = db.session.query(func.sum(Booking.total_price)).filter(
        func.date(Booking.created_at) == datetime.utcnow().date()
    ).scalar() or 0
    
    revenue_week = db.session.query(func.sum(Booking.total_price)).filter(
        Booking.created_at >= datetime.utcnow() - timedelta(days=7)
    ).scalar() or 0
    
    # Get recent bookings
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    
    # Chart data - bookings by day for the last week
    days = []
    booking_counts = []
    
    for i in range(6, -1, -1):
        day = datetime.utcnow().date() - timedelta(days=i)
        days.append(day.strftime('%a'))
        
        count = Booking.query.filter(
            func.date(Booking.created_at) == day
        ).count()
        booking_counts.append(count)
    
    # Top spaces by booking count
    top_spaces = db.session.query(
        Space,
        func.count(Booking.id).label('booking_count')
    ).join(
        Booking, Space.id == Booking.space_id
    ).group_by(
        Space.id
    ).order_by(
        func.count(Booking.id).desc()
    ).limit(5).all()
    
    return render_template('admin/dashboard.html',
                          total_users=total_users,
                          total_spaces=total_spaces,
                          total_bookings=total_bookings,
                          total_reviews=total_reviews,
                          revenue_today=revenue_today,
                          revenue_week=revenue_week,
                          recent_bookings=recent_bookings,
                          days=json.dumps(days),
                          booking_counts=json.dumps(booking_counts),
                          top_spaces=top_spaces)

@admin.route('/spaces')
@login_required
@admin_required
def spaces():
    """Admin management of spaces"""
    spaces = Space.query.order_by(Space.name).all()
    return render_template('admin/spaces/index.html', spaces=spaces)

@admin.route('/spaces/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_space():
    """Create a new space"""
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        capacity = request.form.get('capacity', type=int)
        price_per_hour = request.form.get('price_per_hour', type=float)
        description = request.form.get('description')
        image_url = request.form.get('image_url')
        amenities = request.form.get('amenities')
        
        # Create new space
        new_space = Space(
            name=name,
            location=location,
            capacity=capacity,
            price_per_hour=price_per_hour,
            description=description,
            image_url=image_url,
            amenities=amenities
        )
        
        db.session.add(new_space)
        db.session.commit()
        
        flash('Space successfully created!', 'success')
        return redirect(url_for('admin.spaces'))
    
    return render_template('admin/spaces/create.html')

@admin.route('/spaces/<int:space_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_space(space_id):
    """Edit an existing space"""
    space = Space.query.get_or_404(space_id)
    
    if request.method == 'POST':
        space.name = request.form.get('name')
        space.location = request.form.get('location')
        space.capacity = request.form.get('capacity', type=int)
        space.price_per_hour = request.form.get('price_per_hour', type=float)
        space.description = request.form.get('description')
        space.image_url = request.form.get('image_url')
        space.amenities = request.form.get('amenities')
        space.is_available = 'is_available' in request.form
        
        db.session.commit()
        
        flash('Space successfully updated!', 'success')
        return redirect(url_for('admin.spaces'))
    
    return render_template('admin/spaces/edit.html', space=space)

@admin.route('/spaces/<int:space_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_space(space_id):
    """Delete a space"""
    space = Space.query.get_or_404(space_id)
    
    db.session.delete(space)
    db.session.commit()
    
    flash('Space successfully deleted!', 'success')
    return redirect(url_for('admin.spaces'))

@admin.route('/users')
@login_required
@admin_required
def users():
    """Admin management of users"""
    users = User.query.order_by(User.username).all()
    return render_template('admin/users/index.html', users=users)

@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Edit an existing user"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.role = request.form.get('role')
        user.is_active = 'is_active' in request.form
        
        db.session.commit()
        
        flash('User successfully updated!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/users/edit.html', user=user)

@admin.route('/bookings')
@login_required
@admin_required
def bookings():
    """Admin management of bookings"""
    # Get filter parameters
    status = request.args.get('status')
    
    # Build query
    query = Booking.query
    
    if status:
        query = query.filter(Booking.status == status)
    
    bookings = query.order_by(Booking.start_time).all()
    
    return render_template('admin/bookings/index.html', 
                           bookings=bookings,
                           selected_status=status)