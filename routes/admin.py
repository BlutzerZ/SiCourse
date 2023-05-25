from models import User as UserModel, Course as CourseModel, Enrollment as EnrollmentModel
from flask import render_template, request, session, redirect, abort, url_for, render_template
from app import app, db

@app.route("/admin")
def admin_home():
    if session['role'] != "admin":
        return "redirect to login"
    userItem = UserModel.query.get(session['userID'])
    return render_template("admin-home.html", user=userItem)
    
@app.route("/admin/course")
def admin_course():
    if session['role'] != "admin":
        return "redirect to login"

    # return render_template('admin-course.html')
    return

@app.route("/admin/course/create", methods=["GET", "POST"])
def admin_course_create():
    if session['role'] != "admin":
        return "redirect to login"
    
    if request.method == "POST":
        fimg = request.form['fimg']
        ftitle = request.form['title']
        fcontent = request.form['content']

        course_item = CourseModel(
            thumbnail = fimg,
            title = ftitle,
            content = fcontent,
        )
        db.session.add(course_item)
        db.session.commit()
        db.session.refresh(course_item)
        return "course success added"

    userItem = UserModel.query.get(session['userID'])

    return render_template('admin-course-create.html', user=userItem)


@app.route("/admin/course/delete/<int:course_id>", methods=["DELETE"])
def admin_course_delete(course_id):
    if session['role'] != "admin":
        return "redirect to login"
    
    course_item = db.session.query(CourseModel).filter(CourseModel.id == course_id).first()
    if course_item is None:
        return f"<p>Item not found with id {course_id}</p>"
    db.session.delete(course_item)
    db.session.commit()
    return "course success deleted"

    
@app.route("/admin/submission")
def admin_submissions():
    if session['role'] != "admin":
        return "redirect to login"
    
    submission_items = EnrollmentModel.queryfilter(EnrollmentModel.filename.isnot(None)).all()
    for submission in submission_items:
        print(submission.studentID)
        print(submission.courseID)
    return "show all submission"
