from flask import redirect, render_template
from flask_jwt_extended import jwt_required

def app_routes(app):
    @app.route('/')
    def home():
        return redirect('/login')

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/dashboard')
    @jwt_required()
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/clients')
    @jwt_required()
    def clients_page():
        return render_template('clients.html')

    @app.route('/programs')
    @jwt_required()
    def programs_page():
        return render_template('programs.html')
