from flask import Flask
from flask_cors import CORS
from api.chat_routes import chat_bp

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for the React frontend running on port 5173
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix='/api/chat')

    @app.route('/')
    def health_check():
        return {"status": "ok", "message": "PromptGate Backend is running!"}

    return app

if __name__ == '__main__':
    app = create_app()
    # Run the server on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
