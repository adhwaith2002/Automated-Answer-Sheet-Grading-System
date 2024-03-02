from flask import Blueprint,render_template,request,redirect,url_for
from asyncio.windows_events import NULL
from flask import flash
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import update
import datetime
from website.models import Student,Teacher
from website import db
from flask_login import  login_required , current_user

views = Blueprint('views',__name__)


@views.route('/')
def home():
    return render_template("home.html")



@views.route('/teachereditdashboard',methods=['GET','POST'])
@login_required
def teachereditdashboard():
    if request.method == 'POST':
        teachername = request.form.get("teachername")
        teacheremail = request.form.get("teacheremail")
        teacherdob = request.form.get("teacherdob")
        teacherdob1 = datetime.datetime.strptime(teacherdob, "%Y-%m-%d")
        teachersex =request.form.get("teachersex")
        teacherdepartment = request.form.get("teacherdepartment")

        teacher = Teacher.query.filter_by(Email=teacheremail).first()
        teacher.Teachername=teachername
        teacher.Email=teacheremail
        teacher.dob=teacherdob1
        teacher.sex=teachersex
        teacher.department =teacherdepartment

        db.session.commit() 

    return render_template('teachereditdashboard.html',user=current_user)

@views.route('/studentdashboard')
@login_required
def studentdashboard():
    return render_template('studentdashboard.html',user=current_user)

@views.route('/studentverification')
@login_required
def studentverification():
    students = Student.query.filter_by(status = 0).all()
    
    return render_template('studentverification.html',user=current_user,students = students)

@views.route('/teacherdashboard')
@login_required
def teacherdashboard():
    return render_template('teacherdashboard.html',user=current_user)

@views.route('/admindashboard')
@login_required
def admindashboard():
    return render_template('admindashboard.html',user=current_user)

@views.route('/changeadminpassword',methods = ['GET','POST'])
@login_required
def changeadminpassword():
    if request.method == 'POST':
        password = request.form.get("password")
        password1 = request.form.get("password1")
        if(password == password1):
            email = request.form.get("email")
            blood = Student.query.filter_by(email=email).first()
            blood.password=password
            db.session.commit()
            flash('password updated successfully', category='sucess')
        else:
            flash('passwords don\'t match', category='error')

    return render_template('changeadminpassword.html',user=current_user)

@views.route('/addadmin', methods=['GET','POST'])
@login_required
def addadmin():
    if request.method == 'POST':
        uname = request.form.get("uname")
        password = request.form.get("password")
        password1 = request.form.get("password1")
        dob1 = request.form.get("dob")
        dob2 = datetime.datetime.strptime(dob1, "%Y-%m-%d")
        sex = request.form.get("sex")
        bloodgroup = request.form.get("bloodgroup")
        address = request.form.get("address")
        city = request.form.get("city")
        email = request.form.get("email")
        contact = request.form.get("contact")

        if len(uname) < 2:
            flash('Name  must be greater than 1 characters', category='error')
        elif len(password1) < 7:
            flash('passwords must be atleast 7 characters', category='error')    
        elif password != password1:
            flash('passwords don\'t match', category='error')
        elif (dob1 == NULL ): 
            flash('dob must be filled', category='error')    
        elif (sex == "Select"): 
            flash('sex must be filled', category='error')
        elif (bloodgroup == "Select"): 
            flash('bloodgroup must be filled' , category ='error') 
        elif (address == NULL): 
            flash('address must be filled' , category='error')  
        elif (city == NULL): 
            flash('city must be filled' ,category='error') 
        elif len(email) < 2:
            flash('email must be greater than 5 characters',category='error')                        
        elif len(contact) != 10:
            flash('contact must conatain 10 characters',category='error')
        else:
            flash('Account created', category='sucess')
            blood = Student(uname=uname,password=password,dob=dob2,sex=sex,bloodgroup=bloodgroup,address=address,city=city,email=email,contact=contact,userrole=1)
            db.session.add(blood)
            db.session.commit()
    return render_template('addadmin.html',user=current_user)

@views.route('/<int:id>/approvestudent',methods=['GET','POST'])
@login_required
def approvestudent(id):
    student = Student.query.filter_by(id=id).first() 
    if request.method == 'POST':
        student.status= 1
        db.session.commit() 
        return redirect(url_for('views.studentverification'))

    return render_template('approvestudent.html',student=student,user=current_user)

@views.route('/<int:id>/deleteuser',methods=['GET','POST'])
@login_required
def deleteuser(id):
    donors = Student.query.filter_by(id=id).first()
    if request.method == 'POST':
        if donors:
            db.session.delete(donors)
            db.session.commit()
            return redirect(url_for('views.admineditdashboard'))
        
    return render_template('deleteuser.html',donors=donors ,user=current_user)

