from flask import Flask, render_template, request, redirect, url_for, session,flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from sqlalchemy import or_, asc, desc
import matplotlib.pyplot as plt
from flask import send_file
import mplcursors
from fpdf import FPDF
import secrets


import matplotlib.pyplot as plt

from flask_login import current_user
import datetime
import random
import json
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from sqlalchemy import desc
import math
import json
import os
# from celery import Celery
# from celery.schedules import crontab
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    # Load user from database based on user_id
    return User(user_id)



app = Flask(__name__)



with open('config.json', 'r') as c:
    params = json.load(c)["params"]
    local_server = params.get("local_server", True)


# app.config['CELERYBEAT_SCHEDULE'] = {
#     'delete-old-otp': {
#         'task': 'app.delete_old_otp',
#         'schedule': crontab(minute='*'),  # Run every minute
#     },
# }

app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql6698210:dfvQrVLYPs@sql6.freemysqlhosting.net:3306/sql6698210'  # MySQL database URL
# celery = Celery(__name__, broker='redis://localhost:6379/0')
db = SQLAlchemy(app)

bcrypt=Bcrypt(app)

#migrate = Migrate(app, db)
with app.app_context():
    db.create_all()
    
# Configure session interface (Example using SQLAlchemy)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db  # SQLAlchemy instance

app.config['SECRET_KEY'] = 'HackHustlers'  # Secret key for session management

# Configure email settings
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password'],
    MAIL_DEFAULT_SENDER = 'hackhustler58@gmail.com'
)

mail = Mail(app)

@app.route('/')
def my_index():
    return render_template("index.html", token="Hello Sayali")




class Event(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(500))
    manager_name = db.Column(db.String(500))
    club_name = db.Column(db.String(100), nullable=True)
    event_date = db.Column(db.String(100))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    hall_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    ph_num = db.Column(db.BigInteger)
    department = db.Column(db.String(100), nullable=True)
    request = db.Column(db.DateTime)
    status = db.Column(db.String(255))
    comment= db.Column(db.String(500),nullable=True)
    final_status = db.Column(db.String(500), default='pending')

 


class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False,default='coep@1234')
    name = db.Column(db.String(100), nullable=True)
    contactNo = db.Column(db.String(20), nullable=True)
    clubname = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(100), nullable=True)


class Admin(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False, default='coep@1234')
    name = db.Column(db.String(500), nullable=True)
    clubname = db.Column(db.String(500), nullable=True)
    

class Superadmin(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False,default='coep@1234')
    name = db.Column(db.String(500), nullable=True)
    


class Venue(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    capacity = db.Column(db.Integer)
    features = db.Column(db.String(255))
    imgfile = db.Column(db.String(255))

class islogin(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), nullable=False,unique=True)

class Otp(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    otp = db.Column(db.Integer, nullable=True)

class Contacts(db.Model):
    # sno, Name, Email, Phone_num, msg, date
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phonenum = db.Column(db.String(255), nullable=False)
    msg = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=False)

@app.route('/logout')
def logout():
    db.session.query(islogin).delete()
    db.session.commit()
    return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Query the database to find the user with the provided email
        user = User.query.filter_by(email=email).first()
        
        if user:
            # If user exists, check if password matches
            if user.password == password:
                # If password matches, set session and redirect to dashboard
                session['user_id'] = user.sno
                new_islogin=islogin(email=email)
                db.session.add(new_islogin)
                db.session.commit()
                flash('Login successful!', 'success')  # Flash message for successful login
                return redirect(url_for('dashboard'))
            else:
                # If password doesn't match, show error message
                flash('Incorrect password. Please try again.', 'error')
                return render_template('index.html')
        else:
            # If user doesn't exist, show error message
            flash('Email not found.', 'error')
            return render_template('index.html')
    
    return render_template('index.html', error_messages={})

@app.route('/adminlogin', methods=['POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Query the database to find the user with the provided email
        admin = Admin.query.filter_by(email=email).first()
        
        if admin:
            # If user exists, check if password matches
            if admin.password == password:
                # If password matches, set session and redirect to dashboard
                session['admin_id'] = admin.sno
                flash('Login successful!', 'success')  # Flash message for successful login
                return redirect(url_for('admindashboard'))
            else:
                # If password doesn't match, show error message
                flash('Incorrect password. Please try again.', 'error')
                
        else:
            # If user doesn't exist, show error message
            flash('Email not found.', 'error')
    
    return render_template('index.html', error_messages={})
            

@app.route('/dashboard')            #USER
def dashboard():
    if 'user_id' in session:
        # If user is logged in, render dashboard page
        return render_template('dashboard.html')
    else:
        # If user is not logged in, redirect to login page
        return redirect(url_for('login'))

@app.route('/admindashboard')
def admindashboard():
    if 'admin_id' in session:
        # If admin is logged in, render admindashboard page
        return render_template('admindashboard.html')
    else:
        # If admin is not logged in, redirect to adminlogin page
        return redirect(url_for('adminlogin'))




# Route for displaying user profile
@app.route('/profile')
def profile():
    # Assuming the user is authenticated and you have their user ID stored in session
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        admins = Admin.query.all()
        club_names = [admin.clubname for admin in admins if admin.clubname]

        if user:
            return render_template('userProfile.html', user=user,club_names=club_names)
    # If user is not authenticated or not found in the database, redirect to login
    return redirect(url_for('login'))

@app.route('/admin_profile')
def admin_profile():
    # Assuming the user is authenticated and you have their admin ID stored in session
    admin_id = session.get('admin_id')
    if admin_id:
        admin = Admin.query.get(admin_id)
        if admin:
            club_names = Admin.query.filter(Admin.clubname != None).with_entities(Admin.clubname).all()
            return render_template('adminProfile.html', admin=admin, club_names=club_names)
    # If user is not authenticated or not found in the database, redirect to login
    return redirect(url_for('login'))




# Password reset token model
class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.sno'), nullable=False)
    token = db.Column(db.String(120), nullable=False)


# Route for updating user profile----------user
@app.route('/update_profile', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            # Update user information based on form submission
            user.name = request.form['name']
            user.contactNo = request.form['contactNo']
            user.clubname = request.form['orgClubName']  # Updated to 'orgClubName'
            user.department = request.form['department']
            db.session.commit()
            flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))


@app.route('/update_adminprofile', methods=['POST'])
def update_adminprofile():
    admin_id = session.get('admin_id')  # Assuming admin_id is used to identify admins
    if admin_id:
        admin = Admin.query.get(admin_id)
        if admin:
            # Update admin information based on form submission
            admin.name = request.form['name']
            admin.contactNo = request.form['contactNo']
            admin.clubname = request.form['orgClubName']
            admin.department = request.form['department']
            db.session.commit()
            flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))


