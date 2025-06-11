from flask import Blueprint, render_template, request, current_app
from app.models import Space, Review
from app import db
from sqlalchemy import func

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Homepage showing featured spaces and statistics"""
    # Get top rated spaces
    top_spaces = db.session.query(
        Space,
        func.avg(Review.rating).label('avg_rating')
    ).join(
        Review, Space.id == Review.space_id, isouter=True
    ).group_by(
        Space.id
    ).order_by(
        func.avg(Review.rating).desc()
    ).limit(4).all()
    
    # Get spaces by location for quick search
    locations = db.session.query(Space.location, func.count(Space.id)).group_by(Space.location).all()
    
    return render_template('pages/index.html', top_spaces=top_spaces, locations=locations)

@main.route('/about')
def about():
    """About page with information about BookSpace"""
    return render_template('pages/about.html')

@main.route('/contact')
def contact():
    """Contact page"""
    return render_template('pages/contact.html')

@main.route('/faq')
def faq():
    """Frequently Asked Questions page"""
    return render_template('pages/faq.html')

@main.route('/terms')
def terms():
    """Terms and Conditions page"""
    return render_template('pages/terms.html')

@main.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('pages/privacy.html')