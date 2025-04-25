from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt,bcrypt
from .models import Doctor

def create_app():
    app  = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    #create database tables
    with app.app_context():
        db.create_all()

        #check if there is any doctor in the database.
        if not Doctor.query.first():
            hashed_password = bcrypt.generate_password_hash("Doctor@123").decode('utf-8')

            #add the default doctor
            default_doctor = Doctor(
                username = "Doctor",
                password = hashed_password
            )
            db.session.add(default_doctor)
            db.session.commit()

    return app