# Route to display form for verifying current password
@app.route('/verify_password', methods=['GET', 'POST'])
def verify_password():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                entered_password = request.form['current_password']
                if user.password == entered_password:
                    session['verified'] = True
                    return redirect(url_for('change_password'))
                else:
                    flash('Incorrect password. Please try again.', 'error')
                    return redirect(url_for('verify_password'))
        flash('User not authenticated.', 'error')
    return render_template('verify_password.html')

# Route for changing password
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if session.get('verified'):
        if request.method == 'POST':
            user_id = session.get('user_id')
            if user_id:
                user = User.query.get(user_id)
                if user:
                    new_password = request.form['new_password']
                    user.password = new_password
                    db.session.commit()
                    flash('Password changed successfully!', 'success')
                    session.pop('verified', None)  # Remove the 'verified' flag from session
                    return redirect(url_for('profile'))
        return render_template('change_password.html')
    else:
        flash('Please verify your current password first.', 'error')
        return redirect(url_for('verify_password'))





@app.route('/verify_password_admin', methods=['GET', 'POST'])
def verify_password_admin():
    if request.method == 'POST':
        admin_id = session.get('admin_id')
        if admin_id:
            admin = Admin.query.get(admin_id)
            if admin:
                entered_password = request.form['current_password']
                if admin.password == entered_password:
                    session['verified'] = True
                    return redirect(url_for('change_password_admin'))
                else:
                    flash('Incorrect password. Please try again.', 'error')
                    return redirect(url_for('verify_password_admin'))
        flash('User not authenticated.', 'error')
    return render_template('verify_password_admin.html')


@app.route('/change_password_admin', methods=['POST', 'GET'])
def change_password_admin():
    if session.get('verified'):
        if request.method == 'POST':
            admin_id = session.get('admin_id')
            if admin_id:
                admin = Admin.query.get(admin_id)
                if admin:
                    new_password = request.form['new_password']
                    admin.password = new_password
                    db.session.commit()
                    flash('Password changed successfully!', 'success')
                    session.pop('verified', None)  # Remove the 'verified' flag from session
                    return redirect(url_for('admin_profile'))
        elif request.method == 'GET':
            return render_template('admin_changepass.html')
    else:
        flash('Please verify your current password first.', 'error')
        return redirect(url_for('verify_password_admin'))













""" @app.route('/file4(OTP)')
def file4_OTP():
    return render_template('file4(OTP).html') """

from flask import request, redirect, url_for, render_template

@app.route("/forgotpass", methods=['GET', 'POST'])
def forgot():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('You are not an eligible user','error')
        else:
            if not email:
                flash('Enter your email','error')
            else:
                otp = ''.join(random.choices('0123456789', k=5))
                otp_add = Otp(email=email, otp=otp)
                db.session.add(otp_add)
                db.session.commit()
                mail.send_message('OTP Request',
                                sender="hackhustlers.com",
                                recipients=[email],  # Pass email address as a list
                                body=f"Your OTP is {otp}.\n Do not share this OTP with anyone.")
                return redirect(url_for('file4_OTP', email=email))  # Pass the email to the next route
    return render_template('index.html', error=error)

@app.route("/file4(OTP)/<email>", methods=['GET', 'POST'])  # Added email parameter to the route
def file4_OTP(email):
    return render_template('file4(OTP).html', email=email)  # Pass the email to the template

@app.route("/verify_otp", methods=['POST'])
def verify_otp():
    if request.method == 'POST':
        otp_entered = request.form.get('otp')
        email = request.form.get('email')  # Get the email from the form
        otp_record = Otp.query.filter_by(email=email).first()
        print(f"otp_entered:{otp_entered},{type(otp_entered)}")
        print(f"otp_record:{otp_record.otp},{type(otp_record)}")
        if otp_record.otp:
            if int(otp_entered) == int(otp_record.otp):
                return redirect(url_for('OTPchange_password', email=email))
                

            else:
                return "Incorrect OTP"
        else:
            return "No OTP found for this email"
    else:
        return "Invalid request method"

@app.route("/OTPchange_password/<email>", methods=['GET', 'POST'])  # Added email parameter to the route
def OTPchange_password(email):
    return render_template('OTPchange_password.html', email=email)

from flask import request, redirect, url_for

@app.route("/change_passwordOtp", methods=['POST'])
def change_password_otp():
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')

        # Ensure the new password and confirm password match
        if new_password != confirm_password:
            return "Passwords do not match"

        # Retrieve the email from the Otp table
        otp_record = Otp.query.filter_by(email=email).first()
        if not otp_record:
            return "No OTP found for this email"
        
        # Retrieve the user from the User table based on the email
        user = User.query.filter_by(email=otp_record.email).first()
        if not user:
            return "User not found"
        
        # Update the user's password
        user.password = new_password
        db.session.commit()
        db.session.delete(otp_record)
        db.session.commit()
        return "Password updated successfully"
    else:
        return "Invalid request method"

from datetime import datetime, timedelta

# @celery.task
# def delete_old_otp():
#     threshold = datetime.utcnow() - timedelta(seconds=60)
#     old_otps = Otp.query.filter(Otp.timestamp < threshold).all()
#     for otp in old_otps:
#         db.session.delete(otp)
#     db.session.commit()






#vaishnavi code : 

@app.route('/approve/<int:event_id>')
def approve_event(event_id):
    event = Event.query.get_or_404(event_id)
    event.status = 'Accepted'
    db.session.commit()
    return redirect(url_for('hall_requests'))

# Route to handle reject action
@app.route('/reject/<int:event_id>')
def reject_event(event_id):
    event = Event.query.get_or_404(event_id)
    event.status = 'Rejected'
    db.session.commit()
    return redirect(url_for('hall_requests'))


@app.route('/view_event/<int:event_id>')
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    

    return render_template('view.html', event=event)

