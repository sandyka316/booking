# BookSpace - Modern Co-working Space Reservation System

BookSpace is a full-stack web application that allows users to find, browse, and book co-working spaces. Built with Python 3.13 and Flask, it demonstrates modern web development practices and architecture.

## Features

- **User Authentication**: Secure registration and login system
- **Space Search & Filters**: Find spaces by location, capacity, and amenities
- **Booking System**: Real-time availability checking and booking management
- **Reviews & Ratings**: Leave and view ratings and reviews for spaces
- **Admin Dashboard**: Complete management interface for spaces, bookings, and users
- **Modern UI**: Clean, responsive design with light/dark mode support

## Tech Stack

- **Backend**: Python 3.13, Flask 3.0+
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5.3
- **Security**: Flask-Login, password hashing
- **Other**: Jinja2 templating, Chart.js for analytics

## Project Structure

```
bookspace/
├── app/                      # Main application package
│   ├── __init__.py           # App initialization
│   ├── config.py             # Configuration settings
│   ├── models/               # Database models
│   ├── routes/               # Route blueprints
│   ├── static/               # Static assets
│   ├── templates/            # Jinja2 templates
│   └── utils/                # Utility functions
├── migrations/               # Database migrations
├── tests/                    # Unit and integration tests
├── instance/                 # Instance-specific data
├── .env                      # Environment variables
├── requirements.txt          # Package dependencies
└── run.py                    # Application entry point
```

## Getting Started

1. **Clone the repository**:
   ```
   git clone https://github.com/sandy/booking.git
   cd bookspace
   ```

2. **Create and activate virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (create a .env file):
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   ```

5. **Run the application**:
   ```
   flask run
   ```

6. **Open in browser**:
   The application will be available at `http://127.0.0.1:5000/`

## Database Schema

- **User**: User accounts with authentication details
- **Space**: Available co-working spaces with details and amenities
- **Booking**: Reservations linking users to spaces
- **Review**: User reviews and ratings of spaces

## Testing

Run the test suite:
```
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.