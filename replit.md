# Plant Care Pro - AI-Powered Plant Disease Detection System

## Overview

Plant Care Pro is a comprehensive Flask web application that provides AI-powered plant disease detection, real-time weather integration, and agricultural assistance. The system combines computer vision, machine learning, and external APIs to deliver a complete farming and gardening solution.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular monolithic architecture with clear separation of concerns:

- **Frontend**: Bootstrap 5-based responsive web interface with custom styling and JavaScript interactions
- **Backend**: Python Flask framework with SQLAlchemy ORM for database operations
- **Machine Learning**: TensorFlow/Keras CNN model for plant disease classification (37+ disease types)
- **AI Integration**: Google Gemini API for conversational agricultural assistance
- **Weather Service**: OpenWeatherMap API for real-time weather data and farming recommendations
- **Authentication**: Flask-Login with session-based user management and password hashing
- **Database**: SQLite for lightweight, file-based data storage

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Central Flask application controller and route handler
- **Responsibilities**: Request routing, session management, file uploads, API integration
- **Architecture Decision**: Single-file Flask app chosen for simplicity while maintaining modularity through imported services

### 2. Database Models (`models.py`)
- **Purpose**: SQLAlchemy ORM models for data persistence
- **Components**: User, Detection, WeatherQuery, ChatHistory, CropCareQuery entities
- **Architecture Decision**: SQLAlchemy ORM provides database abstraction and easy migration capabilities

### 3. Plant Disease Detection (`plant_disease_model.py`)
- **Purpose**: Machine learning pipeline for image-based disease identification
- **Components**: CNN model wrapper, image preprocessing, confidence scoring, treatment recommendations
- **Architecture Decision**: Separate module enables independent ML model updates and testing

### 4. AI Chat Assistant (`gemini_chat.py`)
- **Purpose**: Conversational AI for agricultural guidance using Google Gemini
- **Components**: API client, agricultural prompt engineering, response processing
- **Architecture Decision**: External AI service provides expert knowledge without local model complexity

### 5. Weather Service (`weather_service.py`)
- **Purpose**: Real-time weather data and agricultural recommendations
- **Components**: OpenWeatherMap API integration, forecast processing, farming advice generation
- **Architecture Decision**: Third-party weather service ensures accuracy and reliability

### 6. Static Content Management
- **Crop Care Data**: JSON-based crop information for planting, care, and harvesting guidance
- **Frontend Assets**: Bootstrap theme, custom CSS, and JavaScript for enhanced user experience

## Data Flow

1. **User Authentication**: Session-based login with password hashing and user management
2. **Image Upload**: Secure file handling with validation and preprocessing for ML inference
3. **Disease Detection**: CNN model processes images and returns classification with confidence scores
4. **Weather Queries**: Location-based API calls retrieve current conditions and forecasts
5. **AI Chat**: Natural language processing through Gemini API with agricultural context
6. **Data Persistence**: All user activities logged to SQLite database for history and analytics

## External Dependencies

### APIs and Services
- **Google Gemini AI**: Conversational agricultural assistance with expert knowledge
- **OpenWeatherMap**: Real-time weather data and 5-day forecasts for farming decisions
- **TensorFlow**: Machine learning framework for plant disease classification

### Python Libraries
- **Flask**: Web framework with SQLAlchemy for database operations
- **Flask-Login**: User session management and authentication
- **Werkzeug**: Password hashing and file upload security
- **PIL (Pillow)**: Image processing and manipulation
- **Requests**: HTTP client for external API calls

### Frontend Technologies
- **Bootstrap 5**: Responsive CSS framework with dark theme support
- **Font Awesome**: Icon library for enhanced UI
- **Custom CSS/JS**: Enhanced user interactions and styling

## Deployment Strategy

### Development Environment
- **Database**: SQLite for zero-configuration development
- **File Storage**: Local filesystem for uploaded images
- **Configuration**: Environment variables for API keys and secrets

### Production Considerations
- **Database**: SQLite provides reliable file-based storage suitable for the application's needs
- **File Storage**: Consider cloud storage (S3, etc.) for uploaded images
- **Security**: HTTPS enforcement, secure session configuration, input validation
- **Scaling**: Container deployment with load balancing for high availability

### Environment Configuration
- **API Keys**: Secure storage of Gemini and OpenWeatherMap credentials
- **Session Security**: Configurable secret keys for production deployment
- **Upload Limits**: File size restrictions and validation for security

The system is designed for easy deployment while maintaining flexibility for future enhancements and scaling requirements.