@app.route('/user_history')
def user_history():
    # Check if there are any entries in the islogin table
    login = islogin.query.first()
    if not login:
        # If no entries, redirect to index.html
        return redirect(url_for('my_index'))
    
    user_email = login.email

    # Query rejected events from the database associated with the user's email
    rejected_events = Event.query.filter_by(email=user_email).all()
    return render_template('user_history_display.html', user_events=rejected_events, category='Rejected Events')


from datetime import datetime
@app.route('/hall_requests', methods=['GET', 'POST'])
def hall_requests():
    search_query = request.args.get('q', '')

    # Retrieve the user ID from 
    
    admin_id = session.get('admin_id')
    
    # Fetch the user object from the database based on the user ID
    user = Admin.query.get(admin_id)

    # Retrieve the clubname attribute from the user object
    clubname = user.clubname if user else None
    print(clubname)
    
    # Query the database to retrieve all requests
    all_hall_requests = Event.query.filter(
        Event.event_date.isnot(None),
        Event.event_date >= datetime.now(),
        Event.club_name == clubname
    )
   
    # Filter events based on search criteria
    if search_query:
        all_hall_requests = all_hall_requests.filter(
            or_(
                Event.manager_name.ilike(f'%{search_query}%'),
                Event.event_name.ilike(f'%{search_query}%'),
                Event.department.ilike(f'%{search_query}%'),
                Event.club_name.ilike(f'%{search_query}%')
            )
        )

    # Fetch all records and convert them to a list
    all_hall_requests = all_hall_requests.all()

    # Sort the events using a custom sorting function
    sorted_requests = sorted(all_hall_requests, key=custom_sort)

    # Render the template with the filtered and sorted requests data
    return render_template('display.html', all_hall_requests=sorted_requests)





@app.route('/view_session')
def view_session():
    session_data = dict(session)
    return session_data

@app.route('/logout_admin', methods=['GET'])
def logout_admin():
    # Remove the user_id from the session
    session.pop('user_id', None)
    # Optionally, you can also clear the entire session
    # session.clear()
    # Redirect to the login page or any other desired page
    return redirect(url_for('login'))



@app.route('/all_events')
def all_events():
    # Retrieve the admin ID from the session
    admin_id = session.get('admin_id')
    
    # Fetch the admin object from the database based on the admin ID
    admin = Admin.query.get(admin_id)

    # Retrieve the clubname attribute from the admin object
    clubname = admin.clubname if admin else None
    
    # Query all events from the database filtered by clubname and event_date
    all_events = Event.query.filter(
        Event.event_date >= datetime.now(),
        Event.club_name == clubname
    ).all()

    return render_template('display.html', all_hall_requests=all_events, category='All Events')


@app.route('/approved_events')
def approved_events():
    # Retrieve the admin ID from the session
    admin_id = session.get('admin_id')
    
    # Fetch the admin object from the database based on the admin ID
    admin = Admin.query.get(admin_id)

    # Retrieve the clubname attribute from the admin object
    clubname = admin.clubname if admin else None
    
    # Query approved events from the database filtered by clubname, status, and event_date
    approved_events = Event.query.filter(
        Event.status == 'Accepted',
        Event.event_date >= datetime.now(),
        Event.club_name == clubname
    ).all()

    return render_template('display.html', all_hall_requests=approved_events, category='Approved Events')





@app.route('/pending_events')
def pending_events():
    # Retrieve the admin ID from the session
    admin_id = session.get('admin_id')
    
    # Fetch the admin object from the database based on the admin ID
    admin = Admin.query.get(admin_id)

    # Retrieve the clubname attribute from the admin object
    clubname = admin.clubname if admin else None
    
    # Query pending events from the database filtered by clubname, status, and event_date
    pending_events = Event.query.filter(
        Event.status == 'Pending',
        Event.event_date >= datetime.now(),
        Event.club_name == clubname
    ).all()

    return render_template('display.html', all_hall_requests=pending_events, category='Pending Events')

@app.route('/rejected_events')
def rejected_events():
    # Retrieve the admin ID from the session
    admin_id = session.get('admin_id')
    
    # Fetch the admin object from the database based on the admin ID
    admin = Admin.query.get(admin_id)

    # Retrieve the clubname attribute from the admin object
    clubname = admin.clubname if admin else None
    
    # Query rejected events from the database filtered by clubname, status, and event_date
    rejected_events = Event.query.filter(
        Event.status == 'Rejected',
        Event.event_date >= datetime.now(),
        Event.club_name == clubname
    ).all()

    return render_template('display.html', all_hall_requests=rejected_events, category='Rejected Events')


@app.route('/hall_requests_user', methods=['GET', 'POST'])
def hall_requests_user():
    search_query = request.args.get('q', '')
    
    # Check if there are any entries in the islogin table
    login = islogin.query.first()
    if not login:
        # If no entries, redirect to index.html
        return redirect(url_for('my_index'))
    
    user_email = login.email
   
    # Query the database to retrieve events associated with the user's email
    user_events = Event.query.filter_by(email=user_email)
    
    # Filter events based on search criteria
    if search_query:
        user_events = user_events.filter(
            or_(
                Event.manager_name.ilike(f'%{search_query}%'),
                Event.event_name.ilike(f'%{search_query}%'),
                Event.department.ilike(f'%{search_query}%'),
                Event.club_name.ilike(f'%{search_query}%')
            )
        )

    # Fetch all the filtered events
    user_events = user_events.all()
    # Print the filtered events to the console for debugging
    for event in user_events:
        print(event.event_name)
        
    # Render the template with the filtered requests data
    return render_template('user_display.html', user_events=user_events)

@app.route('/view_event_user/<int:event_id>')
def view_event_user(event_id):
    event = Event.query.get_or_404(event_id)
    

    return render_template('user_view.html', event=event)


@app.route('/cancel_event/<int:event_id>', methods=['POST'])
def cancel_event(event_id):
    if request.form['action'] == 'cancel':
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for('hall_requests_user'))


@app.route('/all_events_user')
def all_events_user():
    # Check if there are any entries in the islogin table
    login = islogin.query.first()
    if not login:
        # If no entries, redirect to index.html
        return redirect(url_for('my_index'))
    
    user_email = login.email

    # Query all events from the database associated with the user's email
    all_events = Event.query.filter_by(email=user_email).filter(Event.event_date >= datetime.now()).all()
    return render_template('user_display.html', user_events=all_events, category='All Events')

