import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
import sqlite3
from datetime import datetime
import json

# Import our modules
from models import db, User, Detection, WeatherQuery, ChatHistory, CropCareQuery
from plant_disease_model import load_model, preprocess_image, predict_disease
from gemini_chat import get_ai_response
from weather_service import get_weather_data

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plant_disease_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Load ML model and crop care data
disease_model = None
crop_care_data = {}

def init_app():
    """Initialize the application"""
    global disease_model, crop_care_data
    
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Create demo users
        create_demo_users()
        
        # Load ML model
        disease_model = load_model()
        
        # Load crop care data
        try:
            with open('crop_care_data.json', 'r') as f:
                crop_care_data = json.load(f)
        except FileNotFoundError:
            logging.warning("crop_care_data.json not found")
            crop_care_data = {}
        
        # Create upload directory
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def create_demo_users():
    """Create demo users for testing"""
    demo_users = [
        ('farmer1', 'farmer1@example.com', 'password123'),
        ('demo', 'demo@example.com', 'demo123'),
        ('gardener', 'gardener@example.com', 'garden123')
    ]
    
    for username, email, password in demo_users:
        if not User.query.filter_by(username=username).first():
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )
            db.session.add(user)
    
    db.session.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user statistics
    detection_count = Detection.query.filter_by(user_id=current_user.id).count()
    weather_count = WeatherQuery.query.filter_by(user_id=current_user.id).count()
    chat_count = ChatHistory.query.filter_by(user_id=current_user.id).count()
    crop_care_count = CropCareQuery.query.filter_by(user_id=current_user.id).count()
    
    # Get recent detections
    recent_detections = Detection.query.filter_by(user_id=current_user.id)\
        .order_by(Detection.detected_at.desc()).limit(5).all()
    
    stats = {
        'detections': detection_count,
        'weather_queries': weather_count,
        'chat_messages': chat_count,
        'crop_care_queries': crop_care_count
    }
    
    return render_template('dashboard.html', stats=stats, recent_detections=recent_detections)

@app.route('/detect', methods=['GET', 'POST'])
@login_required
def detect():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return render_template('detect.html')
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return render_template('detect.html')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename or "")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Process image
                image = Image.open(filepath)
                processed_image = preprocess_image(image)
                
                if processed_image is not None and disease_model is not None:
                    # Make prediction
                    prediction = predict_disease(disease_model, processed_image)
                    
                    # Save detection to database
                    detection = Detection()
                    detection.user_id = current_user.id
                    detection.disease_name = prediction['disease']
                    detection.confidence = prediction['confidence']
                    detection.treatment = prediction['treatment']
                    detection.image_path = filename
                    db.session.add(detection)
                    db.session.commit()
                    
                    return render_template('detect.html', prediction=prediction, image_path=filename)
                else:
                    flash('Error processing image', 'error')
            except Exception as e:
                logging.error(f"Error during prediction: {e}")
                flash('Error analyzing image. Please try again.', 'error')
    
    return render_template('detect.html')

@app.route('/crop-care')
@login_required
def crop_care():
    return render_template('crop_care.html', crops=crop_care_data)

@app.route('/crop-care/<crop_name>')
@login_required
def crop_detail(crop_name):
    if crop_name in crop_care_data:
        # Log query
        query = CropCareQuery()
        query.user_id = current_user.id
        query.crop_type = crop_name
        db.session.add(query)
        db.session.commit()
        
        crop_info = crop_care_data[crop_name]
        return render_template('crop_care.html', crop_name=crop_name, crop_info=crop_info, crops=crop_care_data)
    else:
        flash('Crop information not found', 'error')
        return redirect(url_for('crop_care'))

@app.route('/weather', methods=['GET', 'POST'])
@login_required
def weather():
    weather_data = None
    if request.method == 'POST':
        location = request.form.get('location')
        if location:
            weather_data = get_weather_data(location)
            if weather_data:
                # Log query
                query = WeatherQuery()
                query.user_id = current_user.id
                query.location = location
                db.session.add(query)
                db.session.commit()
            else:
                flash('Weather data not available for this location', 'error')
    
    return render_template('weather.html', weather_data=weather_data)

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    chat_history = ChatHistory.query.filter_by(user_id=current_user.id)\
        .order_by(ChatHistory.created_at.desc()).limit(20).all()
    
    if request.method == 'POST':
        user_message = request.form.get('message')
        if user_message:
            ai_response = get_ai_response(user_message)
            
            # Save to database
            chat = ChatHistory()
            chat.user_id = current_user.id
            chat.user_message = user_message
            chat.ai_response = ai_response
            db.session.add(chat)
            db.session.commit()
            
            return redirect(url_for('chat'))
    
    return render_template('chat.html', chat_history=reversed(chat_history))

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize the app
init_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
