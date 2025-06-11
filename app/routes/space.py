from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models import Space, Review, Booking
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func

space = Blueprint('space', __name__)

@space.route('/spaces')
def index():
    """List all available spaces with search and filter options"""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['SPACES_PER_PAGE']
    
    # Get filter parameters
    location = request.args.get('location')
    capacity_min = request.args.get('capacity_min', type=int)
    capacity_max = request.args.get('capacity_max', type=int)
    
    # Build query
    query = Space.query.filter_by(is_available=True)
    
    if location:
        query = query.filter(Space.location == location)
    if capacity_min:
        query = query.filter(Space.capacity >= capacity_min)
    if capacity_max:
        query = query.filter(Space.capacity <= capacity_max)
    
    # Get locations for filter dropdown
    locations = db.session.query(Space.location).distinct().all()
    
    # Paginate results
    spaces = query.order_by(Space.name).paginate(page=page, per_page=per_page)
    
    return render_template('pages/spaces/index.html', 
                           spaces=spaces,
                           locations=locations,
                           selected_location=location,
                           capacity_min=capacity_min,
                           capacity_max=capacity_max)

@space.route('/spaces/<int:space_id>')
def detail(space_id):
    """Show detailed information about a specific space"""
    space = Space.query.get_or_404(space_id)
    
    # Get reviews
    reviews = Review.query.filter_by(space_id=space_id).order_by(Review.created_at.desc()).all()
    
    # Calculate average rating
    avg_rating = db.session.query(func.avg(Review.rating)).filter(Review.space_id == space_id).scalar() or 0
    
    # Get available time slots for next 7 days
    today = datetime.now().date()
    date_slots = []
    for i in range(7):
        current_date = today + timedelta(days=i)
        date_slots.append(current_date)
    
    return render_template('pages/spaces/detail.html', 
                           space=space,
                           reviews=reviews,
                           avg_rating=avg_rating,
                           date_slots=date_slots)

@space.route('/spaces/<int:space_id>/available-slots', methods=['POST'])
@login_required
def available_slots(space_id):
    """AJAX endpoint to get available time slots for a specific date"""
    space = Space.query.get_or_404(space_id)
    date_str = request.form.get('date')
    
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return {"error": "Invalid date format"}, 400
    
    # Generate all possible hourly slots
    start_hour = current_app.config['BOOKING_START_HOUR']
    end_hour = current_app.config['BOOKING_END_HOUR']
    
    all_slots = []
    for hour in range(start_hour, end_hour):
        slot_start = datetime.combine(selected_date, datetime.min.time().replace(hour=hour))
        slot_end = slot_start + timedelta(hours=1)
        
        # Check if slot is available
        is_available = space.is_available_at(slot_start, slot_end)
        
        all_slots.append({
            'start': slot_start.strftime('%H:%M'),
            'end': slot_end.strftime('%H:%M'),
            'available': is_available
        })
    
    return {"slots": all_slots}