@app.route('/approved_events_user')
def approved_events_user():
    # Check if there are any entries in the islogin table
    login = islogin.query.first()
    if not login:
        # If no entries, redirect to index.html
        return redirect(url_for('my_index'))
    
    user_email = login.email

    # Query approved events from the database associated with the user's email
    approved_events = Event.query.filter_by(email=user_email, status='Accepted').filter(Event.event_date >= datetime.now()).all()
    return render_template('user_display.html', user_events=approved_events, category='Approved Events')

@app.route('/pending_events_user')
def pending_events_user():
    # Check if there are any entries in the islogin table
    login = islogin.query.first()
    if not login:
        # If no entries, redirect to index.html
        return redirect(url_for('my_index'))
    
    user_email = login.email

    # Query pending events from the database associated with the user's email
    pending_events = Event.query.filter_by(email=user_email, status='Pending').filter(Event.event_date >= datetime.now()).all()
    return render_template('user_display.html', user_events=pending_events, category='Pending Events')

@app.route('/rejected_events_user')
def rejected_events_user():
    # Check if there are any entries in the islogin table
    login = islogin.query.first()
    if not login:
        # If no entries, redirect to index.html
        return redirect(url_for('my_index'))
    
    user_email = login.email

    # Query rejected events from the database associated with the user's email
    rejected_events = Event.query.filter_by(email=user_email, status='Rejected').filter(Event.event_date >= datetime.now()).all()
    return render_template('user_display.html', user_events=rejected_events, category='Rejected Events')






def vis_overlapping(event_date, new_start_str, new_end_str, hall_name):
    new_start = datetime.strptime(new_start_str, '%H:%M').time()
    new_end = datetime.strptime(new_end_str, '%H:%M').time()

    events = Event.query.filter_by(event_date=event_date, hall_name=hall_name).all()
    for event in events:
        # start_time = event.start_time.strftime('%H:%M')
        # end_time = event.end_time.strftime('%H:%M')
        if(event.status.lower()=="accepted"):
            start_time = event.start_time
            end_time = event.end_time
            print(event.sno)
            # start_time = datetime.strptime(start_time, '%H:%M').time()
            # end_time = datetime.strptime(end_time, '%H:%M').time()

            if (start_time <= new_start < end_time) or \
            (start_time < new_end <= end_time) or \
            (new_start <= start_time and new_end >= end_time):
                return True
    return False




def vis_overlapping_super(event_date, new_start_str, new_end_str, hall_name):
    new_start = datetime.strptime(new_start_str, '%H:%M').time()
    new_end = datetime.strptime(new_end_str, '%H:%M').time()

    events = Event.query.filter_by(event_date=event_date, hall_name=hall_name).all()
    for event in events:
        # start_time = event.start_time.strftime('%H:%M')
        # end_time = event.end_time.strftime('%H:%M')
        if(event.final_status.lower()=="accepted"):
            start_time = event.start_time
            end_time = event.end_time
            print(event.sno)
            # start_time = datetime.strptime(start_time, '%H:%M').time()
            # end_time = datetime.strptime(end_time, '%H:%M').time()

            if (start_time <= new_start < end_time) or \
            (start_time < new_end <= end_time) or \
            (new_start <= start_time and new_end >= end_time):
                return True
    return False



@app.route('/confirm_cancel/<int:event_id>', methods=['POST'])
def confirm_cancel(event_id):
     if request.form['action'] == 'cancel':
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
     return redirect(url_for('hall_requests_user'))

@app.route('/confirm_accept/<int:event_id>', methods=['POST'])
def confirm_accept(event_id):
    if request.form['action'] == 'accept':
        event = Event.query.get_or_404(event_id)
        event_date = event.event_date
        start_time = event.start_time  # Keep .time()
        end_time = event.end_time # Keep .time()
        hall_name = event.hall_name
        if not vis_overlapping(event_date, start_time.strftime('%H:%M'), end_time.strftime('%H:%M'), hall_name):
            event.status = 'Accepted'
            db.session.commit()

            
            mail.send_message('Mail for acceptance',
                sender="hackhustler58@gmail.com",
                recipients=[event.email],  # Pass email address as a list
                body=f"Your request for event {event.event_name} has been accepted by admin  for date {event_date} from {start_time} to {end_time} at {hall_name}")
            
            flash('Event has been accepted successfully!', 'success')
            return redirect(url_for('hall_requests'))  # Pass status parameter here
        else:
            # Handle the case when there is an overlap
            event.status = 'Rejected'
            db.session.commit()
            mail.send_message('Mail for rejection',
                sender="hackhustler58@gmail.com",
                recipients=[event.email],  # Pass email address as a list
                body=f"Your request for event {event.event_name} has been rejected for date {event_date}  due to overlapping with another event")

            flash('Event has been rejected due to overlapping!', 'danger')
            return redirect(url_for('hall_requests'))   # Pass status parameter here

@app.route('/confirm_reject/<int:event_id>', methods=['POST'])
def confirm_reject(event_id):
    if request.form['action'] == 'reject':
        event = Event.query.get_or_404(event_id)
        event.status = 'Rejected'
        db.session.commit()

        mail.send_message('Mail for rejection',
                sender="hackhustler58@gmail.com",
                recipients=[event.email],  # Pass email address as a list
                body=f"Your request for event {event.event_name} has been rejected for date {event.event_date} due to some unavoidable circumstances")
        
    return redirect(url_for('hall_requests'))  # Pass status parameter here



# super admin starts



