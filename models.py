from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    detections = db.relationship('Detection', backref='user', lazy=True)
    weather_queries = db.relationship('WeatherQuery', backref='user', lazy=True)
    chat_history = db.relationship('ChatHistory', backref='user', lazy=True)
    crop_care_queries = db.relationship('CropCareQuery', backref='user', lazy=True)

class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    disease_name = db.Column(db.String(200), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    treatment = db.Column(db.Text)
    image_path = db.Column(db.String(200))
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)

class WeatherQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    queried_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CropCareQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crop_type = db.Column(db.String(100), nullable=False)
    queried_at = db.Column(db.DateTime, default=datetime.utcnow)
