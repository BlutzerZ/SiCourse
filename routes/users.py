from models import User as UserModel, Course as CourseModel, Enrollment as EnrollmentModel
from flask import render_template, request, session, redirect, abort, url_for, render_template
from app import app, db
from werkzeug.utils import secure_filename
import os
from pytz import timezone
from datetime import datetime

@app.before_request
def before_request():
    session.setdefault('role', None)
    session.setdefault('userID', None)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # get posted form
        fusername = request.form['uname']
        femail = request.form['email']
        fpassword = request.form['pwd']

        # query add user to db
        db_item = UserModel(
            username = fusername,
            email = femail,
            password = fpassword,
            role = "student"
        )
        db.session.add(db_item)
        db.session.commit()
        db.session.refresh(db_item)

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get posted form
        email = request.form['email']
        password = request.form['pwd']

        # query match
        user = UserModel.query.filter_by(email=email).first()
        if user and user.password == password:
            if user.role == 'admin':
                session['role'] = user.role
                session['userID'] = user.id
                return redirect(url_for('admin_home'))
            else:
                session['role'] = user.role
                session['userID'] = user.id
                return redirect(url_for('home'))
        else:
            return "failed to login"

    return render_template('login.html')

@app.route("/logout")
def admin_logout():
    session.pop('userID', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route("/")
def home():
    if session['role'] != "student":
        return redirect(url_for('login'))
    
    userItem = UserModel.query.get(session['userID'])

    courseItem = CourseModel.query.limit(6).all()
    for course in courseItem:
        utc_time = datetime.utcfromtimestamp(course.createdAt)
        jakarta_time = timezone('Asia/Jakarta').localize(utc_time)
        print("jakarta time: ", jakarta_time)
        course.createdAt = jakarta_time.strftime('%d %b %Y')
    return render_template('home.html', courses=courseItem, user=userItem)

@app.route("/edit-profile", methods=["GET", "POST"])
def profil():
    print(session['role'] != "student", session['role'] != "admin")
    if session['role'] != "student" and session['role'] != "admin":
        return redirect(url_for('login'))
    
    if request.method == "POST":
        # get form
        fusername = request.form['uname']
        femail = request.form['email']
        fpassword = request.form['pwd']

        # query db update
        user_item = UserModel.query.get(session['userID'])
        
        user_item.username = fusername
        user_item.email = femail
        user_item.password = fpassword

        db.session.commit()


        return render_template('update-profile.html', user=user_item)
    
    user_item = UserModel.query.get(session['userID'])

    return render_template('update-profile.html', user=user_item)

@app.route("/contact")
def about():
    if session['role'] != "student":
        return redirect(url_for('login'))
    
    user_item = UserModel.query.get(session['userID'])

    return render_template('contact.html', user=user_item)

@app.route("/course")
def show_all_course():
    if session['role'] != "student":
        return redirect(url_for('login'))
    
    userItem = UserModel.query.get(session['userID'])
    courses = CourseModel.query.all()

    for course in courses:
        utc_time = datetime.utcfromtimestamp(course.createdAt)
        jakarta_time = timezone('Asia/Jakarta').localize(utc_time)
        print("jakarta time: ", jakarta_time)
        course.createdAt = jakarta_time.strftime('%d %b %Y')
    return render_template('courses.html', courses=courses, user=userItem)

@app.route("/course/<int:course_id>")
def course_content(course_id):
    if session['role'] != "student":
        return redirect(url_for('login'))
    
    enrollmentCheck = EnrollmentModel.query.filter(EnrollmentModel.studentID == session['userID'],EnrollmentModel.courseID == course_id).first()
    if enrollmentCheck == None:
        enrollment = EnrollmentModel(
            studentID = session['userID'],
            courseID = course_id
        )
        db.session.add(enrollment)
        db.session.commit()
        db.session.refresh(enrollment)

    enrollemnt = EnrollmentModel.query.filter(EnrollmentModel.studentID == session['userID'],EnrollmentModel.courseID == course_id).first()
    userItem = UserModel.query.get(session['userID'])
    courseContent = CourseModel.query.get(course_id)
    courseContent.content = courseContent.content.split("\n")

    utc_time = datetime.utcfromtimestamp(courseContent.createdAt)
    jakarta_time = timezone('Asia/Jakarta').localize(utc_time)
    courseContent.createdAt = jakarta_time.strftime('%d %b %Y')


    return render_template('course-content.html', course=courseContent, user=userItem, enrollment=enrollemnt)

@app.route("/course/<int:course_id>/upload", methods=["POST"])
def course_upload(course_id):
    if session['role'] != "student":
        return redirect(url_for('login'))
    
    f = request.files['fimg']
    filename = secure_filename(f.filename)
    f.save(os.path.join('static', 'upload', 'images', filename))

    enrollment = EnrollmentModel.query.filter_by(courseID=course_id, studentID=session['userID']).first()
    enrollment.filename = filename
    db.session.commit()    

    return redirect(url_for('course_content', course_id=course_id))