@app.route('/confirm_accept_super/<int:event_id>', methods=['POST'])
def confirm_accept_super(event_id):
    if request.form['action'] == 'accept':
        event = Event.query.get_or_404(event_id)
        event_date = event.event_date
        start_time = event.start_time  # Keep .time()
        end_time = event.end_time # Keep .time()
        hall_name = event.hall_name
        if not vis_overlapping_super(event_date, start_time.strftime('%H:%M'), end_time.strftime('%H:%M'), hall_name):
            event.final_status = 'Accepted'
            db.session.commit()

            
                        # Create a PDF using ReportLab
            pdf_filename = 'event_confirmation.pdf'
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
            styles = getSampleStyleSheet()
            style_heading = styles['Heading1']
            style_body = ParagraphStyle(name='Body', fontSize=12, leading=16)

            content = []
            content.append(Paragraph('Event Confirmation', style_heading))
            content.append(Spacer(1, 12))
            content.append(Spacer(1, 12))
            content.append(Paragraph(f'Subject: Confirmation of Hall Booking at {event.hall_name}', style_body))  
            content.append(Spacer(1, 12))
            content.append(Paragraph(f'Dear {event.manager_name},', style_body))
            content.append(Spacer(1, 12))
            content.append(Paragraph(f'We are pleased to confirm that your booking for the hall at {event.hall_name} has been successfully approved. Your event is scheduled to take place on {event.event_date} from {event.start_time} to {event.end_time} on {event.event_date}.', style_body))
            content.append(Spacer(1, 12))
            content.append(Paragraph(f'- Event: {event.event_name}', style_body))
            content.append(Paragraph(f'- Date: {event.event_date}', style_body))
            content.append(Paragraph(f'- Time: {event.start_time}', style_body))
            content.append(Paragraph(f'- Venue: {event.hall_name}', style_body))
            content.append(Spacer(1, 12))
            content.append(Paragraph('Please review the attached terms and conditions document for your reference. It contains important information regarding your booking, including policies, rules, and regulations that must be adhered to during your event.', style_body))
            content.append(Spacer(1, 12))   
            content.append(Paragraph('Regards,', style_body))
            content.append(Paragraph('COEP TECH', style_body))

            doc.build(content)

            # Attach PDF to email
            with app.open_resource(pdf_filename) as pdf_file:
                pdf_data = pdf_file.read()

            msg = Message('Mail for acceptance',
                        recipients=[event.email])
            msg.body = "Your request for event {} has been accepted for date {} from {} to {} at {}".format(event.event_name, event.event_date, event.start_time, event.end_time, event.hall_name)
            msg.attach(pdf_filename, "application/pdf", pdf_data)

            # Send email
            mail.send(msg)
                    
            flash('Event has been accepted successfully!', 'success')
            return redirect(url_for('hall_requests_super'))  # Pass status parameter here
        else:
            # Handle the case when there is an overlap
            event.final_status = 'Rejected'
            db.session.commit()
            pdf_filename = 'event_confirmation.pdf'
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
            styles = getSampleStyleSheet()
            style_heading = styles['Heading1']
            style_body = ParagraphStyle(name='Body', fontSize=12, leading=16)

            content = []
            content.append(Paragraph('Event Confirmation', style_heading))
            content.append(Spacer(1, 12))
            content.append(Spacer(1, 12))
            content.append(Paragraph(f'Subject: Confirmation of Hall Booking at {event.hall_name}', style_body))  
            content.append(Spacer(1, 12))
            content.append(Paragraph(f'Dear {event.manager_name},', style_body))
            content.append(Spacer(1, 12))
            content.append(Paragraph(f'We are pleased to confirm that your booking for the hall at {event.hall_name} has been successfully approved. Your event is scheduled to take place on {event.event_date} from {event.start_time} to {event.end_time} on {event.event_date}.', style_body))
            content.append(Spacer(1, 12))
            content.append(Paragraph(f'- Event: {event.event_name}', style_body))
            content.append(Paragraph(f'- Date: {event.event_date}', style_body))
            content.append(Paragraph(f'- Time: {event.start_time}', style_body))
            content.append(Paragraph(f'- Venue: {event.hall_name}', style_body))
            content.append(Spacer(1, 12))
            content.append(Paragraph('Please review the attached terms and conditions document for your reference. It contains important information regarding your booking, including policies, rules, and regulations that must be adhered to during your event.', style_body))
            content.append(Spacer(1, 12))   
            content.append(Paragraph('Best regards,', style_body))
            content.append(Paragraph('The Management Team', style_body))

            doc.build(content)

        # Attach PDF to email
            with app.open_resource(pdf_filename) as pdf_file:
                pdf_data = pdf_file.read()

            msg = Message('Mail for acceptance',
                          recipients=[event.email])
            msg.body = "Your request for event {} has been accepted for date {} from {} to {} at {}".format(event.event_name, event.event_date, event.start_time, event.end_time, event.hall_name)
            msg.attach(pdf_filename, "application/pdf", pdf_data)

            # Send email
            mail.send(msg)

            flash('Event has been rejected due to overlapping!', 'danger')
            return redirect(url_for('hall_requests_super'))   # Pass status parameter here

@app.route('/confirm_reject_super/<int:event_id>', methods=['POST'])
def confirm_reject_super(event_id):
    if request.form['action'] == 'reject':
        event = Event.query.get_or_404(event_id)
        event.final_status = 'Rejected'
        db.session.commit()

        mail.send_message('Mail for rejection',
                sender="hackhustler58@gmail.com",
                recipients=[event.email],  # Pass email address as a list
                body=f"Your request for event {event.event_name} has been rejected for date {event.event_date} by super admin  due to some unavoidable circumstances")
        
    return redirect(url_for('hall_requests_super'))  # Pass status parameter here





@app.route('/approve_super/<int:event_id>')
def approve_event_super(event_id):
    event = Event.query.get_or_404(event_id)
    event.final_status = 'Accepted'
    db.session.commit()
    return redirect(url_for('hall_requests_super'))

# Route to handle reject action
@app.route('/reject_super/<int:event_id>')
def reject_event_super(event_id):
    event = Event.query.get_or_404(event_id)
    event.final_status = 'Rejected'
    db.session.commit()
    return redirect(url_for('hall_requests_super'))




















@app.route('/hall_requests_super', methods=['GET', 'POST'])
def hall_requests_super():
    search_query = request.args.get('q', '')

    # Query the database to retrieve all requests
    all_hall_requests = Event.query.filter(Event.event_date.isnot(None), Event.event_date >= datetime.now())

    # Filter events based on search criteria
    if search_query:
        all_hall_requests = all_hall_requests.filter(
            or_(
                Event.manager_name.ilike(f'%{search_query}%'),
                Event.event_name.ilike(f'%{search_query}%'),
                Event.department.ilike(f'%{search_query}%'),
                Event.club_name.ilike(f'%{search_query}%')
            )
        )

    # Filter events by status (only Accepted events)
    all_hall_requests = all_hall_requests.filter_by(status='Accepted')

    # Fetch all records and convert them to a list
    all_hall_requests = all_hall_requests.all()

    # Sort the events using a custom sorting function
    sorted_requests = sorted(all_hall_requests, key=custom_sort)

    # Render the template with the filtered and sorted requests data
    return render_template('super_display.html', all_hall_requests=sorted_requests)


