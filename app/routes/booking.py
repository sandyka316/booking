from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import Space, Booking, Review
from app import db
from datetime import datetime, timedelta

booking = Blueprint('booking', __name__)

@booking.route('/book/<int:space_id>', methods=['GET', 'POST'])
@login_required
def create(space_id):
    """Create a new booking for a space"""
    space = Space.query.get_or_404(space_id)
    
    if request.method == 'POST':
        date_str = request.form.get('date')
        start_time_str = request.form.get('start_time')
        hours = int(request.form.get('hours', 1))
        notes = request.form.get('notes')
        
        # Parse date and time
        try:
            start_datetime = datetime.strptime(f"{date_str} {start_time_str}", '%Y-%m-%d %H:%M')
            end_datetime = start_datetime + timedelta(hours=hours)
        except ValueError:
            flash('Invalid date or time format!', 'danger')
            return redirect(url_for('space.detail', space_id=space_id))
        
        # Check if space is available
        if not space.is_available_at(start_datetime, end_datetime):
            flash('The space is not available at the selected time!', 'danger')
            return redirect(url_for('space.detail', space_id=space_id))
        
        # Calculate total price
        total_price = space.price_per_hour * hours
        
        # Create booking
        new_booking = Booking(
            user_id=current_user.id,
            space_id=space_id,
            start_time=start_datetime,
            end_time=end_datetime,
            total_price=total_price,
            notes=notes
        )
        
        db.session.add(new_booking)
        db.session.commit()
        
        flash('Booking successfully created!', 'success')
        return redirect(url_for('booking.my_bookings'))
    
    return render_template('pages/bookings/create.html', space=space)

@booking.route('/my-bookings')
@login_required
def my_bookings():
    """Show current user's bookings"""
    # Get upcoming bookings
    upcoming = Booking.query.filter_by(
        user_id=current_user.id,
        status='confirmed'
    ).filter(
        Booking.start_time > datetime.utcnow()
    ).order_by(
        Booking.start_time
    ).all()
    
    # Get past bookings
    past = Booking.query.filter_by(
        user_id=current_user.id
    ).filter(
        Booking.end_time < datetime.utcnow()
    ).order_by(
        Booking.start_time.desc()
    ).all()
    
    return render_template('pages/bookings/my_bookings.html', 
                           upcoming_bookings=upcoming,
                           past_bookings=past)

@booking.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel(booking_id):
    """Cancel a booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if booking belongs to current user
    if booking.user_id != current_user.id and not current_user.is_admin():
        flash('You do not have permission to cancel this booking!', 'danger')
        return redirect(url_for('booking.my_bookings'))
    
    # Check if booking can be cancelled
    if not booking.can_be_cancelled():
        flash('This booking cannot be cancelled!', 'danger')
        return redirect(url_for('booking.my_bookings'))
    
    booking.status = 'cancelled'
    db.session.commit()
    
    flash('Booking successfully cancelled!', 'success')
    return redirect(url_for('booking.my_bookings'))

@booking.route('/bookings/<int:booking_id>/review', methods=['GET', 'POST'])
@login_required
def review(booking_id):
    """Add a review for a completed booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if booking belongs to current user
    if booking.user_id != current_user.id:
        flash('You do not have permission to review this booking!', 'danger')
        return redirect(url_for('booking.my_bookings'))
    
    # Check if booking is completed
    if not booking.is_completed():
        flash('You can only review completed bookings!', 'danger')
        return redirect(url_for('booking.my_bookings'))
    
    # Check if user has already reviewed this booking
    existing_review = Review.query.filter_by(
        user_id=current_user.id,
        space_id=booking.space_id
    ).first()
    
    if existing_review:
        flash('You have already reviewed this space!', 'info')
        return redirect(url_for('space.detail', space_id=booking.space_id))
    
    if request.method == 'POST':
        rating = int(request.form.get('rating'))
        comment = request.form.get('comment')
        
        if not 1 <= rating <= 5:
            flash('Rating must be between 1 and 5!', 'danger')
            return redirect(url_for('booking.review', booking_id=booking_id))
        
        new_review = Review(
            user_id=current_user.id,
            space_id=booking.space_id,
            rating=rating,
            comment=comment
        )
        
        db.session.add(new_review)
        db.session.commit()
        
        flash('Your review has been submitted!', 'success')
        return redirect(url_for('space.detail', space_id=booking.space_id))
    
    return render_template('pages/reviews/create.html', booking=booking)