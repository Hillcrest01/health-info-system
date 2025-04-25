from flask import request, jsonify
from flask_jwt_extended import create_access_token
from .models import Doctor
from .extensions import bcrypt

def auth_routes(app):
    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()
        
        # Validate input
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Username and password required"}), 400

        # Find doctor
        doctor = Doctor.query.filter_by(username=data['username']).first()
        if not doctor:
            return jsonify({"error": "Invalid credentials"}), 401

        # Verify password
        if not bcrypt.check_password_hash(doctor.password, data['password']):
            return jsonify({"error": "Invalid credentials"}), 401

        # Create token with doctor's ID
        access_token = create_access_token(identity=str(doctor.id))
        return jsonify(access_token=access_token)