def custom_sort(event):
    # Example sorting logic
    if event.start_time is None:
        return datetime.max  # Return a high datetime value for events with None start time
    else:
        return event.start_time


@app.route('/all_events_super')
def all_events_super():
    # Query all events from the database where status is 'Accepted' and event date is greater than or equal to the current date
    all_events = Event.query.filter(Event.status == 'Accepted', Event.event_date >= datetime.now()).all()
    return render_template('super_display.html', all_hall_requests=all_events, category='All Events')

@app.route('/approved_events_super')
def approved_events_super():
    # Query approved events from the database where status is 'Accepted' and final status is also 'Accepted'
    approved_events = Event.query.filter(Event.status == 'Accepted', Event.final_status == 'Accepted', Event.event_date >= datetime.now()).all()
    return render_template('super_display.html', all_hall_requests=approved_events, category='Approved Events')




@app.route('/pending_events_super')
def pending_events_super():
    # Query approved events from the database where status is 'Accepted' and final status is also 'Accepted'
    approved_events = Event.query.filter(Event.status == 'Accepted', Event.final_status == 'pending', Event.event_date >= datetime.now()).all()
    return render_template('super_display.html', all_hall_requests=approved_events, category='Approved Events')



@app.route('/rejected_events_super')
def rejected_events_super():
    # Query rejected events from the database where status is 'Accepted' and final status is 'Rejected'
    rejected_events = Event.query.filter(Event.status == 'Accepted', Event.final_status == 'Rejected', Event.event_date >= datetime.now()).all()
    return render_template('super_display.html', all_hall_requests=rejected_events, category='Rejected Events')


@app.route("/home_super")
def home_super():
    venue = Venue.query.filter_by().all()
    last = math.ceil(len(venue)/int(params['no_of_posts']))
    

    page = request.args.get('page')

    if(not str(page).isnumeric()):
        page = 1
    page = int(page)
    venue = venue[(page - 1) * int(params['no_of_posts']):(page - 1) * int(params['no_of_posts']) + int(params['no_of_posts'])]
    if page == 1:
        prev = "#"
        next = "/home_super?page=" + str(page + 1)
    elif page == last:
        prev = "/home_super?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/home_super?page=" + str(page - 1)
        next = "/home_super?page=" + str(page + 1)

    return render_template('home_super.html', params=params, venue=venue, prev=prev, next=next)








# vaishnavi routes ended 

@app.route("/home")
def home():
    venue = Venue.query.filter_by().all()
    last = math.ceil(len(venue)/int(params['no_of_posts']))
    

    page = request.args.get('page')

    if(not str(page).isnumeric()):
        page = 1
    page = int(page)
    venue = venue[(page - 1) * int(params['no_of_posts']):(page - 1) * int(params['no_of_posts']) + int(params['no_of_posts'])]
    if page == 1:
        prev = "#"
        next = "/home?page=" + str(page + 1)
    elif page == last:
        prev = "/home?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/home?page=" + str(page - 1)
        next = "/home?page=" + str(page + 1)

    return render_template('home_admin.html', params=params, venue=venue, prev=prev, next=next)

@app.route("/venue")
def venue():
    venue = Venue.query.filter_by().all()
    last = math.ceil(len(venue)/int(params['no_of_posts']))
    

    page = request.args.get('page')

    if(not str(page).isnumeric()):
        page = 1
    page = int(page)
    venue = venue[(page - 1) * int(params['no_of_posts']):(page - 1) * int(params['no_of_posts']) + int(params['no_of_posts'])]
    if page == 1:
        prev = "#"
        next = "/venue?page=" + str(page + 1)
    elif page == last:
        prev = "/venue?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/venue?page=" + str(page - 1)
        next = "/venue?page=" + str(page + 1)

    return render_template('venue.html', params=params, venue=venue, prev=prev, next=next)

@app.route("/addvenue", methods=['GET','POST'])
def addvenue():
    if request.method == 'POST':
        name = request.form.get('name')
        capacity = request.form.get('capacity')
        features = request.form.get('features')
        imgfile = request.form.get('imgfile')

        f = request.files['file1']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        venue = Venue(name=name, capacity=capacity, features=features, imgfile=filename)
        db.session.add(venue)
        db.session.commit()
    return render_template('addvenue.html', params=params)


@app.route("/analytics")
def analytics():
    total_venues = Venue.query.count()
    total_bookings = Event.query.count()
    total_users = User.query.count()
    venues = Venue.query.all()
    recent_bookings = Event.query.filter_by(status='accepted').order_by(desc(Event.request)).limit(5).all()

    halls = db.session.query(Event.hall_name, db.func.count(Event.sno)).filter(Event.status == 'accepted').group_by(Event.hall_name).all()

    # Extract venue names and booking counts from the query result
    halls_data = [hall[0] for hall in halls]
    bookings_data = [hall[1] for hall in halls]

    # Create a bar graph
    plt.figure(figsize=(4, 3))  # Adjust the figsize here
    bars = plt.bar(halls_data, bookings_data, color='#3b9cc3')

    # Add labels to the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom')

    plt.xlabel('Hall Name')
    plt.ylabel('Number of Bookings')
    plt.title('Number of Bookings in Each Hall')
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Add hovering effect to display total bookings
    mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(f'Total Bookings: {int(sel.target[1])}'))

    # Save the graph as a PNG file
    plt.savefig('static/hall_stats.png')
    return render_template("analytics.html", total_venues=total_venues, total_bookings=total_bookings, total_users=total_users,recent_bookings=recent_bookings, venues=venues)


class PDFWithHeader(FPDF):
    def header(self):
        # Logo
        # self.image('static/COEP.png', 3, 5, 50)

        # Set font for the title
        self.set_font('Arial', 'B', 25)
        
        # Title
        self.cell(0, 30, 'COEP TECHNOLOGICAL UNIVERSITY PUNE', 0, 1, 'C')

