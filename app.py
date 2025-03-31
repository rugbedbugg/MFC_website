from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from sqlalchemy.exc import IntegrityError
import os
import sys
from config import Config
from services.spycloud_service import SpyCloudService

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

app = Flask(__name__)
app.config.from_object(Config)

# Ensure the instance folder exists
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)

# Configure SQLAlchemy with absolute path
db_path = os.path.join(instance_path, 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db = SQLAlchemy(app)

# User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)

# Create the database and tables
def init_db():
    try:
        with app.app_context():
            db.create_all()
            logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Error initializing database: {str(e)}")
        raise

init_db()

# Initialize SpyCloud service
spycloud_service = SpyCloudService()

# Base route (redirect to login if not logged in)
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        logging.info(f"Attempting to create user with email: {email}")
        try:
            hashed_password = generate_password_hash(password, method='sha256')
            logging.info("Password hashed successfully")
            
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                logging.info(f"User with email {email} already exists")
                flash('Email already exists. Please log in.')
                return redirect(url_for('login'))
            
            new_user = User(email=email, password=hashed_password)
            logging.info("New user object created")
            
            db.session.add(new_user)
            logging.info("User added to session")
            
            db.session.commit()
            logging.info("Changes committed to database")
            
            flash('Account created successfully! Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error during signup: {str(e)}")
            logging.error(f"Error type: {type(e)}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
            flash('An unexpected error occurred. Please try again.')
    return render_template('signup.html')

# Threat Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('login'))
    
    try:
        # Get current user's email
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found. Please log in again.')
            return redirect(url_for('login'))
        
        # Fetch breach and exposure data
        breach_data = spycloud_service.get_breach_data(user.email)
        exposure_data = spycloud_service.get_exposure_data(user.email)
        
        # Process and format the data
        threats = []
        for breach in breach_data:
            threats.append({
                "date": breach.get('date', 'Unknown'),
                "description": f"Data breach detected in {breach.get('source', 'Unknown source')}",
                "severity": breach.get('severity', 'Medium')
            })
        
        # Add exposure data
        if exposure_data:
            for exposure in exposure_data.get('exposures', []):
                threats.append({
                    "date": exposure.get('date', 'Unknown'),
                    "description": f"Data exposure detected: {exposure.get('type', 'Unknown type')}",
                    "severity": exposure.get('severity', 'High')
                })
        
        return render_template('dashboard.html', threats=threats)
        
    except Exception as e:
        logging.error(f"Error in dashboard: {str(e)}")
        flash('An error occurred while loading the dashboard. Please try again.')
        return render_template('dashboard.html', threats=[])

# Breach Checker route
@app.route('/breach_checker', methods=['GET', 'POST'])
def breach_checker():
    if 'user_id' not in session:
        flash('Please log in to access the breach checker.')
        return redirect(url_for('login'))
    breaches = []
    if request.method == 'POST':
        query = request.form.get('query')
        if query == "test@example.com":
            breaches = ["Breach 1: Data leaked on 2023-05-01"]
        else:
            breaches = ["No breaches found"]
    return render_template('breach_checker.html', breaches=breaches)

# About Us route
@app.route('/about')
def about():
    return render_template('about.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Profile route
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in to access your profile.')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found. Please log in again.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            # Update user information
            user.first_name = request.form.get('first_name')
            user.last_name = request.form.get('last_name')
            
            # Only update password if a new one is provided
            new_password = request.form.get('password')
            if new_password:
                user.password = generate_password_hash(new_password, method='sha256')
            
            db.session.commit()
            flash('Profile updated successfully!')
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating profile: {str(e)}")
            flash('An error occurred while updating your profile.')
    
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
