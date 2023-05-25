from models import User as UserModel, Course as CourseModel, Enrollment as EnrollmentModel
from flask import render_template, request, session, redirect, abort, url_for, render_template
from app import app, db
import os
from werkzeug.utils import secure_filename
from pytz import timezone
from datetime import datetime

@app.route("/admin")
def admin_home():
    if session['role'] != "admin":
        return redirect(url_for('login'))
    userItem = UserModel.query.get(session['userID'])
    students = UserModel.query.all()

    courses = CourseModel.query.limit(6).all()

    for course in courses:
        utc_time = datetime.utcfromtimestamp(course.createdAt)
        jakarta_time = timezone('Asia/Jakarta').localize(utc_time)
        print("jakarta time: ", jakarta_time)
        course.createdAt = jakarta_time.strftime('%d %b %Y')

    return render_template("admin-home.html", courses=courses, user=userItem, totalCourse=len(courses), totalStudent=len(students)-1)
    
@app.route("/admin/course")
def admin_course():
    if session['role'] != "admin":
        return redirect(url_for('login'))

    userItem = UserModel.query.get(session['userID'])
    courses = CourseModel.query.all()

    for course in courses:
        utc_time = datetime.utcfromtimestamp(course.createdAt)
        jakarta_time = timezone('Asia/Jakarta').localize(utc_time)
        print("jakarta time: ", jakarta_time)
        course.createdAt = jakarta_time.strftime('%d %b %Y')
    return render_template('admin-course.html', courses=courses, user=userItem)

@app.route("/admin/course/create", methods=["GET", "POST"])
def admin_course_create():
    if session['role'] != "admin":
        return redirect(url_for('login'))
    
    if request.method == "POST":
        f = request.files['fimg']
        filename = secure_filename(f.filename)
        f.save(os.path.join('static', 'upload', 'images', filename))

        ftitle = request.form['title']
        fcontent = request.form['content']

        course_item = CourseModel(
            thumbnail = filename,
            title = ftitle,
            content = fcontent,
        )
        db.session.add(course_item)
        db.session.commit()
        db.session.refresh(course_item)
        return redirect(url_for('admin_course'))

    userItem = UserModel.query.get(session['userID'])

    return render_template('admin-course-create.html', user=userItem)


@app.route("/admin/course/delete/<int:course_id>")
def admin_course_delete(course_id):
    if session['role'] != "admin":
        return redirect(url_for('login'))
    
    # course_item = db.session.query(CourseModel).filter(CourseModel.id == course_id).first()
    # if course_item is None:
    #     return f"<p>Item not found with id {course_id}</p>"
    db.session.query(CourseModel).filter(CourseModel.id == course_id).delete()
    # db.session.delete(course_item)
    db.session.commit()
    return redirect(url_for('admin_course'))

    
@app.route("/admin/submission")
def admin_submissions():
    if session['role'] != "admin":
        return redirect(url_for('login'))
    
    userItem = UserModel.query.get(session['userID'])

    submission_items = EnrollmentModel.query.filter(EnrollmentModel.filename.isnot(None)).all()
    for submission in submission_items:
        print(submission.studentID)
        print(submission.courseID)
    return render_template('admin-submission.html', submissions=submission_items, user=userItem)
