from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user ,current_user
from website.models import Student, Teacher
from website import db

auth = Blueprint('auth', __name__)

@auth.route('/studentlogin', methods=['GET', 'POST'])
def studentlogin():
    if request.method == 'POST':
        email = request.form.get('studentloginemail')
        password = request.form.get('studentloginpassword')

        user = Student.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                login_user(user, remember=True)
                return redirect('studentdashboard')
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("studentlogin.html")


@auth.route('/teacherlogin', methods=['GET', 'POST'])
def teacherlogin():
    if request.method == 'POST':
        email = request.form.get('teacherloginemail')
        password = request.form.get('teacherloginpassword')

        user = Teacher.query.filter_by(Email=email).first()
        if user:
            if user.password == password:
                login_user(user, remember=True)
            
                return redirect('teacherdashboard')
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("teacherlogin.html")

@auth.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form.get('teacherloginemail')
        password = request.form.get('teacherloginpassword')

        user = Teacher.query.filter_by(Email=email).first()
        if user:
            if user.password == password:
                login_user(user, remember=True)
            
                return redirect('teacherdashboard')
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("adminlogin.html")


@auth.route('/studentlogout')
@login_required
def studentlogout():
    logout_user()
    return redirect(url_for('auth.studentlogin'))


@auth.route('/teacherlogout')
@login_required
def teacherlogout():
    logout_user()
    return redirect(url_for('auth.teacherlogin'))
