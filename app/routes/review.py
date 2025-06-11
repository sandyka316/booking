from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Space, Review
from app import db

review = Blueprint('review', __name__)

@review.route('/spaces/<int:space_id>/reviews')
def index(space_id):
    """Show all reviews for a specific space"""
    space = Space.query.get_or_404(space_id)
    reviews = Review.query.filter_by(space_id=space_id).order_by(Review.created_at.desc()).all()
    
    return render_template('pages/reviews/index.html', space=space, reviews=reviews)

@review.route('/reviews/<int:review_id>/delete', methods=['POST'])
@login_required
def delete(review_id):
    """Delete a review (admin or owner only)"""
    review = Review.query.get_or_404(review_id)
    
    # Check if user has permission to delete
    if review.user_id != current_user.id and not current_user.is_admin():
        flash('You do not have permission to delete this review!', 'danger')
        return redirect(url_for('review.index', space_id=review.space_id))
    
    db.session.delete(review)
    db.session.commit()
    
    flash('Review successfully deleted!', 'success')
    return redirect(url_for('review.index', space_id=review.space_id))