@app.route('/generate_pdf', methods=['GET', 'POST'])
def generate_pdf():
    if request.method == 'POST':
        # Fetch data from the event table
        events = Event.query.all()

        # Create a PDF object with a custom page size (600mm x 400mm)
        pdf = PDFWithHeader(unit='mm', format=(600, 400))
        pdf.add_page()

        # Set font for the entire document
        pdf.set_font("Arial", size=14)

        # Add header
        

        # Logo
        pdf.image('static/COEP.jpeg', 10, 3, 40)

        pdf.ln(20)

        pdf.cell(280, 10, "Event Table Data", ln=True, align='C')

        # Add a table with headers
        pdf.set_font("Arial", style='B', size=12)  
        pdf.cell(70, 10, "Event Name", 1)
        pdf.cell(70, 10, "Manager Name", 1)
        pdf.cell(50, 10, "Club Name", 1)
        pdf.cell(40, 10, "Event Date", 1)
        pdf.cell(40, 10, "Start Time", 1)
        pdf.cell(40, 10, "End Time", 1)
        pdf.cell(50, 10, "Hall Name", 1)
        pdf.cell(90, 10, "Email", 1)
        pdf.cell(50, 10, "Phone Number", 1)
        pdf.cell(50, 10, "Department", 1)
        pdf.cell(70, 10, "Request", 1)
        pdf.ln()

        # Add data rows to the table
        pdf.set_font("Arial", size=10)
        for event in events:
            pdf.cell(70, 10, event.event_name, 1)
            pdf.cell(70, 10, event.manager_name, 1)
            pdf.cell(50, 10, event.club_name or "", 1)
            pdf.cell(40, 10, str(event.event_date), 1)
            pdf.cell(40, 10, str(event.start_time), 1)
            pdf.cell(40, 10, str(event.end_time), 1)
            pdf.cell(50, 10, event.hall_name, 1)
            pdf.cell(90, 10, event.email, 1)
            pdf.cell(50, 10, str(event.ph_num), 1)
            pdf.cell(50, 10, event.department or "", 1)
            pdf.cell(70, 10, str(event.request), 1)
            pdf.ln()

        # Save the PDF to a file
        pdf_output = 'static/event_table_data.pdf'
        pdf.output(pdf_output)

        # Return the PDF file for download
        return send_file(pdf_output, as_attachment=True)

    return render_template('analytics.html')

# @app.route('/booking_form', methods=['GET', 'POST'])
# def booking_form():
#     if request.method == 'POST':
#         # Handle form submission
#         event_name = request.form['eventName']
#         manager_name = request.form['eventManagerName']
#         club_name = request.form['orgClubName']
#         event_date = request.form['eventDate']
#         start_time = request.form['startTime']
#         end_time = request.form['endTime']
#         hall_name = request.form['hallName']  # Retrieve hall name from the form
#         email = request.form['email']
#         ph_num = request.form['phoneNumber']
#         department = request.form['department']
#         request_text = request.form['requestCreatedAt']
#         club_names = Admin.query.with_entities(Admin.clubname).distinct().all()
#     # Flatten the list of tuples into a list of club names
#         club_names = [club[0] for club in club_names]
#         status = "pending"
#         # Check for event overlap at the same venue
#         if not is_overlapping(event_date, start_time, end_time, hall_name):
#             # Add new event to the database
#             new_event = Event(event_name=event_name, manager_name=manager_name, club_name=club_name, event_date=event_date,
#                               start_time=start_time, end_time=end_time, hall_name=hall_name, email=email,
#                               ph_num=ph_num, department=department, request=request_text,status=status)
#             db.session.add(new_event)
#             db.session.commit()
#             return "Event added successfully!"
#         else:
#             return "The event overlaps with an existing event at the same venue. Please choose another time."

#     # Fetch all venues from the Venue table
#     venues = Venue.query.all()
#     return render_template('overlap.html', venues=venues,club_names=club_names)

@app.route('/booking_form', methods=['GET', 'POST'])
def booking_form():
    # Query unique club names from the Admin table
    club_names = Admin.query.with_entities(Admin.clubname).distinct().all()
    # Flatten the list of tuples into a list of club names
    club_names = [club[0] for club in club_names]

    if request.method == 'POST':
        # Handle form submission
        event_name = request.form['eventName']
        manager_name = request.form['eventManagerName']
        club_name = request.form['clubname']
        event_date = request.form['eventDate']
        start_time = request.form['startTime']
        end_time = request.form['endTime']
        hall_name = request.form['hallName']  # Retrieve hall name from the form
        email = request.form['email']
        ph_num = request.form['phoneNumber']
        department = request.form['department']
        request_text = request.form['requestCreatedAt']
        if club_name == "none":
            status = "Accepted"
        else:
            status = "pending"
        # Check for event overlap at the same venue
        if not is_overlapping(event_date, start_time, end_time, hall_name):
            # Add new event to the database
            new_event = Event(event_name=event_name, manager_name=manager_name, club_name=club_name, event_date=event_date,
                              start_time=start_time, end_time=end_time, hall_name=hall_name, email=email,
                              ph_num=ph_num, department=department, request=request_text, status=status)
            db.session.add(new_event)
            db.session.commit()
            return "Event added successfully!"
        else:
            return "The event overlaps with an existing event at the same venue. Please choose another time."

    # For GET request, fetch all venues from the Venue table
    venues = Venue.query.all()

    return render_template('overlap.html', venues=venues, club_names=club_names)


@app.route('/booking_form_admin', methods=['GET', 'POST'])
def booking_form_admin():
    if request.method == 'POST':
        # Handle form submission
        event_name = request.form['eventName']
        manager_name = request.form['eventManagerName']
        club_name = request.form['orgClubName']
        event_date = request.form['eventDate']
        start_time = request.form['startTime']
        end_time = request.form['endTime']
        hall_name = request.form['hallName']  # Retrieve hall name from the form
        email = request.form['email']
        ph_num = request.form['phoneNumber']
        department = request.form['department']
        request_text = request.form['requestCreatedAt']

        status = "pending"
        # Check for event overlap at the same venue
        if not is_overlapping(event_date, start_time, end_time, hall_name):
            # Add new event to the database
            new_event = Event(event_name=event_name, manager_name=manager_name, club_name=club_name, event_date=event_date,
                              start_time=start_time, end_time=end_time, hall_name=hall_name, email=email,
                              ph_num=ph_num, department=department, request=request_text,status=status)
            db.session.add(new_event)
            db.session.commit()
            return "Event added successfully!"
        else:
            return "The event overlaps with an existing event at the same venue. Please choose another time."

    # Fetch all venues from the Venue table
    venues = Venue.query.all()
    return render_template('booking_admin.html', venues=venues)



