from app import db
from datetime import datetime

class Space(db.Model):
    __tablename__ = 'spaces'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    amenities = db.Column(db.Text)  # Stored as JSON string
    is_available = db.Column(db.Boolean, default=True)
    
    # Relationships
    bookings = db.relationship('Booking', backref='space', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='space', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, name, location, capacity, price_per_hour, description=None, image_url=None, amenities=None):
        self.name = name
        self.location = location
        self.capacity = capacity
        self.price_per_hour = price_per_hour
        self.description = description
        self.image_url = image_url
        self.amenities = amenities
        
    def calculate_average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)
    
    def is_available_at(self, start_time, end_time):
        """Check if space is available for booking at the specified time range"""
        overlapping_bookings = Booking.query.filter(
            Booking.space_id == self.id,
            Booking.status == 'confirmed',
            Booking.start_time < end_time,
            Booking.end_time > start_time
        ).first()
        return overlapping_bookings is None
    
    def __repr__(self):
        return f'<Space {self.name} at {self.location}>'