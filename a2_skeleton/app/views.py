#from PyQt5.QtWidgets.QWidget import updatesEnabled
from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
from app import app
from app.models import User, Course, Enrolment
from app.forms import ChooseForm, LoginForm, EnrolmentChangeForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
import csv
import io
import datetime


@app.route("/")
def home():
    return render_template('home.html', title="Home")


@app.route("/account")
@login_required
def account():
    enrol_form = EnrolmentChangeForm()
    return render_template('account.html', title="Account", enrol_form=enrol_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('generic_form.html', title='Sign In', form=form)

@app.route("/all_courses")
def all_courses():
    courses = db.session.scalars(sa.select(Course)).all()
    return render_template("all_courses.html", title="All Courses", courses=courses)


@app.route("/course_details/<int:course_id>")
def course_details(course_id):
    form = EnrolmentChangeForm()
#    is_enrolled = False
    is_enrolled = any(e.course_id == course.id for e in current_user.enrolments)

    course = db.session.get(Course, course_id)
    if not course:
        flash("Course not found.", "danger")
        return redirect(url_for("all_courses"))


    if current_user.is_authenticated:
        q = db.select(Enrolment).where(
            Enrolment.user_id == current_user.id,
            Enrolment.course_id == course.id
        )
        is_enrolled = db.session.scalar(q) is not None

    return render_template("course_details.html", title=course.title, course=course, form=form, is_enrolled=is_enrolled)

@app.route("/cancel_enrolment", methods=["POST"])
@login_required
def cancel_enrolment():
    form = EnrolmentChangeForm()
    if form.validate_on_submit():
        course_id = int(form.course_id.data)
        q = db.select(Enrolment).where(
            Enrolment.user_id == current_user.id,
            Enrolment.course_id == course_id
        )
        enrol = db.session.scalar(q)
        if enrol:
            db.session.delete(enrol)
            db.session.commit()
            flash("Enrolment cancelled.", "info")
    return redirect(url_for("account"))

@app.route("/toggle_enrolment", methods=["POST"])
@login_required
def toggle_enrolment():
    form = EnrolmentChangeForm()
    if form.validate_on_submit():
        course_id_str = form.course_id.data
        if not course_id_str or not course_id_str.isdigit():
            flash("Invalid course ID!", "danger")
            return redirect(url_for("all_courses"))

        course_id = int(course_id_str)
        q = db.select(Enrolment).where(
            Enrolment.user_id == current_user.id,
            Enrolment.course_id == course_id
        )
        enrol = db.session.scalar(q)
        if enrol:
            db.session.delete(enrol)
            flash("Unenrolled from course.", "warning")
        else:
            enrol = Enrolment(user=current_user, course_id=course_id)
            db.session.add(enrol)
            flash("Successfully enrolled!", "success")

        db.session.commit()
        return redirect(url_for("course_details", course_id=course_id))
    flash("Form validation failed", "danger")
    return redirect(url_for("all_courses"))



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Error handlers
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

# Error handler for 403 Forbidden
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

# Handler for 404 Not Found
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

# 500 Internal Server Error
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500
