from flask import request, jsonify
from flask_jwt_extended import jwt_required
from .models import db, Program, Client, Enrollment
from datetime import datetime

def api_routes(app):
    # HEALTH PROGRAMS 
    @app.route('/api/programs', methods=['POST'])
    @jwt_required()
    def create_program():
        data = request.get_json()
        if not data.get('name'):
            return jsonify({"error": "Program name is required"}), 400
            
        program = Program(
            name=data['name'],
            description=data.get('description', '')
        )
        db.session.add(program)
        db.session.commit()
        return jsonify({
            "id": program.id,
            "name": program.name,
            "message": "Program created successfully"
        }), 201

    @app.route('/api/programs', methods=['GET'])
    def get_programs():
        programs = Program.query.all()
        return jsonify([{
            "id": p.id,
            "name": p.name,
            "description": p.description
        } for p in programs])

    #  CLIENTS 
    @app.route('/api/clients', methods=['POST'])
    @jwt_required()
    def create_client():
        data = request.get_json()
        required_fields = ['name', 'gender', 'age']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        client = Client(
            name=data['name'],
            gender=data['gender'],
            age=data['age']
        )
        db.session.add(client)
        db.session.commit()
        return jsonify({
            "id": client.id,
            "message": "Client registered successfully"
        }), 201

    @app.route('/api/clients', methods=['GET'])
    def get_clients():
        # Search functionality
        name = request.args.get('name')
        age = request.args.get('age')
        
        query = Client.query
        if name:
            query = query.filter(Client.name.ilike(f"%{name}%"))
        if age:
            query = query.filter_by(age=age)
            
        clients = query.all()
        return jsonify([{
            "id": c.id,
            "name": c.name,
            "age": c.age,
            "gender": c.gender
        } for c in clients])

    # --- ENROLLMENTS ---
    @app.route('/api/enrollments', methods=['POST'])
    @jwt_required()
    def enroll_client():
        data = request.get_json()
        required_fields = ['client_id', 'program_id']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing client_id or program_id"}), 400

        enrollment = Enrollment(
            client_id=data['client_id'],
            program_id=data['program_id'],
            notes=data.get('notes', ''),
            enrolled_at=datetime.utcnow()
        )
        db.session.add(enrollment)
        db.session.commit()
        return jsonify({
            "id": enrollment.id,
            "message": "Client enrolled successfully"
        }), 201

    # --- CLIENT PROFILE ---
    @app.route('/api/clients/<int:client_id>', methods=['GET'])
    def get_client_profile(client_id):
        client = Client.query.get_or_404(client_id)
        enrollments = Enrollment.query.filter_by(client_id=client_id).all()
        
        return jsonify({
            "client": {
                "id": client.id,
                "name": client.name,
                "age": client.age,
                "gender": client.gender,
                "registered_at": client.created_at.isoformat()
            },
            "enrollments": [{
                "program_id": e.program_id,
                "program_name": e.program.name,
                "enrolled_at": e.enrolled_at.isoformat(),
                "notes": e.notes
            } for e in enrollments]
        })

    # --- PROGRAM ENROLLMENTS ---
    @app.route('/api/programs/<int:program_id>/clients', methods=['GET'])
    def get_program_enrollments(program_id):
        enrollments = Enrollment.query.filter_by(program_id=program_id).all()
        return jsonify([{
            "client_id": e.client_id,
            "client_name": e.client.name,
            "enrolled_at": e.enrolled_at.isoformat()
        } for e in enrollments])


    @app.route('/api/clients/search', methods=['GET'])
    def search_clients():
     """
     Search clients with multiple filters
     Example: /api/clients/search?name=John&age=30&gender=male&program=HIV
     """
      # Get query parameters
     name = request.args.get('name')
     age = request.args.get('age')
     gender = request.args.get('gender')
     program_name = request.args.get('program')

     # Build query
     query = Client.query
    
     if name:
         query = query.filter(Client.name.ilike(f'%{name}%'))
     if age:
        query = query.filter_by(age=age)
     if gender:
        query = query.filter_by(gender=gender.lower())
     if program_name:
          query = query.join(Enrollment).join(Program).filter(
            Program.name.ilike(f'%{program_name}%')
        )

    # Execute and format results
     clients = query.all()
     return jsonify([{
        'id': c.id,
        'name': c.name,
        'age': c.age,
        'gender': c.gender,
        'programs': [e.program.name for e in c.enrollments]
    } for c in clients])
    