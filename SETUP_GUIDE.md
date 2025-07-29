# Plant Care Pro - VS Code Setup Guide

## Prerequisites

Before setting up the project, make sure you have the following installed on your laptop:

### 1. Python 3.11+
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: Use Homebrew: `brew install python@3.11` or download from python.org
- **Linux**: `sudo apt install python3.11 python3.11-pip python3.11-venv`

### 2. VS Code
- Download from [code.visualstudio.com](https://code.visualstudio.com/)
- Install the Python extension by Microsoft

### 3. Git (optional but recommended)
- **Windows**: Download from [git-scm.com](https://git-scm.com/)
- **macOS**: Use Homebrew: `brew install git`
- **Linux**: `sudo apt install git`

## Setup Instructions

### Step 1: Create Project Directory
```bash
# Create a new directory for your project
mkdir plant-care-pro
cd plant-care-pro
```

### Step 2: Download Project Files
Download all the following files from your Replit project and place them in the `plant-care-pro` directory:

**Python Files:**
- `app.py` (main Flask application)
- `models.py` (database models)
- `plant_disease_model.py` (ML model handling)
- `gemini_chat.py` (AI chat functionality)
- `weather_service.py` (weather API integration)
- `main.py` (application entry point)

**Data Files:**
- `crop_care_data.json` (crop information database)

**Template Files (create `templates/` folder):**
- `templates/base.html`
- `templates/index.html`
- `templates/login.html`
- `templates/register.html`
- `templates/dashboard.html`
- `templates/detect.html`
- `templates/chat.html`
- `templates/crop_care.html`
- `templates/weather.html`

**Static Files (create `static/` folder):**
- `static/css/style.css`
- `static/js/app.js`
- Create empty `static/uploads/` folder

### Step 3: Set Up Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 4: Install Dependencies
Create a `requirements.txt` file with the following content:
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
Pillow==10.1.0
requests==2.31.0
google-genai==0.3.0
tensorflow==2.15.0
numpy==1.24.3
gunicorn==21.2.0
```

Then install the dependencies:
```bash
pip install -r requirements.txt
```

### Step 5: Set Up Environment Variables
Create a `.env` file in your project root:
```env
# Flask Configuration
FLASK_APP=main.py
FLASK_ENV=development
SESSION_SECRET=your-secret-key-change-this-in-production

# API Keys
GEMINI_API_KEY=your-gemini-api-key-here
OPENWEATHER_API_KEY=your-openweather-api-key-here
```

**Important**: Replace the API keys with your actual keys:
- **Gemini API Key**: Get from [ai.google.dev](https://ai.google.dev/)
- **OpenWeather API Key**: Get from [openweathermap.org](https://openweathermap.org/api)

### Step 6: Install Python Extension for Environment Variables
```bash
pip install python-dotenv
```

### Step 7: Update app.py for Environment Variables
Add this to the top of your `app.py` file (after the imports):
```python
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
```

### Step 8: VS Code Configuration
Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/venv": true,
        "*.pyc": true
    }
}
```

Create `.vscode/launch.json` for debugging:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask App",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "env": {
                "FLASK_ENV": "development"
            },
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

## Running the Application

### Option 1: Using VS Code Terminal
1. Open VS Code in your project directory
2. Open the integrated terminal (Ctrl+` or View → Terminal)
3. Make sure your virtual environment is activated
4. Run the application:
```bash
python main.py
```

### Option 2: Using VS Code Debugger
1. Open `main.py` in VS Code
2. Press F5 or go to Run → Start Debugging
3. Select "Flask App" configuration

### Option 3: Using Flask Command
```bash
flask run --host=0.0.0.0 --port=5000 --debug
```

## Accessing the Application

Once running, open your web browser and go to:
- **Local access**: `http://localhost:5000`
- **Network access**: `http://your-laptop-ip:5000`

## Project Structure
```
plant-care-pro/
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── models.py             # Database models
├── plant_disease_model.py # ML model handling
├── gemini_chat.py        # AI chat functionality
├── weather_service.py    # Weather API integration
├── crop_care_data.json   # Crop information
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── .gitignore           # Git ignore file
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── detect.html
│   ├── chat.html
│   ├── crop_care.html
│   └── weather.html
├── static/              # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── uploads/         # Image uploads
├── venv/                # Virtual environment
└── .vscode/             # VS Code configuration
    ├── settings.json
    └── launch.json
```

## Troubleshooting

### Common Issues:

1. **Module not found errors**:
   - Make sure your virtual environment is activated
   - Install missing packages: `pip install package-name`

2. **API Key errors**:
   - Check your `.env` file has the correct API keys
   - Make sure python-dotenv is installed

3. **Database errors**:
   - Delete the existing database file if it exists
   - The app will create a new SQLite database automatically

4. **Port already in use**:
   - Change the port in `main.py`: `app.run(host='0.0.0.0', port=5001, debug=True)`

5. **Template not found**:
   - Make sure all template files are in the `templates/` folder
   - Check file names match exactly

## Additional VS Code Extensions (Recommended)

- Python (Microsoft) - Already mentioned
- Pylance (Microsoft) - Enhanced Python language support
- Python Docstring Generator - Auto-generate docstrings
- SQLite Viewer - View SQLite database files
- HTML CSS Support - Better HTML/CSS editing
- Bootstrap 5 Quick Snippets - Bootstrap code snippets

## Development Tips

1. **Auto-reload**: The app runs in debug mode, so changes are automatically reflected
2. **Database**: SQLite database file will be created automatically in your project root
3. **Uploads**: Images are stored in `static/uploads/` folder
4. **Logs**: Check the terminal for application logs and errors
5. **Environment**: Always activate your virtual environment before working

## Testing the Features

1. **User Registration**: Create a new account at `/register`
2. **Plant Disease Detection**: Upload plant images at `/detect`
3. **Weather Data**: Check weather information at `/weather`
4. **AI Chat**: Ask agricultural questions at `/chat`
5. **Crop Care**: Browse crop information at `/crop-care`

Your Plant Care Pro application should now be running successfully on your laptop with VS Code!