from app import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey('spaces.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmed')  # 'confirmed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def __init__(self, user_id, space_id, start_time, end_time, total_price, status='confirmed', notes=None):
        self.user_id = user_id
        self.space_id = space_id
        self.start_time = start_time
        self.end_time = end_time
        self.total_price = total_price
        self.status = status
        self.notes = notes
        
    def duration_hours(self):
        """Calculate booking duration in hours"""
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600
    
    def is_upcoming(self):
        """Check if booking is in the future"""
        return self.start_time > datetime.utcnow()
    
    def is_active(self):
        """Check if booking is currently active"""
        now = datetime.utcnow()
        return self.start_time <= now and self.end_time >= now and self.status == 'confirmed'
    
    def is_completed(self):
        """Check if booking is completed"""
        return self.end_time < datetime.utcnow() and self.status == 'confirmed'
    
    def can_be_cancelled(self):
        """Check if booking can be cancelled (only future bookings)"""
        return self.is_upcoming() and self.status == 'confirmed'
    
    def __repr__(self):
        return f'<Booking {self.id}: {self.space_id} by User {self.user_id}>'