@views.route('/admineditdashboard')
@login_required
def admineditdashboard():
    donors = Student.query.all()
    donors.pop(1)
    return render_template('admineditdashboard.html',donors=donors,user=current_user)


@views.route('/teacherchangepassword',methods=['GET','POST'])
@login_required
def teacherchangepassword():
    if request.method == 'POST':
        teacherpassword = request.form.get("teacherpassword")
        teacherpassword1 = request.form.get("teacherpassword1")
        if(teacherpassword == teacherpassword1):
            email = request.form.get("email")
            teacher = Teacher.query.filter_by(Email=email).first()
            teacher.password=teacherpassword
            db.session.commit()
            flash('password updated successfully', category='sucess')
        else:
            flash('passwords don\'t match', category='error')

    return render_template('teacherchangepassword.html',user=current_user)

@views.route('/<int:id>/lastdonationdate',methods=['GET','POST'])
@login_required
def lastdonationdate(id):
    if request.method == 'POST':
        lastdonationdate = request.form.get("lastdonationdate")
        date = datetime.datetime.strptime(lastdonationdate, "%Y-%m-%d")
        blood = Student.query.filter_by(id=id).first()
       
        blood.Lastdonationdate=date
        db.session.commit()
        flash('Last donation date updated sucessfully',category='sucess') 
        
    return render_template('lastdonationdate.html',user=current_user)

@views.route('/uploadhealthcertificate')
@login_required
def uploadhealthcertificate():
    return render_template('uploadhealthcertificate.html',user=current_user)


@views.route('/studentregister',methods=['GET','POST'])
def studentregister():
    if request.method == 'POST':
        studentname = request.form.get("studentname")
        studentemail = request.form.get("studentemail")
        studentregisternumber = request.form.get("studentregisternumber")
        dob1 = request.form.get("studentdob")
        studentdob = datetime.datetime.strptime(dob1, "%Y-%m-%d")
        studentgender = request.form.get("studentgender")
        studentsemester = request.form.get("studentsemester")
        studentdepartment = request.form.get("studentdepartment")
        studentpassword = request.form.get("studentpassword")

       
        
        if len(studentname) < 2:
            flash('Name  must be greater than 1 characters', category='error')
        elif len(studentpassword) < 8:
            flash('passwords must be atleast 8 characters', category='error')    
        elif not dob1: 
            flash('dob must be filled', category='error') 
            return render_template('studentregister.html')    
        elif (studentgender == "Select Gender"): 
            flash('Gender must be filled', category='error')
        elif (studentregisternumber == NULL): 
            flash('studentregisternumber must be filled' , category ='error') 
        elif (studentdepartment == "Select Department"): 
            flash('Department must be filled' , category='error')  
        elif (studentsemester == "Select Semester"): 
            flash('semester must be filled' ,category='error') 
        elif len(studentemail) < 2:
            flash('email must be greater than 5 characters',category='error')                        
        else:
            flash('Account created', category='sucess')
            student = Student(Studentname=studentname,email=studentemail,register_number=studentregisternumber,dob=studentdob,sex=studentgender,semester=studentsemester,department=studentdepartment,password=studentpassword,status=0)
            db.session.add(student)
            db.session.commit()
            
        return render_template('studentregister.html') 
    return render_template("studentregister.html")      

@views.route('/teacherregister',methods=['GET','POST'])
def teacherregister():
    if request.method == 'POST':
        teachername = request.form.get("teachername")
        teacheremail = request.form.get("teacheremail")
        dob1 = request.form.get("teacherdob")
        dob2 = datetime.datetime.strptime(dob1, "%Y-%m-%d")
        teachergender = request.form.get("teachergender")
        teacherdepartment = request.form.get("teacherdepartment")
        teacherpassword = request.form.get("teacherpassword")
        
        if len(teachername) < 2:
            flash('Name  must be greater than 1 characters', category='error')
        elif len(teacheremail) < 2:
            flash('email must be greater than 5 characters',category='error')
        elif (dob1 == NULL ): 
            flash('dob must be filled', category='error')   
        elif (teachergender == "Select Gender"): 
            flash('Gender must be filled', category='error') 
        elif (teacherdepartment == "Select Department"): 
            flash('Department must be filled' , category ='error')  
        elif len(teacherpassword) < 7:
            flash('password must be atleast 7 characters', category='error')    
        else:
            flash('Account created', category='sucess')
            teacher = Teacher(Teachername=teachername,Email=teacheremail,dob=dob2,sex=teachergender,department=teacherdepartment,password=teacherpassword,status=0)
            db.session.add(teacher)
            db.session.commit()
            
        return render_template('teacherregister.html') 
    return render_template("teacherregister.html")