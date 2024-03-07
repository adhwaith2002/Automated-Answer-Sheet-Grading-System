from . import db 
from flask_login import UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


 

class Student(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Studentname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    register_number = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    sex = db.Column(db.String(200), nullable=False)
    semester = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Integer)
    
class Teacher(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Teachername = db.Column(db.String(200), nullable=False)
    Email = db.Column(db.String(200), unique=True, nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    sex = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Integer)

class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Adminname = db.Column(db.String(200), nullable=False)
    Email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


    






