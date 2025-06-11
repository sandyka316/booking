from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from datetime import datetime
from app.config import Config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.space import space
    from app.routes.booking import booking
    from app.routes.review import review
    from app.routes.admin import admin
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(space)
    app.register_blueprint(booking)
    app.register_blueprint(review)
    app.register_blueprint(admin)
    
    # Create instance folder for SQLite
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Ensure parent directory for database exists
    db_path = os.path.join(app.instance_path, 'bookspace.db')
    db_dir = os.path.dirname(db_path)
    os.makedirs(db_dir, exist_ok=True)
    
    # Context processors
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
        
    @app.context_processor
    def utility_processor():
        def format_price(amount):
            return f"${amount:.2f}"
        return dict(format_price=format_price)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    @app.after_request
    def add_header(response):
        # Prevent cache for development
        if app.debug:
            response.headers['Cache-Control'] = 'no-store'
        return response
    
    return app