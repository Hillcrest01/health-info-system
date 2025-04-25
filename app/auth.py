from flask import request, jsonify
from flask_jwt_extended import create_access_token
from .models import Doctor
from .extensions import bcrypt

def auth_routes(app):
    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()
        doctor = Doctor.query.filter_by(username=data.get('username')).first()

        if not doctor or not bcrypt.check_password_hash(doctor.password, data.get('password')):
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(identity=doctor)
        return jsonify(access_token=access_token)
    