def is_overlapping(event_date, new_start_str, new_end_str, hall_name):
    new_start = datetime.strptime(new_start_str, '%H:%M').time()
    new_end = datetime.strptime(new_end_str, '%H:%M').time()

    events = Event.query.filter_by(event_date=event_date, hall_name=hall_name,status='accepted').all()
    for event in events:
        start_time = event.start_time.strftime('%H:%M')
        end_time = event.end_time.strftime('%H:%M')

        start_time = datetime.strptime(start_time, '%H:%M').time()
        end_time = datetime.strptime(end_time, '%H:%M').time()

        if (start_time <= new_start < end_time) or \
           (start_time < new_end <= end_time) or \
           (new_start <= start_time and new_end >= end_time):
            return True
    return False



@app.route('/calendar1',methods=['POST'])
def calendar1():
    return render_template('calendar1.html')

@app.route('/calendar_user')  
def calendar_user():
    return render_template('calendar1.html')

@app.route('/calendar_admin')   #admin
def calendar_admin():
    return render_template('calendar_admin.html')


@app.route('/fetch-events', methods=['POST'])
def fetch_events():
    try:
        selected_date_str = request.json.get('selectedDate')
        selected_datetime = datetime.fromisoformat(selected_date_str)
        selected_date = selected_datetime.date()

        print(selected_date)

        # Query events from the database for the selected date
        events = Event.query.filter_by(event_date=selected_date,final_status='Accepted').all()

        # Convert event objects to dictionary format
        event_list = []
        for event in events:
            print(event.event_name)
            event_data = {
                'event_name': event.event_name,
                'manager_name': event.manager_name,
                'club_name': event.club_name,
                'start_time': event.start_time.strftime('%H:%M'),
                'end_time': event.end_time.strftime('%H:%M'),
                'hall_name': event.hall_name,
                'email': event.email,
                'ph_num': event.ph_num,
                'department': event.department,
                'status': event.status
            }
            event_list.append(event_data)
            for i in event_list:
                print(i)
        return jsonify({'events': event_list})

    except Exception as e:
        # Handle the exception
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while fetching events'}), 500





@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if request.method == 'POST':
        name = request.form.get('name')
        capacity = request.form.get('capacity')
        features = request.form.get('features')

        f = request.files['file1']
        filename = secure_filename(f.filename)

        # Ensure the directory exists before saving the file
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        f.save(os.path.join(upload_folder, filename))
        
        venue = Venue.query.filter_by(sno=sno).first()
        venue.name = name
        venue.capacity = capacity
        venue.features = features
        venue.imgfile = filename
        db.session.commit()
        return redirect('/edit/' + sno)
    venue = Venue.query.filter_by(sno=sno).first()
    return render_template('edit.html', params=params, venue=venue, sno=sno)

@app.route("/delete/<string:sno>", methods=['GET', 'POST'])
def delete(sno): 
    venue = Venue.query.filter_by(sno=sno).first()
    db.session.delete(venue)
    db.session.commit()
    return redirect('/home')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
        # if 'user' not in session:
        # return redirect('/')
    if request.method == 'POST':
        '''add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        entry = Contacts(name=name, phonenum=phone, msg=message, email=email, date=datetime.now)
        db.session.add(entry)
        db.session.commit()
        mail.send_message(name + 'from COEP VENUE BOOKING WEBSITE wants to contact with you' ,
                          sender=email,
                          body=message + "\n" + phone,
                          recipients=[params['gmail-user']]
                          )
    return render_template('contact.html', params=params)






@app.route('/go_to_add_user', methods=['GET'])
def go_to_add_user():
    # Fetch all users from the database
    users = User.query.all()
    return render_template('adminAddUsers.html', users=users)
        
# Route to handle user search
@app.route('/search_users', methods=['GET'])
def search_users():
    search_term = request.args.get('search', '')
    # Search users by email
    users = User.query.filter(User.email.contains(search_term)).all()
    return render_template('adminAddUsers.html', users=users,search_term=search_term)

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        # Default password
        
        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists!', 'error')
        else:
            # Create a new user object
            new_user = User(email=email)
            
            try:
                # Add the new user to the database
                db.session.add(new_user)
                db.session.commit()
                flash('User added successfully!', 'success')
            except Exception as e:
                # Rollback changes if an error occurs
                db.session.rollback()
                flash(f'Error adding user: {str(e)}', 'error')
            finally:
                # Close the database session
                db.session.close()

    return render_template('adminAddUsers.html')



@app.route('/add_facad', methods=['POST'])
def add_facad():
    if request.method == 'POST':
        email = request.form['email']
        clubname=request.form['clubname']
        # Default password
        
        # Check if the user already exists
        existing_user = Admin.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists!', 'error')
        else:
            # Create a new user object
            new_facad = Admin(email=email,clubname=clubname)
            
            try:
                # Add the new user to the database
                db.session.add(new_facad)
                db.session.commit()
                flash('Facad added successfully!', 'success')
            except Exception as e:
                # Rollback changes if an error occurs
                db.session.rollback()
                flash(f'Error adding user: {str(e)}', 'error')
            finally:
                # Close the database session
                db.session.close()

    return render_template('adminAddUsers.html')













@app.route('/super_admindashboard')
def super_admindashboard():
    if 'user_id' in session:
        # If admin is logged in, render admindashboard page
        return render_template('super_admindashboard.html')
    else:
        # If admin is not logged in, redirect to adminlogin page
        return redirect(url_for('super_adminlogin'))


@app.route('/superadminlogin',methods=['POST'])
def super_adminlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Query the database to find the user with the provided email
        user = Superadmin.query.filter_by(email=email).first()
        
        if user:
            # If user exists, check if password matches
            if user.password == password:
                # If password matches, set session and redirect to dashboard
                session['user_id'] = user.sno
                     # Flash message for successful login
                return redirect(url_for('super_admindashboard'))
            else:
                # If password doesn't match, show error message
                flash('Incorrect password. Please try again.', 'error')
                return render_template('index.html')
        else:
            # If user doesn't exist, show error message
            flash('Email not found.', 'error')
            return render_template('index.html')
    
    return render_template('index.html', error_messages={})

    
@app.route('/calendar_admin_super')
def calendar_admin_super():
        return render_template('super_admincalendar.html')
    

@app.route('/superadminloginshow',methods=['POST'])
def superadminloginshow(): 
    print("hii")
    return render_template('superadminlogin.html')




if __name__ == "__main__":
    app.run(debug=True)