from datetime import datetime, time

def format_datetime(dt):
    """Format datetime for display"""
    return dt.strftime('%Y-%m-%d %H:%M')

def format_date(dt):
    """Format date for display"""
    return dt.strftime('%Y-%m-%d')

def format_time(dt):
    """Format time for display"""
    return dt.strftime('%H:%M')

def is_valid_time_range(start_time, end_time):
    """Check if a time range is valid"""
    return start_time < end_time

def generate_time_slots(start_hour=7, end_hour=22, interval=60):
    """Generate time slots for bookings"""
    slots = []
    current = start_hour
    
    while current < end_hour:
        slot_time = time(hour=current)
        slots.append(slot_time)
        current += interval // 60
        
    return slots