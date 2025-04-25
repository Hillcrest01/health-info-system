from datetime import datetime
from .extensions import db

#Doctors table code
class Doctor(db.Model):
    __table_name__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

#Clients Table
class Client(db.Model):
    id  = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable  = False)
    gender = db.Column(db.String(10) , nullable = False)
    age = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

#Program Table
class Program(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100) , nullable = False)
    description = db.Column(db.text)

#Enrollment table to ensure the many-many relationship between clients and programs
class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    client_id = db.Column(db.Integer, db.ForeignKey('client_id'), nullable = False)
    program_id = db.Column(db.Integer, db.ForeignKey('program_id') , nullable=False)
    enrolled_at = db.Column(db.DateTime, default = datetime.utcnow)
    notes = db.Column(db.Text)

    #Relationships
    client = db.relationship('Client' , backref = 'enrollments')
    program = db.relationship('Program' , backref = "enrollments")