from flask import Flask, jsonify
from config import Config
from extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Import models so they are registered with SQLAlchemy
    import models

    @app.route('/api/health')
    def health_check():
        return jsonify({"status": "ok", "message": "UMS Backend is running."})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
