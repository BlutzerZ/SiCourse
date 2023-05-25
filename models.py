import time
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(10), nullable=False)
    createdAt = db.Column(db.Integer, default=time.time())

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    thumbnail = db.Column(db.String(100))
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    createdAt = db.Column(db.Integer, default=time.time())
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    studentID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    courseID = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    filename = db.Column(db.String(100))
    completed = db.Column(db.Boolean, default=False)

    studentDetail = db.relationship('User', backref='enrollment', foreign_keys=[studentID])

    courseDetail = db.relationship('Course', backref='enrollment', foreign_keys=[courseID])