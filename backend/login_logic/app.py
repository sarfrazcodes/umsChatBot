from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import sys
import os

# Add backend directory to sys.path so we can import extensions, config, and services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from extensions import db
from config import Config
from services.action_router import handle_user_query

app = Flask(__name__)
CORS(app) # Enable CORS for frontend communication

# Configuration
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Dummy database for simple demonstration (JSON/Dict)
# Pre-populated with the starting user
users_db = {
    "12505649": bcrypt.generate_password_hash("hackthon@123").decode('utf-8')
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    registration_number = data.get('registration_number')
    password = data.get('password')

    if not registration_number or not password:
        return jsonify({"msg": "Missing registration number or password"}), 400

    # Retrieve hashed password from DB
    hashed_password = users_db.get(registration_number)
    
    # Verify the password using bcrypt
    if not hashed_password or not bcrypt.check_password_hash(hashed_password, password):
        return jsonify({"msg": "Bad registration number or password"}), 401

    # Create JWT token
    access_token = create_access_token(identity=registration_number)
    return jsonify({"access_token": access_token, "msg": "Login successful"}), 200

@app.route('/api/chat', methods=['POST'])
@jwt_required()
def chat():
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({"response": "Please provide a message."}), 400
        
    registration_number = get_jwt_identity()
    
    # Send directly to the UMS Action Router
    response_text = handle_user_query(message, registration_number)
    
    return jsonify({"response": response_text})

@app.route('/api/dashboard', methods=['GET'])
@jwt_required()
def dashboard_data():
    registration_number = get_jwt_identity()
    
    # Import services dynamically or globally
    from services.academic_service import get_profile
    from services.attendance_service import get_overall_attendance
    from services.timetable_service import get_todays_timetable
    from services.rms_service import check_rms_status
    
    profile = get_profile(registration_number)
    attendance = get_overall_attendance(registration_number)
    timetable = get_todays_timetable(registration_number)
    rms = check_rms_status(registration_number, limit=100)
    
    return jsonify({
        "profile": profile,
        "attendance": attendance,
        "timetable": timetable,
        "rms": rms
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
