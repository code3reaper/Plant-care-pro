from app import app

if __name__ == '__main__':
    print("🌱 Starting Plant Disease Detection System...")
    print("📱 Application will be available at: http://localhost:5000")
    print("🔐 Demo login: farmer1 / password123")
    print("=" * 50)
    
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000, debug=True)
