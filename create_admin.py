from app import db, create_app
from app.models import User
from app.config import Config

app = create_app(Config)

with app.app_context():
    # Cek apakah admin sudah ada
    admin = User.query.filter_by(email='admin@bookspace.com').first()
    
    if not admin:
        # Buat user admin baru
        admin = User(
            username='s',
            email='s@gmail.com',
            password='s',
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists!")