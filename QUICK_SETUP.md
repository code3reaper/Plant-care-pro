# Quick Setup Guide - Plant Care Pro on VS Code

## What You Need First
1. **Python 3.11+** - Download from [python.org](https://www.python.org/downloads/)
2. **VS Code** - Download from [code.visualstudio.com](https://code.visualstudio.com/)
3. **Gemini API Key** - Get free from [ai.google.dev](https://ai.google.dev/) (takes 2 minutes)

## Simple 5-Step Setup

### Step 1: Create Project Folder
```bash
mkdir plant-care-pro
cd plant-care-pro
```

### Step 2: Download All Files
Download these files from your Replit project and put them in the `plant-care-pro` folder:

**Main Files:**
- `app.py`
- `main.py`
- `models.py`
- `plant_disease_model.py`
- `gemini_chat.py`
- `weather_service.py`
- `crop_care_data.json`
- `local_requirements.txt` (rename to `requirements.txt`)

**Create folders and download:**
- `templates/` folder with all `.html` files
- `static/css/` folder with `style.css`
- `static/js/` folder with `app.js`
- Create empty `static/uploads/` folder

### Step 3: Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install everything
pip install -r requirements.txt
```

### Step 4: Create Environment File
Create `.env` file in your project folder:
```env
FLASK_APP=main.py
FLASK_ENV=development
SESSION_SECRET=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key-here
OPENWEATHER_API_KEY=64938d187da356d6f4b298eec9118b32
```

**Important:** Replace `your-gemini-api-key-here` with your actual Gemini API key from [ai.google.dev](https://ai.google.dev/)

### Step 5: Add Environment Loading to app.py
Add these 2 lines at the top of `app.py` (after the existing imports):
```python
from dotenv import load_dotenv
load_dotenv()
```

## Run the Project

### Option 1: Simple Run
```bash
python main.py
```

### Option 2: VS Code Debug
1. Open the folder in VS Code
2. Press `F5` to debug
3. Choose "Python File" if asked

## Access Your App
Open browser: `http://localhost:5000`

## Your Project Structure Should Look Like This:
```
plant-care-pro/
├── app.py
├── main.py
├── models.py
├── plant_disease_model.py
├── gemini_chat.py
├── weather_service.py
├── crop_care_data.json
├── requirements.txt
├── .env
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── detect.html
│   ├── chat.html
│   ├── crop_care.html
│   └── weather.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── uploads/
└── venv/
```

## Common Issues & Solutions

**Error: Module not found**
- Make sure virtual environment is activated: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)

**Error: API Key issues**
- Check your `.env` file has the correct Gemini API key
- Make sure you added the `load_dotenv()` lines to `app.py`

**Error: Port already in use**
- In `main.py`, change port: `app.run(host='0.0.0.0', port=5001, debug=True)`

**Error: Templates not found**
- Make sure all HTML files are in `templates/` folder
- Check file names match exactly

## Test Everything Works
1. Go to `http://localhost:5000`
2. Register a new account
3. Try plant disease detection (upload any plant image)
4. Test AI chat with questions like "How to grow tomatoes?"
5. Check weather for your city
6. Browse crop care information

That's it! Your Plant Care Pro app should work exactly like it does here on Replit.