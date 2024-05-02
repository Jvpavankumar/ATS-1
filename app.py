from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import pandas as pd
from datetime import date, datetime as dt
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer, BadSignature
from sqlalchemy import or_
from sqlalchemy import and_ 
from flask import Flask, render_template, request, redirect
import psycopg2
from datetime import date, datetime
import ast
import datetime
import os
import json
from flask_cors import CORS
import re
# import spacy
from flask_mail import Mail, Message
from flask import render_template, redirect, url_for, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
# from spacy.matcher import Matcher
from flask import Flask, request, render_template
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from itsdangerous import URLSafeTimedSerializer
from flask import request, render_template, flash, redirect, url_for
import secrets
import secrets
from urllib.parse import quote_plus
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'saiganeshkanuparthi@gmail.com'
app.config['MAIL_PASSWORD'] = 'tozvnmxbcejynxpe'
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

app.config['SECRET_KEY'] = secrets.token_hex(16)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
app.config['SECRET_KEY'] = secrets.token_hex(16)
# Specify the folder where uploaded resumes will be stored
UPLOAD_FOLDER = 'C:/Users/Makonis/PycharmProjects/login/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app)
# Specify the allowed resume file extensions
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from datetime import timedelta
#hello

# Specify the folder where uploaded resumes will be stored
# UPLOAD_FOLDER = 'static/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# cors = CORS(app)
# Specify the allowed resume file extensions
# ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

def generate_verification_token(user_id):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(user_id)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    client = db.Column(db.String(100))
    candidate = relationship("Candidate", back_populates="user", uselist=False)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.String(50))
    otp = db.Column(db.String(6), default=False)
    registration_completed = db.Column(db.String(50))
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'user_type': self.user_type,
            'client': self.client,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_by': self.created_by,
            'otp': self.otp,
            'registration_completed': self.registration_completed
        }

class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    client = db.Column(db.String(100), nullable=False)
    current_company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    profile = db.Column(db.String(200))
    current_job_location = db.Column(db.String(100))
    preferred_job_location = db.Column(db.String(100))
    resume = db.Column(db.String(100))
    skills = db.Column(db.String(500))
    qualifications = db.Column(db.String(200))
    experience = db.Column(db.String(200))
    relevant_experience = db.Column(db.String(200))
    current_ctc = db.Column(db.String(200))
    expected_ctc = db.Column(db.String(200))
    notice_period = db.Column(db.String(20))
    last_working_date = db.Column(db.Date)
    buyout = db.Column(db.Boolean, default=False)
    holding_offer = db.Column(db.String(20))
    total = db.Column(db.Integer)
    package_in_lpa = db.Column(db.Float)
    recruiter = db.Column(db.String(100))
    management = db.Column(db.String(100))
    status = db.Column(db.String(100))
    reason_for_job_change = db.Column(db.String(200))
    remarks = db.Column(db.String(200))
    screening_done = db.Column(db.Boolean, default=False)
    rejected_at_screening = db.Column(db.Boolean, default=False)
    l1_cleared = db.Column(db.Boolean, default=False)
    rejected_at_l1 = db.Column(db.Boolean, default=False)
    dropped_after_clearing_l1 = db.Column(db.Boolean, default=False)
    l2_cleared = db.Column(db.Boolean, default=False)
    rejected_at_l2 = db.Column(db.Boolean, default=False)
    dropped_after_clearing_l2 = db.Column(db.Boolean, default=False)
    onboarded = db.Column(db.Boolean, default=False)
    dropped_after_onboarding = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.Date, default=datetime.date.today)
    time_created = db.Column(db.Time, default=datetime.datetime.now().time())
    comments = db.Column(db.String(1000))
    linkedin_url = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    period_of_notice = db.Column(db.String(1000))
    user = relationship("User", back_populates="candidate")
    reference = db.Column(db.String(200))
    reference_name = db.Column(db.String(200))
    reference_position = db.Column(db.String(200))
    reference_information = db.Column(db.String(200))
    def serialize(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'name': self.name,
            'mobile': self.mobile,
            'email': self.email,
            'client': self.client,
            'current_company': self.current_company,
            'position': self.position,
            'profile': self.profile,
            'current_job_location': self.current_job_location,
            'preferred_job_location': self.preferred_job_location,
            'resume': self.resume,
            'skills': self.skills,
            'qualifications': self.qualifications,
            'experience': self.experience,
            'relevant_experience': self.relevant_experience,
            'current_ctc': self.current_ctc,
            'expected_ctc': self.expected_ctc,
            'notice_period': self.notice_period,
            'last_working_date': self.last_working_date.strftime('%Y-%m-%d') if self.last_working_date else None,
            'buyout': self.buyout,
            'holding_offer': self.holding_offer,
            'total': self.total,
            'package_in_lpa': self.package_in_lpa,
            'recruiter': self.recruiter,
            'management': self.management,
            'status': self.status,
            'reason_for_job_change': self.reason_for_job_change,
            'remarks': self.remarks,
            'screening_done': self.screening_done,
            'rejected_at_screening': self.rejected_at_screening,
            'l1_cleared': self.l1_cleared,
            'rejected_at_l1': self.rejected_at_l1,
            'dropped_after_clearing_l1': self.dropped_after_clearing_l1,
            'l2_cleared': self.l2_cleared,
            'rejected_at_l2': self.rejected_at_l2,
            'dropped_after_clearing_l2': self.dropped_after_clearing_l2,
            'onboarded': self.onboarded,
            'dropped_after_onboarding': self.dropped_after_onboarding,
            'date_created': self.date_created.strftime('%Y-%m-%d'),
            'time_created': self.time_created.strftime('%H:%M:%S'),
            'comments': self.comments,
            'linkedin_url': self.linkedin_url,
            'user_id': self.user_id,
            'period_of_notice': self.period_of_notice,
            'reference': self.reference,
            'reference_name': self.reference_name,
            'reference_position': self.reference_position,
            'reference_information': self.reference_information
        }

class Career_user(db.Model):
    __tablename__ = 'career_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(50), default="career_visitor")


class Career_notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recruiter_name = db.Column(db.String(100), nullable=False)
    notification_status = db.Column(db.Boolean, default=False)

    def __init__(self, recruiter_name, notification_status=False):
        self.recruiter_name = recruiter_name
        self.notification_status = notification_status


class JobPost(db.Model):
    __tablename__ = 'job_posts'

    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(100))
    experience_min = db.Column(db.Integer)
    experience_max = db.Column(db.Integer)
    budget_min = db.Column(db.String(300))
    budget_max = db.Column(db.String(300))
    location = db.Column(db.String(100))
    shift_timings = db.Column(db.String(100))
    notice_period = db.Column(db.String(100))
    role = db.Column(db.String(100))
    detailed_jd = db.Column(db.Text)
    jd_pdf = db.Column(db.String(100))
    mode = db.Column(db.String(100))
    recruiter = db.Column(db.String(1000))
    management = db.Column(db.String(100))
    date_created = db.Column(db.Date)
    time_created = db.Column(db.Time)
    job_status = db.Column(db.String(20))
    job_type = db.Column(db.String(100))
    skills = db.Column(db.String(500))
    notification = db.Column(db.String(20))

    def __init__(self, client, experience_min, experience_max, budget_min, budget_max, location, shift_timings,
                 notice_period, role, detailed_jd,jd_pdf, mode, recruiter, management,job_status,job_type,skills):
        self.client = client
        self.experience_min = experience_min
        self.experience_max = experience_max
        self.budget_min = budget_min
        self.budget_max = budget_max
        self.location = location
        self.shift_timings = shift_timings
        self.notice_period = notice_period
        self.role = role
        self.detailed_jd = detailed_jd
        self.jd_pdf = jd_pdf
        self.mode = mode
        self.recruiter = recruiter
        self.management = management
        self.job_status = job_status
        self.job_type = job_type
        self.skills = skills

class Deletedcandidate(db.Model):
    _tablename_ = 'deletedcandidate'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    candidate_name = db.Column(db.String(100), nullable=False)
    candidate_email = db.Column(db.String(100), nullable=False)
    client = db.Column(db.String(100), nullable=False)
    profile = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recruiter_name = db.Column(db.String(100), nullable=False)
    notification_status = db.Column(db.Boolean, default=False)

    def __init__(self, recruiter_name, notification_status=False):
        self.recruiter_name = recruiter_name
        self.notification_status = notification_status

@app.route('/check_candidate', methods=['POST'])
def check_candidate():
    clients = []
    profiles = []
    dates=[]
    job_ids=[]
    status=[]
    field = request.json['field']
    value = request.json['value']

    # Query the database to check for an existing candidate with the provided mobile or email
    existing_candidate = Candidate.query.filter(or_(Candidate.mobile == value, Candidate.email == value)).all()
    for i in existing_candidate:
        clients.append(" " + i.client + " ")
        profiles.append(" " + i.profile + " " )
        dates.append(i.date_created.strftime('%Y-%m-%d'))
        job_ids.append(i.job_id)
        status.append(i.status)

    # candidate = Candidate.query.filter_by(mobile=existing_candidate.mobile).first()
    if existing_candidate:
        response = {
            'message' : f"Candidate with this {field} already exists.",
            'client' : clients,
            'profile' : profiles,
            'dates':dates,
            'jobId':job_ids,
            'status':status
        }

    else:
        response = {
            'message': f"{field.capitalize()} is available.",
            'client': None,
            'profile': None,
            'dates':None,
            'jobId':None,
            'status':None
        }
    return json.dumps(response)

@app.route('/recruiter')
def recruiter_index():
    return render_template('recruiter_index.html')

@app.route('/')
def index():
    session_timeout_msg = request.args.get("session_timeout_msg")
    reset_message = request.args.get("reset_message")
    signup_message = request.args.get('signup_message')
    password_message = request.args.get('password_message')
    return render_template('index.html',reset_message=reset_message,session_timeout_msg=session_timeout_msg,signup_message=signup_message,password_message=password_message)

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

def generate_6otp():
    digits = "0123456789"
    otp = "".join(random.choice(digits) for _ in range(6))
    return otp


@app.route('/generate_otp', methods=['POST'])
def generate_otp():
    if request.method == 'POST':
        username = request.json.get('username')
        email = request.json.get('email')
        user = User.query.filter_by(username=username, email=email).first()
        if user:
            otp = generate_6otp()
            user.otp = otp
            db.session.commit()
            msg = Message('Account Verification', sender='saiganeshkanuparthi@gmail.com', recipients=[email])
            msg.body = f'Hi {user.name},\n\n OTP for resetting your password {otp}.'
            mail.send(msg)
            return jsonify({'status': 'success', 'message': 'OTP has been sent to your email.'})
        else:
            return jsonify({'status': 'error', 'message': 'User does not exist.'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request method.'})
    

   
@app.route('/reset_password', methods=['POST'])
def reset_password():
    # data=request.json
    if request.method == 'POST':
        # username =data['username']
        # email = data['email']
        otp = request.json['otp']
        new_password = request.json.get('new_password')
        confirm_password = request.json.get('confirm_password')

        # user = User.query.filter_by(username=username, email=email).first()
        user = User.query.filter_by(otp=otp).first()

        if user and user.otp == otp and new_password == confirm_password and user.user_type == 'recruiter':
            # Update the user's password in the database
            user.password = new_password
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Password changed successfully.'})
        elif user and user.otp == otp and new_password == confirm_password and user.user_type == 'management':
            # Update the user's password in the database
            user.password = new_password
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Password changed successfully.'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid OTP or password confirmation. Please try again.'})

    return jsonify({'status': 'error', 'message': 'Invalid request method.'})

@app.route('/verify/<token>')
def verify(token):
    user_id = verify_token(token)
    if user_id:
        user = User.query.get(user_id)
        user.is_verified = True
        db.session.commit()
        if user.user_type == 'management':
            return jsonify({'status': 'success', 'message': 'Account verified successfully!', 'redirect': url_for('management_login', verification_msg_manager='Your Account has been Successfully Verified. Please Login.')})
        elif user.user_type == 'recruiter':
            return jsonify({'status': 'success', 'message': 'Account verified successfully!', 'redirect': url_for('recruiter_index')})
    else:
        return jsonify({'status': 'error', 'message': 'Your verification link has expired. Please contact management to activate your account.'})
    return jsonify({'status': 'error', 'message': 'An error occurred while verifying your account.'})

import random
import string

# Function to generate a random password
def generate_random_password(length=8):
    digits = string.digits
    password = ''.join(random.choice(digits) for _ in range(length - 3))
    return "Mak" + password


@app.route('/signup', methods=['POST'])
def signup():
    user_name = session.get('user_name')

    if 'user_id' in session and 'user_type' in session:
        if session['user_type'] == 'management':
            username = request.json.get('username')
            name = request.json.get('name')
            email = request.json.get('email')
            user_type = request.json.get('user_type')

            # Check if required fields are provided
            if not all([username, name, email, user_type]):
                return jsonify({'status': 'error', 'message': 'All fields are required'})

            # Generate a random password
            password = generate_random_password()
            created_by = user_name

            user = User.query.filter(or_(User.username == username, User.email == email, User.name == name)).first()

            if user:
                return jsonify({'status': 'error', 'message': 'Account with the same Username, Email or Name Already exists.'})

            new_user = User(username=username, password=password, name=name, email=email, user_type=user_type, created_by=created_by)

            db.session.add(new_user)
            db.session.commit()

            # Generate a verification token
            verification_token = generate_verification_token(new_user.id)

            # Create the verification link
            verification_link = url_for('verify', token=verification_token, _external=True)

            # Send the verification email
            msg = Message('Account Verification', sender='saiganeshkanuparthi@gmail.com', recipients=[new_user.email])
            msg.body = f'Hello {new_user.name},\n\n We are pleased to inform you that your account has been successfully created for the ATS Makonis Talent Track Pro. Here are your login credentials:\n\nUsername: {new_user.username}\nPassword: {new_user.password}\n\nTo complete the account setup, kindly click on the verification link below : \n{verification_link}\n\n Please note that the verification link will expire after 24 hours. \n\n After successfully verifying your account, you can access the application using the following link : \n\n Application Link (Post Verification): http://vms.makonissoft.com:1818/ \n\n If you have any questions or need assistance, please feel free to reach out. \n\n Best regards, '
            mail.send(msg)

            return jsonify({'status': 'success', 'message': 'A verification email has been sent to your email address. Please check your inbox.'})
        else:
            return jsonify({'status': 'error', 'message': 'You do not have permission to create recruiter accounts.'})
    else:
        return jsonify({'status': 'error', 'message': 'You must be logged in to create a recruiter account.'})
    

@app.route('/signup-onetime', methods=['POST'])
def signup_onetime():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        name = request.json.get('name')
        email = request.json.get('email')
        user_type = 'management'
        registration_completed = 'one_time'

        user_onetime = User.query.filter_by(registration_completed='one_time').first()
        if user_onetime:
            return jsonify({'status': 'error', 'message': 'The one-time registration for this application has already been completed.'})

        new_user = User(username=username, password=password, name=name,
                        email=email, user_type=user_type, registration_completed=registration_completed)

        db.session.add(new_user)
        db.session.commit()

        # Generate a verification token
        verification_token = generate_verification_token(new_user.id)

        # Create the verification link
        verification_link = url_for('verify', token=verification_token, _external=True)

        # Send the verification email
        msg = Message('Account Verification', sender='saiganeshkanuparthi@gmail.com', recipients=[new_user.email])
        msg.body = f'Hello {new_user.name},\n\n We are pleased to inform you that your account has been successfully created for the ATS Makonis Talent Track Pro.\n\nTo complete the account setup, kindly click on the verification link below : \n{verification_link}\n\n Please note that the verification link will expire after 24 hours. \n\n After successfully verifying your account, you can access the application using the following link : \n\n Application Link (Post Verification): http://vms.makonissoft.com:1818/ \n\n If you have any questions or need assistance, please feel free to reach out. \n\n Best regards, '
        mail.send(msg)

        return jsonify({'status': 'success', 'message': 'A verification email has been sent to your email address. Please check your inbox.'})

    return jsonify({'status': 'error', 'message': 'Invalid request method.'})


@app.route('/login/recruiter', methods=['POST'])
def recruiter_login():
    verification_msg = request.args.get('verification_msg')
    reset_message = request.args.get('reset_message')
    session_timeout_msg = request.args.get("session_timeout_msg")
    password_message = request.args.get('password_message')

    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        # Check if the user exists and the password is correct
        user = User.query.filter_by(username=username, password=password, user_type='recruiter').first()
        user_id=user.id
        print(user_id)
        if user:
            if user.is_active:  # Check if the user is active
                if user.is_verified:
                    # Set the user session variables
                    session['user_id'] = user.id
                    session['user_type'] = user.user_type
                    session['username'] = user.username
                    session['user_name'] = user.name
                    session['JWT Token'] = secrets.token_hex(16)
                    return jsonify({'status': 'success', 'redirect': url_for('dashboard'),'user_id':user_id})
                else:
                    message = 'Your account is not verified yet. Please check your email for the verification link.'
            else:
                message = 'Your account is not active. Please contact the administrator.'
        else:
            message = 'Invalid username or password'

        return jsonify({'status': 'error', 'message': message})

    # For GET requests, return necessary data
    return jsonify({
        'status': 'success',
        'verification_msg': verification_msg,
        'reset_message': reset_message,
        'session_timeout_msg': session_timeout_msg,
        'password_message': password_message
    })
    

@app.route('/login/management', methods=['POST'])
def management_login():
    username = request.json.get('username')
    password = request.json.get('password')
    verification_msg_manager = request.args.get('verification_msg_manager')

    # Check if the user exists and the password is correct
    user = User.query.filter_by(username=username, password=password, user_type='management').first()
    user_id=user.id
    print(user_id)
    if user:
        if user.is_active:  # Check if the user is active
            if user.is_verified:
                # Set the user session variables
                session['user_id'] = user.id
                session['user_type'] = user.user_type
                session['username'] = user.username
                session['user_name'] = user.name
                session['JWT Token'] = secrets.token_hex(16)
                return jsonify({'status': 'success', 'redirect': url_for('dashboard'),'user_id':user_id})
            else:
                message = 'Your account is not verified yet. Please check your email for the verification link.'
        else:
            message = 'Your account is not active. Please contact the administrator.'
    else:
        message = 'Invalid username or password'

    return jsonify({'status': 'error', 'message': message, 'verification_msg_manager': verification_msg_manager})


from flask import jsonify

@app.route('/candidate_details/<int:candidate_id>/<user_type>/<int:page_no>', methods=['GET'])
def candidate_details(candidate_id, user_type, page_no):
    user_name = session.get('user_name')
    count_notification_no = Notification.query.filter(Notification.notification_status == 'false', Notification.recruiter_name == user_name).count()
    candidate = Candidate.query.get(candidate_id)
    if candidate:
        # Return JSON response with candidate details
        return jsonify({
            "candidate_id": candidate.id,
            "name": candidate.name,
            "mobile": candidate.mobile,
            "email": candidate.email,
            "client": candidate.client,
            "current_company": candidate.current_company,
            "position": candidate.position,
            "profile": candidate.profile,
            "current_job_location": candidate.current_job_location,
            "preferred_job_location": candidate.preferred_job_location,
            "resume": candidate.resume,
            "skills": candidate.skills,
            "qualifications": candidate.qualifications,
            "experience": candidate.experience,
            "relevant_experience": candidate.relevant_experience,
            "current_ctc": candidate.current_ctc,
            "expected_ctc": candidate.expected_ctc,
            "linkedin_url": candidate.linkedin_url,
            "notice_period": candidate.notice_period,
            "holding_offer": candidate.holding_offer,
            "user_type": user_type,
            "user_name": user_name,
            "count_notification_no": count_notification_no,
            "page_no": page_no
        })
    else:
        # Return JSON response with error message
        return jsonify({"error_message": "Candidate not found"}), 404



import json

@app.route('/dashboard', methods=['POST'])
def dashboard():
    data = request.json
    print(data)  # Just to verify if data is received properly

    edit_candidate_message = data.get('edit_candidate_message')
    page_no = data.get('page_no')
    candidate_message = data.get('candidate_message')
    signup_message = data.get('signup_message')
    job_message = data.get('job_message')
    update_candidate_message = data.get('update_candidate_message')
    delete_message = data.get("delete_message")

    user_id = data['user_id']
    user_type = data.get('user_type')
    user_name = data.get('user_name')

    response_data = {}

    if user_id and user_type:
        if user_type == 'recruiter':
            recruiter = User.query.filter_by(id=user_id, user_type='recruiter').first()
            if recruiter:
                candidates = Candidate.query.filter(and_(Candidate.recruiter == recruiter.name, Candidate.reference.is_(None))).all()  # Filter candidates by recruiter's name
                candidates = sorted(candidates, key=lambda candidate: candidate.id)
                count_notification_no = Notification.query.filter(Notification.notification_status == 'false',
                                                                  Notification.recruiter_name == user_name).count()
                career_count_notification_no = Career_notification.query.filter(Career_notification.notification_status == 'false',
                                                                  Career_notification.recruiter_name == user_name).count()
                response_data = {
                    'user': {
                        'id': recruiter.id,
                        'name': recruiter.name,
                        'user_type': recruiter.user_type,
                        'email': recruiter.email
                        # Add more attributes as needed
                    },
                    'user_type': user_type,
                    'user_name': user_name,
                    'candidates': [{
                        'id': candidate.id,
                        'job_id':candidate.job_id,
                        'name': candidate.name,
                        'email': candidate.email,
                        'mobile': candidate.mobile,
                        'client':candidate.client,
                        'skills':candidate.skills,
                        "profile": candidate.profile, 
                        'recruiter':candidate.recruiter,
                        "management":candidate.management,
                        'resume': candidate.resume,
                        'current_company': candidate.current_company,
                        'position': candidate.position,
                        'current_job_location': candidate.current_job_location,
                        'preferred_job_location': candidate.preferred_job_location,
                        'qualifications':candidate.qualifications,
                        'experience': candidate.experience,
                        'relevant_experience':candidate.relevant_experience,
                        'current_ctc':candidate.current_ctc,
                        'experted_ctc': candidate.expected_ctc,
                        "total":candidate.total,
                        'package_in_lpa':candidate.package_in_lpa,
                        'holding_offer':candidate.holding_offer,
                        'status': candidate.status,
                        'reason_for_job_change':candidate.reason_for_job_change,
                        'remarks':candidate.remarks,
                        'screening_done': candidate.screening_done,
                        'rejected_at_screening': candidate.rejected_at_screening,
                        'l1_cleared':candidate.l1_cleared,
                        'rejected_at_l1':candidate.rejected_at_l1,
                        "dropped_after_clearing_l1": candidate.dropped_after_clearing_l1,
                        'l2_cleared':candidate.l1_cleared,
                        'rejected_at_l2':candidate.rejected_at_l1,
                        "dropped_after_clearing_l2": candidate.dropped_after_clearing_l1,
                        'onboarded': candidate.onboarded,
                        'dropped_after_onboarding': candidate.dropped_after_onboarding,
                        'linkedin_url': candidate.linkedin_url,
                        'period_of_notice': candidate.period_of_notice,
                        'reference': candidate.reference,
                        'reference_name': candidate.reference_name,
                        'reference_position': candidate.reference_position,
                        'reference_information': candidate.reference_information,
                        'comments':candidate.comments,
                        "time_created":str(candidate.time_created),
                        "date_created": str(candidate.date_created)
                        # Add more attributes as needed
                    } for candidate in candidates],
                    'candidate_message': candidate_message,
                    'update_candidate_message': update_candidate_message,
                    'count_notification_no': count_notification_no,
                    'edit_candidate_message': edit_candidate_message,
                    'page_no': page_no,
                    'career_count_notification_no': career_count_notification_no
                }
        elif user_type == 'management':
            users = User.query.all()
            candidates = Candidate.query.filter(Candidate.reference.is_(None)).all()
            candidates = sorted(candidates, key=lambda candidate: candidate.id)
            jobs = JobPost.query.all()
            response_data = {
                'users': [{
                    'id': user.id,
                    'name': user.name,
                    'user_type': user.user_type,
                    'email': user.email
                     
                    # Add more attributes as needed
                } for user in users],
                'user_type': user_type,
                'user_name': user_name,
                'candidates': [{
                        'id': candidate.id,
                        'job_id':candidate.job_id,
                        'name': candidate.name,
                        'email': candidate.email,
                        'mobile': candidate.mobile,
                        'client':candidate.client,
                        'skills':candidate.skills,
                        "profile": candidate.profile, 
                        'recruiter':candidate.recruiter,
                        "management":candidate.management,
                        'resume': candidate.resume,
                        'current_company': candidate.current_company,
                        'position': candidate.position,
                        'current_job_location': candidate.current_job_location,
                        'preferred_job_location': candidate.preferred_job_location,
                        'qualifications':candidate.qualifications,
                        'experience': candidate.experience,
                        'relevant_experience':candidate.relevant_experience,
                        'current_ctc':candidate.current_ctc,
                        'experted_ctc': candidate.expected_ctc,
                        "total":candidate.total,
                        'package_in_lpa':candidate.package_in_lpa,
                        'holding_offer':candidate.holding_offer,
                        'status': candidate.status,
                        'reason_for_job_change':candidate.reason_for_job_change,
                        'remarks':candidate.remarks,
                        'screening_done': candidate.screening_done,
                        'rejected_at_screening': candidate.rejected_at_screening,
                        'l1_cleared':candidate.l1_cleared,
                        'rejected_at_l1':candidate.rejected_at_l1,
                        "dropped_after_clearing_l1": candidate.dropped_after_clearing_l1,
                        'l2_cleared':candidate.l1_cleared,
                        'rejected_at_l2':candidate.rejected_at_l1,
                        "dropped_after_clearing_l2": candidate.dropped_after_clearing_l1,
                        'onboarded': candidate.onboarded,
                        'dropped_after_onboarding': candidate.dropped_after_onboarding,
                        'linkedin_url': candidate.linkedin_url,
                        'period_of_notice': candidate.period_of_notice,
                        'reference': candidate.reference,
                        'reference_name': candidate.reference_name,
                        'reference_position': candidate.reference_position,
                        'reference_information': candidate.reference_information,
                        'comments':candidate.comments,
                        "time_created":str(candidate.time_created),
                        "date_created": str(candidate.date_created)
                    # Add more attributes as needed
                } for candidate in candidates],
                'jobs': [{
                    'id': job.id,
                    'client': job.client,
                    'experience_min': job.experience_min,
                    'experience_max': job.experience_max,
                    'budget_min': job.budget_min,
                    'budget_max': job.budget_max,
                    'location': job.location,
                    'shift_timings': job.shift_timings,
                    'notice_period': job.notice_period,
                    'role': job.role,
                    'detailed_jd': job.detailed_jd,
                    'jd_pdf': job.jd_pdf,
                    'mode': job.mode,
                    'recruiter': job.recruiter,
                    'management': job.management,
                    'date_created': job.date_created,
                    'time_created': job.time_created,
                    'job_status': job.job_status,
                    'job_type': job.job_type,
                    'skills': job.skills,
                    'notification': job.notification
                    # Add more attributes as needed
                } for job in jobs],
                'signup_message': signup_message,
                'job_message': job_message,
                'page_no': page_no,
                'edit_candidate_message': edit_candidate_message
            }
        else:
            user = User.query.filter_by(id=user_id).first()
            if user:
                candidates = Candidate.query.filter_by(recruiter=user.name).all()  # Filter candidates by user's name
                response_data = {
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'user_type': user.user_type,
                        'email': user.email
                        # Add more attributes as needed
                    },
                    'user_type': user_type,
                    'user_name': user_name,
                    'candidates': [{
                        'id': candidate.id,
                        'job_id':candidate.job_id,
                        'name': candidate.name,
                        'email': candidate.email,
                        'mobile': candidate.mobile,
                        'client':candidate.client,
                        'skills':candidate.skills,
                        "profile": candidate.profile, 
                        'recruiter':candidate.recruiter,
                        "management":candidate.management,
                        'resume': candidate.resume,
                        'current_company': candidate.current_company,
                        'position': candidate.position,
                        'current_job_location': candidate.current_job_location,
                        'preferred_job_location': candidate.preferred_job_location,
                        'qualifications':candidate.qualifications,
                        'experience': candidate.experience,
                        'relevant_experience':candidate.relevant_experience,
                        'current_ctc':candidate.current_ctc,
                        'experted_ctc': candidate.expected_ctc,
                        "total":candidate.total,
                        'package_in_lpa':candidate.package_in_lpa,
                        'holding_offer':candidate.holding_offer,
                        'status': candidate.status,
                        'reason_for_job_change':candidate.reason_for_job_change,
                        'remarks':candidate.remarks,
                        'screening_done': candidate.screening_done,
                        'rejected_at_screening': candidate.rejected_at_screening,
                        'l1_cleared':candidate.l1_cleared,
                        'rejected_at_l1':candidate.rejected_at_l1,
                        "dropped_after_clearing_l1": candidate.dropped_after_clearing_l1,
                        'l2_cleared':candidate.l1_cleared,
                        'rejected_at_l2':candidate.rejected_at_l1,
                        "dropped_after_clearing_l2": candidate.dropped_after_clearing_l1,
                        'onboarded': candidate.onboarded,
                        'dropped_after_onboarding': candidate.dropped_after_onboarding,
                        'linkedin_url': candidate.linkedin_url,
                        'period_of_notice': candidate.period_of_notice,
                        'reference': candidate.reference,
                        'reference_name': candidate.reference_name,
                        'reference_position': candidate.reference_position,
                        'reference_information': candidate.reference_information,
                        'comments':candidate.comments,
                        "time_created":str(candidate.time_created),
                        "date_created": str(candidate.date_created)
                        # Add more attributes as needed
                    } for candidate in candidates],
                }
    else:
        response_data = {"message": "User ID or User Type missing"}

    # Convert date objects to string representations before returning the response
    for job in response_data.get('jobs', []):
        job['date_created'] = job['date_created'].isoformat()

    return Response(json.dumps(response_data, default=str), content_type='application/json')





# Mocked function for demonstration
# Mocked function for demonstration
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'doc', 'docx'}


import binascii  

@app.route('/add_candidate', methods=['POST'])
def add_candidate():
    try:
        # Retrieve user session data
        user_id = session.get('user_id')
        user_type = session.get('user_type')
        user_name = session.get('user_name')

        # Retrieve request data from JSON
        data = request.json
        user_id = data.get('user_id')
        job_id = data.get('job_id')
        client = data.get('client')
        name = data.get('name')
        mobile = data.get('mobile')
        email = data.get('email')
        profile = data.get('profile')
        skills = data.get('skills')
        current_company = data.get('current_company')
        position = data.get('position')
        current_job_location = data.get('current_job_location')
        preferred_job_location = data.get('preferred_job_location')
        qualifications = data.get('qualifications')
        experience = data.get('experience')
        relevant_experience = data.get('relevant_experience')
        current_ctc = data.get('current_ctc')
        expected_ctc = data.get('expected_ctc')
        linkedin = data.get('linkedin')
        notice_period = data.get('notice_period')
        holding_offer = data.get('holding_offer')
        resume = data.get('resume')

        # Check if the resume is a hexadecimal string and convert it to bytes
        if isinstance(resume, str):
            # Remove leading backslashes and split the string into pairs of hexadecimal digits
            hex_string = resume.replace("\\", "").replace("\\", "")
            # Decode the hexadecimal string to bytes using binascii.unhexlify()
            resume = binascii.unhexlify(hex_string)

        elif isinstance(resume, bytes):
            resume = resume
        # else:
        #     raise ValueError("Resume must be either a hexadecimal string or bytes.")

        # Check if the user is logged in
        if 'user_id' in session and 'user_type' in session:
            if request.method == 'POST':
                # Retrieve the logged-in user's ID and user type from the session
                user_id = session['user_id']
                user_type = session['user_type']
                user_name = session['user_name']

            # Retrieve the recruiter and management names based on user type
            if user_type == 'recruiter':
                recruiter = User.query.get(user_id).name
                management = None
            elif user_type == 'management':
                recruiter = None
                management = User.query.get(user_id).name
            else:
                recruiter = None
                management = None

            # Check if the job_id is provided and job is active
            matching_job_post = JobPost.query.filter(and_(JobPost.id == job_id, JobPost.job_status == 'Active')).first()
            if not matching_job_post:
                return jsonify({"error_message": "Job on hold"})

            # Create new candidate object
            new_candidate = Candidate(
                user_id=user_id,
                job_id=job_id,
                name=name,
                mobile=mobile,
                email=email,
                client=client,
                current_company=current_company,
                position=position,
                profile=profile,
                current_job_location=current_job_location,
                preferred_job_location=preferred_job_location,
                qualifications=qualifications,
                experience=experience,
                relevant_experience=relevant_experience,
                current_ctc=current_ctc,
                expected_ctc=expected_ctc,
                notice_period=notice_period,
                linkedin_url=linkedin,
                holding_offer=holding_offer,
                recruiter=recruiter,
                management=management,
                status='None',
                remarks=data.get('remarks'),
                skills=skills,
                resume=resume,
                period_of_notice=data.get('months') if notice_period == 'no' else None,
                last_working_date=data.get('last_working_date') if notice_period in {'yes', 'completed'} else None,
                buyout='buyout' in data
            )

            new_candidate.date_created = date.today()
            new_candidate.time_created = datetime.now().time()

            db.session.add(new_candidate)
            db.session.commit()

            return jsonify({"message": "Candidate Added Successfully", "candidate_id": new_candidate.id})

        return jsonify({"error_message": "User not logged in"})

    except Exception as e:
        return jsonify({"error_message": str(e)})

        
from flask import jsonify

@app.route('/get_job_role', methods=['GET'])
def get_job_role():
    job_id = request.args.get('job_id')

    job_post = JobPost.query.filter_by(id=job_id).first()
    if job_post:
        return jsonify({"role": job_post.role})
    else:
        return jsonify({"role": ""})

@app.route('/delete_candidate/<int:candidate_id>', methods=["POST"])
def delete_candidate(candidate_id):
    if 'user_id' in session and 'user_type' in session:
        user_type = session['user_type']
        user_name = session['user_name']

        if user_type == 'management':
            candidate = Candidate.query.filter_by(id=candidate_id).first()

            if candidate:
                if request.method == "POST":
                    # Save deletion details before deleting the candidate
                    deleted_candidate = Deletedcandidate(
                        username=user_name,
                        candidate_name=candidate.name,
                        candidate_email=candidate.email,
                        client=candidate.client,
                        profile=candidate.profile,
                        status=candidate.status
                    )
                    db.session.add(deleted_candidate)
                    db.session.commit()

                    # Delete the candidate
                    Candidate.query.filter_by(id=candidate_id).delete()
                    db.session.commit()

                    return jsonify({"message": "Candidate details deleted successfully"})

                return jsonify({
                    "candidate": {
                        "id": candidate.id,
                        "name": candidate.name,
                        "email": candidate.email,
                        "client": candidate.client,
                        "profile": candidate.profile,
                        "status": candidate.status
                    },
                    "user_name": user_name
                })

            else:
                return jsonify({"error_message": "Candidate not found"}), 404

        return jsonify({"error_message": "Unauthorized: Only management can delete candidates"}), 401

    return jsonify({"error_message": "Unauthorized: You must log in to access this page"}), 401


@app.route('/delete_candidate_recruiter/<int:candidate_id>', methods=["GET", "POST"])
def delete_candidate_recruiter(candidate_id):
    if 'user_id' in session and 'user_type' in session:
        user_type = session['user_type']
        user_name = session['user_name']

        if user_type == 'management':
            candidate = Candidate.query.filter_by(id=candidate_id,recruiter=user_name)

            if request.method == "POST":
                # Save deletion details before deleting the candidate
                deleted_candidate = Deletedcandidate(
                    username=user_name,
                    candidate_name=candidate.name,
                    candidate_email=candidate.email,
                    client=candidate.client,
                    profile=candidate.profile,
                    status=candidate.status
                )
                db.session.add(deleted_candidate)
                db.session.commit()

                # Delete the candidate
                Candidate.query.filter_by(id=candidate_id).delete()
                db.session.commit()

                return redirect(url_for('dashboard', delete_message="Candidate details deleted successfully"))

            return render_template('delete_candidate.html', candidate=candidate, user_name=user_name)

        return "Unauthorized: Only management can delete candidates", 401

    return "Unauthorized: You must log in to access this page", 401


def verify_token(token):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        user_id = serializer.loads(token, max_age=86400)  
        return user_id
    except BadSignature:
        return None  
    except Exception as e:
        return None

# Search String Changed
# @app.route('/update_candidate/<int:candidate_id>/<page_no>/<search_string>', methods=['GET', 'POST'])
@app.route('/update_candidate/<int:candidate_id>', methods=['POST'])
def update_candidate(candidate_id):
    print(type(candidate_id))
    if 'user_id' in session and 'user_type' in session:
        print("Hello")
        user_id = session['user_id']
        user_type = session['user_type']
        user_name = session['user_name']
        count_notification_no = Notification.query.filter(Notification.notification_status == 'false',
                                                          Notification.recruiter_name == user_name).count()
        career_count_notification_no = Career_notification.query.filter(
            Career_notification.notification_status == 'false',
            Career_notification.recruiter_name == user_name).count()
        if request.method == 'POST':
            user_id = session['user_id']
            user_type = session['user_type']
            if user_type == 'recruiter':
                recruiter = User.query.get(user_id).name
                management = None
            elif user_type == 'management':
                recruiter = None
                management = User.query.get(user_id).name
            else:
                recruiter = None
                management = None

            if user_type == 'recruiter':
                user_email = User.query.get(user_id).email
                management_email = None
            elif user_type == 'management':
                user_email = None
                management_email = User.query.get(user_id).email
            else:
                user_email = None
                management_email = None

            candidate = Candidate.query.filter_by(id=candidate_id).first()
            print(candidate)
            
            previous_status = candidate.status

            candidate_status = request.json.get('candidate_status')
            candidate_comment = request.json.get('comments')

            candidate.status = candidate_status
            candidate.comments = candidate_comment

            db.session.commit()

            if candidate_status in ["SCREENING", "SCREEN REJECTED", "NO SHOW", "DROP", "CANDIDATE HOLD", "OFFERED - DECLINED", "DUPLICATE"]:
                candidate_name = candidate.name
                candidate_position = candidate.position
                candidate_email = candidate.email

                if candidate_position:
                    candidate_position = candidate_position.upper()
                else:
                    candidate_position = ""

                if candidate.client:
                    client = candidate.client.upper()
                else:
                    client = ""

                if candidate_status in ["SCREENING", "SCREEN REJECTED"]:
                    message = f'Dear {candidate_name}, \n\nGreetings! \n\nWe hope this email finds you well. We wanted to extend our thanks for showing your interest in the {candidate_position} position and participating in the recruitment process. \n\nWe are writing to inform you about the latest update we received from our client {client} regarding your interview. \n\n        Current Status :  "{candidate_status}"\n\nThank you once again for considering this opportunity with us. We wish you all the best in your future endeavors. \n\nIf you have any questions or need further information, please feel free to reach out to us. \n\nThanks,\n'
                else:
                    message = f'Dear {candidate_name}, \n\nGreetings! \n\nWe hope this email finds you well. We wanted to extend our thanks for showing your interest in the {candidate_position} position and participating in the recruitment process. \n\nWe are writing to inform you about the latest update we received from our client {client} regarding your interview. \n\n        Previous Status : "{previous_status}"\n\n        Current Status :  "{candidate_status}"\n\nThank you once again for considering this opportunity with us. We wish you all the best in your future endeavors. \n\nIf you have any questions or need further information, please feel free to reach out to us. \n\nThanks,\n'
            else:
                message = ""
                candidate_name = ""
                candidate_position = ""
                candidate_email = ""

            return jsonify({
            "message": "Candidate Status Updated Successfully",
            "user_id": user_id,
            "user_type": user_type,
            "user_name": user_name,
            "count_notification_no": count_notification_no,
            "career_count_notification_no": career_count_notification_no,
            "recruiter": recruiter,
            "management": management,
            "recruiter_email": user_email,
            "management_email": management_email,
            "candidate_name": candidate_name,
            "candidate_position": candidate_position,
            "candidate_email": candidate_email,
            "message": message
        }),200



@app.route('/update_candidate_careers/<int:candidate_id>/<page_no>/<search_string>', methods=['GET', 'POST'])
@app.route('/update_candidate_careers/<int:candidate_id>/<page_no>', methods=['GET', 'POST'])
def update_candidate_careers(candidate_id, page_no):
    if 'user_id' in session and 'user_type' in session:
        user_id = session['user_id']
        user_type = session['user_type']
        user_name = session['user_name']
        count_notification_no = Notification.query.filter(Notification.notification_status == 'false',
                                                          Notification.recruiter_name == user_name).count()
        career_count_notification_no = Career_notification.query.filter(
            Career_notification.notification_status == 'false',
            Career_notification.recruiter_name == user_name).count()
        if request.method == 'POST':
            # Retrieve the logged-in user's ID and user type from the session
            user_id = session['user_id']
            user_type = session['user_type']

            # Retrieve the recruiter and management names based on user type
            if user_type == 'recruiter':
                recruiter = User.query.get(user_id).name
                management = None
            elif user_type == 'management':
                recruiter = None
                management = User.query.get(user_id).name
            else:
                recruiter = None
                management = None

            if user_type == 'recruiter':
                recruiter_email = User.query.get(user_id).email
                management = None
            elif user_type == 'management':
                recruiter = None
                recruiter_email = User.query.get(user_id).email
            else:
                recruiter_email = None
                management_email = None

            # Retrieve the form data for the candidate
            candidate = Candidate.query.get(candidate_id)
            previous_status = candidate.status
            # candidate.recruiter = recruiter
            # candidate.management = management

            # Get the selected candidate status from the form
            candidate_status = request.form.get('candidate_status')
            candidate_comment = request.form.get('comments')

            # Update the candidate status field
            candidate.status = candidate_status

            candidate.comments = candidate_comment

            db.session.commit()

            if candidate_status == "SCREENING" or candidate_status == "SCREEN REJECTED":
                candidate_name = candidate.name
                candidate_position = candidate.position

                # Retrieve the candidate's email
                candidate_email = candidate.email

                # Determine if the logged-in user is a recruiter or management
                user_type = session.get('user_type')

                if user_type == 'recruiter' or user_type == 'management':
                    # Retrieve the corresponding user's email
                    user_email = User.query.get(session.get('user_id')).email

                    message = Message(f'Job Application Status - {candidate_position}',
                                      sender='saich5252@gmail.com', recipients=[candidate_email])

                    if user_type == 'management':
                        management_email = user_email
                        message.cc = [management_email]
                    elif user_type == 'recruiter':
                        recruiter_email = user_email
                        message.cc = [recruiter_email]
                    message.body = f'''Dear {candidate.name}, 

Greetings! 

We hope this email finds you well. We wanted to extend our thanks for showing your interest in the {candidate.position.upper()} position and participating in the recruitment process. 

We are writing to inform you about the latest update we received from our client {candidate.client.upper()} regarding your interview. 

        Current Status :  "{candidate.status}"

Thank you once again for considering this opportunity with us. We wish you all the best in your future endeavors. 

If you have any questions or need further information, please feel free to reach out to us. 

Thanks, 
                            '''
                #mail.send(message)
                pass
            elif candidate_status == "NO SHOW" or candidate_status == "DROP" or candidate_status == "CANDIDATE HOLD" or candidate_status == "OFFERED - DECLINED" or candidate_status == "DUPLICATE":
                pass
            else:
                candidate_name = candidate.name
                candidate_position = candidate.position
                candidate_email = candidate.email

                user_type = session.get('user_type')

                if user_type == 'recruiter' or user_type == 'management':
                    user_email = User.query.get(session.get('user_id')).email

                    message = Message(f'Job Application Status - {candidate_position}',
                                      sender='saich5252@gmail.com', recipients=[candidate_email])

                    if user_type == 'management':
                        management_email = user_email
                        message.cc = [management_email]
                    elif user_type == 'recruiter':
                        recruiter_email = user_email
                        message.cc = [recruiter_email]
                    message.body = f'''Dear {candidate.name}, 

Greetings! 

We hope this email finds you well. We wanted to extend our thanks for showing your interest in the {candidate.position.upper()} position and participating in the recruitment process. 

We are writing to inform you about the latest update we received from our client {candidate.client.upper()} regarding your interview. 

        Previous Status : "{previous_status}"

        Current Status :  "{candidate.status}"

Thank you once again for considering this opportunity with us. We wish you all the best in your future endeavors. 

If you have any questions or need further information, please feel free to reach out to us. 

Thanks, 
                            '''
                #mail.send(message)
                pass

            return redirect(
                url_for('career_dashboard', update_candidate_message='Candidate Status Updated Sucessfully', page_no=page_no))

        candidate = Candidate.query.get(candidate_id)
        candidate_data = {
            'id': candidate.id,
            'name': candidate.name,
            'mobile': candidate.mobile,
            'email': candidate.email,
            'client': candidate.client,
            'current_company': candidate.current_company,
            'position': candidate.position,
            'profile': candidate.profile,
            'current_job_location': candidate.current_job_location,
            'preferred_job_location': candidate.preferred_job_location,
            'resume': candidate.resume,
            'qualifications': candidate.qualifications,
            'experience': candidate.experience,
            'relevant_experience': candidate.relevant_experience,
            'current_ctc': candidate.current_ctc,
            'expected_ctc': candidate.expected_ctc,
            'notice_period': candidate.notice_period,
            'last_working_date': candidate.last_working_date,
            'buyout': candidate.buyout,
            'holding_offer': candidate.holding_offer,
            'total': candidate.total,
            'package_in_lpa': candidate.package_in_lpa,
            'reason_for_job_change': candidate.reason_for_job_change,
            'remarks': candidate.remarks,
            'candidate_status': candidate.status,
        }

        return render_template('update_candidate.html', candidate_data=candidate_data, user_id=user_id,
                               user_type=user_type, user_name=user_name, candidate=candidate,
                               count_notification_no=count_notification_no,
                               career_count_notification_no=career_count_notification_no)

    return redirect(url_for('career_dashboard'))



@app.route('/logout', methods=['POST'])
def logout():
    data = request.json
    
    if data:
        user_type = data.get("user_type")
        message = data.get("message")

        if user_type == "management":
            session.clear()
            return jsonify({"status": "success", "message": message}), 200
        else:
            session.clear()
            return jsonify({"status": "success", "message": message}), 200
    
    return jsonify({"status": "error", "message": "No JSON data provided"}), 400


from datetime import datetime

# Search String Changed
@app.route('/edit_candidate/<int:candidate_id>/<int:page_no>/<search_string>', methods=['GET', 'POST'])
@app.route('/edit_candidate/<int:candidate_id>', methods=['POST'])
def edit_candidate(candidate_id):
    if 'user_id' in session and 'user_type' in session:
        user_name = session['user_name']
        count_notification_no = Notification.query.filter(Notification.notification_status == 'false',
                                                          Notification.recruiter_name == user_name).count()
        career_count_notification_no = Career_notification.query.filter(
            Career_notification.notification_status == 'false',
            Career_notification.recruiter_name == user_name).count()

        if request.method == 'POST':
            # Retrieve the form data for the candidate from JSON payload
            data = request.json

            # Retrieve the candidate object
            candidate = Candidate.query.get(candidate_id)
            if candidate:
                # Update the candidate fields with the new data
                candidate.name = data.get('name')
                candidate.mobile = data.get('mobile')
                candidate.email = data.get('email')
                candidate.client = data.get('client')
                candidate.current_company = data.get('current_company')
                candidate.position = data.get('position')
                candidate.profile = data.get('profile')
                candidate.current_job_location = data.get('current_job_location')
                candidate.preferred_job_location = data.get('preferred_job_location')
                candidate.qualifications = data.get('qualifications')
                experience = data.get('total_experience_years')
                exp_months = data.get('total_experience_months')
                if experience is not None and exp_months is not None:
                    candidate.experience = f"{experience}.{exp_months}"
                else:
                    return jsonify({"error_message": "Experience or experience months is missing"}), 400
                candidate.current_ctc = f"{data['currency_type_current']} {data['current_ctc']}"
                candidate.expected_ctc = f"{data['currency_type_except']} {data['expected_ctc']}"
                candidate.notice_period = data.get('notice_period')
                candidate.reason_for_job_change = data.get('reason_for_job_change')
                candidate.linkedin_url = data.get('linkedin')
                candidate.remarks = data.get('remarks')
                candidate.skills = data.get('skills')
                candidate.holding_offer = data.get('holding_offer')
                candidate.total = data.get('total')
                candidate.package_in_lpa = data.get('package_in_lpa')
                candidate.period_of_notice = data.get('period_of_notice')

                db.session.commit()
                return jsonify({"message": "Candidate Details Edited Successfully"})
            else:
                return jsonify({"error_message": "Candidate not found"}), 404

    return jsonify({"error_message": "Unauthorized: You must log in to access this page"}), 401


@app.route('/edit_candidate_careers/<int:candidate_id>/<int:page_no>/<search_string>', methods=['GET', 'POST'])
@app.route('/edit_candidate_careers/<int:candidate_id>/<int:page_no>', methods=['GET', 'POST'])
def edit_candidate_careers(candidate_id, page_no):
    if 'user_id' in session and 'user_type' in session:
        user_id = session['user_id']
        user_type = session['user_type']
        user_name = session['user_name']
        count_notification_no = Notification.query.filter(Notification.notification_status == 'false',
                                                          Notification.recruiter_name == user_name).count()
        career_count_notification_no = Career_notification.query.filter(
            Career_notification.notification_status == 'false',
            Career_notification.recruiter_name == user_name).count()

        if request.method == 'POST':
            # Retrieve the logged-in user's ID and user type from the session
            user_id = session['user_id']
            user_type = session['user_type']

            # Retrieve the form data for the candidate
            candidate = Candidate.query.get(candidate_id)

            # Update the candidate information based on user type
            if user_type == 'recruiter':
                candidate.recruiter = User.query.get(user_id).name
            elif user_type == 'management':
                candidate.management = User.query.get(user_id).name

            # Update the candidate fields with the new form data
            candidate.name = request.form.get('name')
            candidate.mobile = request.form.get('mobile')
            candidate.email = request.form.get('email')
            candidate.client = request.form.get('client')
            candidate.current_company = request.form.get('current_company')
            candidate.position = request.form.get('position')
            candidate.profile = request.form.get('profile')
            candidate.current_job_location = request.form.get('current_job_location')
            candidate.preferred_job_location = request.form.get('preferred_job_location')
            candidate.qualifications = request.form.get('qualifications')
            experience = request.form.get('experience')
            exp_months = request.form.get('exp_months')
            candidate.experience = experience +'.'+exp_months
            relevant_experience = request.form.get('relevant_experience')
            relevant_exp_months = request.form.get('relevant_exp_months')
            candidate.relevant_experience = relevant_experience + '.' + relevant_exp_months
            candidate.current_ctc = request.form.get('current_ctc')
            candidate.expected_ctc = request.form.get('expected_ctc')
            currency_type_current = request.form['currency_type_current']
            currency_type_except = request.form['currency_type_except']
            candidate.current_ctc = currency_type_current + " " + request.form['current_ctc']
            candidate.expected_ctc = currency_type_except + " " + request.form['expected_ctc']
            candidate.notice_period = request.form.get('notice_period')
            candidate.reason_for_job_change = request.form.get('reason_for_job_change')
            candidate.linkedin_url = request.form.get('linkedin')
            candidate.remarks = request.form.get('remarks')
            candidate.skills = request.form.get('skills')
            candidate.holding_offer = request.form.get('holding_offer')
            candidate.total = request.form.get('total')
            candidate.package_in_lpa = request.form.get('package_in_lpa')
            candidate.period_of_notice = request.form.get('period_of_notice')

            # Handle the resume file upload
            resume_file = request.files['resume']
            if resume_file.filename != '':
                # Save the new resume to the candidate's resume field as bytes
                candidate.resume = resume_file.read()

            holding_offer = request.form.get('holding_offer')
            if holding_offer == 'yes':
                total = request.form.get('total')
                package_in_lpa = request.form.get('package_in_lpa')

                candidate.total = total
                candidate.package_in_lpa = package_in_lpa
            elif holding_offer in ['no', 'pipeline']:
                candidate.total = None
                candidate.package_in_lpa = None

            notice_period = request.form.get('notice_period')
            if notice_period == 'yes':
                last_working_date = request.form['last_working_date']
                buyout = 'buyout' in request.form
                candidate.last_working_date = last_working_date
                candidate.buyout = buyout
            elif notice_period == 'no':
                period_of_notice = request.form['months']
                buyout = 'buyout' in request.form
                candidate.period_of_notice = period_of_notice
                candidate.buyout = buyout
            elif notice_period == 'completed':
                last_working_date = request.form['last_working_date']
                candidate.last_working_date = last_working_date

            db.session.commit()

            return redirect(
                url_for('career_dashboard', page_no=page_no, edit_candidate_message='Candidate Details Edited Successfully'))

        candidate = Candidate.query.get(candidate_id)
        candidate_data = {
            'id': candidate.id,
            'name': candidate.name,
            'mobile': candidate.mobile,
            'email': candidate.email,
            'client': candidate.client,
            'current_company': candidate.current_company,
            'position': candidate.position,
            'profile': candidate.profile,
            'current_job_location': candidate.current_job_location,
            'preferred_job_location': candidate.preferred_job_location,
            'qualifications': candidate.qualifications,
            'experience': candidate.experience,
            'relevant_experience': candidate.relevant_experience,
            'current_ctc': candidate.current_ctc,
            'expected_ctc': candidate.expected_ctc,
            'notice_period': candidate.notice_period,
            'reason_for_job_change': candidate.reason_for_job_change,
            'remarks': candidate.remarks,
            'candidate_status': candidate.status,
            'linkedin_url': candidate.linkedin_url,
            'skills': candidate.skills,
            'resume': candidate.resume,
            'holding_offer': candidate.holding_offer,
            'total': candidate.total,
            'package_in_lpa': candidate.package_in_lpa,
            'last_working_date': candidate.last_working_date,
            'buyout': candidate.buyout,
            'period_of_notice': candidate.period_of_notice,
        }

        return render_template('edit_candidate_careers.html', candidate_data=candidate_data, user_id=user_id,
                               user_type=user_type, user_name=user_name, count_notification_no=count_notification_no,
                               page_no=page_no,career_count_notification_no=career_count_notification_no)

    return redirect(url_for('career_dashboard'))


# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


from flask import send_file

@app.route('/download_resume/<int:candidate_id>')
def download_resume(candidate_id):
    candidate = Candidate.query.get(candidate_id)
    if candidate is None or candidate.resume is None:
        return redirect(url_for('dashboard'))

    # Save the resume file from the database
    resume_file = io.BytesIO(candidate.resume)
    is_pdf = resume_file.getvalue().startswith(b"%PDF")
    if is_pdf : 
        resume_filename = f"{candidate.name}_resume.pdf"  # Set the filename as desired
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        with open(resume_path, 'wb') as file:
            file.write(candidate.resume)

        # Send the saved resume file for download
        return send_file(resume_path, as_attachment=True)
    else:
        resume_filename = f"{candidate.name}_resume.docx"  # Set the filename as desired
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
        with open(resume_path, 'wb') as file:
            file.write(candidate.resume)

        # Send the saved resume file for download
        return send_file(resume_path, as_attachment=True)

# @app.route('/post_job', methods=['GET', 'POST'])
@app.route('/post_job', methods=['POST'])
def post_job():
    try:
        # Accessing the JSON data from the request
        json_data = request.json
        
        # Accessing the "user_name" field from the JSON data
        user_name = json_data.get('user_name')

        # Check if the "user_name" field exists
        if user_name:
            # Continue processing the request
            user_id = json_data.get('user_id')
            user_type = json_data.get('user_type')

            if user_type == 'management':
                if user_type == 'recruiter':
                    recruiter_names = [User.query.get(user_id).name]
                    management = None
                elif user_type == 'management':
                    management = User.query.get(user_id).name
                else:
                    management = None

                # Retrieve other form data from the JSON request
                client = json_data.get('client')
                experience_min = json_data.get('experience_min')
                experience_max = json_data.get('experience_max')
                budget_min = json_data.get('budget_min')
                budget_max = json_data.get('budget_max')
                currency_type_min = json_data.get('currency_type_min')
                currency_type_max = json_data.get('currency_type_max')
                budget_min = currency_type_min + ' ' + budget_min
                budget_max = currency_type_max + ' ' + budget_max  
                location = json_data.get('location')
                shift_timings = json_data.get('shift_timings')
                notice_period = json_data.get('notice_period')
                role = json_data.get('role')
                detailed_jd = json_data.get('detailed_jd')
                mode = json_data.get('mode')
                job_status = json_data.get('job_status')
                job_type = json_data.get('Job_Type')
                skills = json_data.get('skills')

                if job_type == 'Contract':
                    Job_Type_details = json_data.get('Job_Type_details')
                    job_type = job_type + '(' + Job_Type_details + ' Months )'
                else:
                    pass

                filename = None
                jd_binary = None
                if 'jd_pdf' in request.files:
                    jd_file = request.files['jd_pdf']
                    if jd_file and allowed_file(jd_file.filename):
                        # Convert the resume file to binary data
                        jd_binary = jd_file.read()
                        filename = secure_filename(jd_file.filename)
                    else:
                        pass
                else:
                    pass

                recruiter_names = json_data.get('recruiter', [])
                joined_recruiters = ', '.join(recruiter_names)

                new_job_post = JobPost(
                    client=client,
                    experience_min=experience_min,
                    experience_max=experience_max,
                    budget_min=budget_min,
                    budget_max=budget_max,
                    location=location,
                    shift_timings=shift_timings,
                    notice_period=notice_period,
                    role=role,
                    detailed_jd=detailed_jd,
                    jd_pdf = jd_binary,
                    mode=mode,
                    recruiter=joined_recruiters,
                    management=management,
                    job_status=job_status,
                    job_type = job_type,
                    skills=skills
                )
                
                new_job_post.notification = 'no'
                new_job_post.date_created = date.today()
                new_job_post.time_created = datetime.now().time()

                # Define an empty list to hold Notification instances
                notifications = []

                if ',' in joined_recruiters:
                    recruiter_names_lst = joined_recruiters.split(',')
                    for recruiter_name in recruiter_names_lst:
                        notification_status = False
                        notification = Notification(
                            recruiter_name=recruiter_name.strip(),
                            notification_status=notification_status
                        )
                        # Append each Notification instance to the notifications list
                        notifications.append(notification)
                        db.session.add_all(notifications)
                else:
                    recruiter_name = joined_recruiters
                    notification_status = False
                    notification = Notification(
                        recruiter_name=recruiter_name,
                        notification_status=notification_status
                    )
                    # Append each Notification instance to the notifications list
                    db.session.add(notification)

                # Associate the notifications list with the new_job_post object
                new_job_post.notifications = notifications

                # Add the new_job_post and all associated notifications to the session
                db.session.add(new_job_post)
                db.session.commit()

                # Retrieve the email addresses of the recruiters
                recruiter_emails = [recruiter.email for recruiter in User.query.filter(User.name.in_(recruiter_names), User.user_type == 'recruiter',User.is_active == True, User.is_verified == True)]
                for email in recruiter_emails:
                    send_notification(email)

                # Return the job_id along with the success message
                return jsonify({"message": "Job posted successfully", "job_id": new_job_post.id}), 200
            else:
                return jsonify({"error": "Invalid user type"}), 400
        else:
            return jsonify({"error": "Missing 'user_name' field in the request"}), 400

    except KeyError as e:
        return jsonify({"error": f"KeyError: {e}"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/update_job_status/<int:job_id>', methods=['POST'])
def update_job_status(job_id):
    # Retrieve the job post from the database based on the provided job_id
    job_post = JobPost.query.get(job_id)

    if job_post:

        new_job_status = request.form['new_job_status']
        job_post.job_status = new_job_status

        db.session.commit()
        

        return redirect(url_for('view_all_jobs'))
    return "Job post not found"

@app.route('/edit_job_post/<int:job_id>', methods=['GET', 'POST'])
def edit_job_post(job_id):
    # Retrieve the job post from the database based on the provided job_id
    user_name = session['user_name']
    job_post = JobPost.query.get(job_id)

    if job_post:
        if request.method == 'POST':
            # Update the job_status based on the form data submitted
            job_status = request.form['job_status']
            job_post.job_status = job_status

            # Commit the changes to the database
            db.session.commit()

            # Redirect the user to the view_all_jobs route or any other appropriate page
            return redirect(url_for('view_all_jobs', job_id=job_id ,status_message='Job Status Updated Sucessfully'))

        # Render the edit job post form template with the job post data
        return render_template('edit_job_post.html',user_name=user_name, job_post=job_post)

    # Handle the case where the job post with the given job_id is not found
    return "Job post not found"

@app.route('/view_all_jobs', methods=['POST'])
def view_all_jobs():
    # Get data from JSON request
    data = request.json

    # Extract any parameters you need from the JSON data
    user_name = data['username']

    # Retrieve all job posts from the database
    job_posts_active = JobPost.query.filter_by(job_status='Active').order_by(JobPost.id).all()
    job_posts_hold = JobPost.query.filter_by(job_status='Hold').order_by(JobPost.id).all()

    # Construct JSON response
    response_data = {
        "user_name": user_name,
        "job_posts_active": [
            {
                "id": job_post.id,
                "client": job_post.client,
                "role": job_post.role,
                "experience_min": job_post.experience_min,
                "experience_max": job_post.experience_max,
                "budget_min": job_post.budget_min,
                "budget_max": job_post.budget_max,
                "location": job_post.location,
                "shift_timings": job_post.shift_timings,
                "notice_period": job_post.notice_period,
                "detailed_jd": job_post.detailed_jd,
                "jd_pdf": job_post.jd_pdf,  # Assuming this is a binary field containing PDF data
                "mode": job_post.mode,
                "recruiter": job_post.recruiter,
                "management": job_post.management,
                "job_status": job_post.job_status,
                "job_type": job_post.job_type,
                "skills": job_post.skills,
                "date_created": str(job_post.date_created),
                "time_created": str(job_post.time_created)
                # Include other attributes as needed
            }
            for job_post in job_posts_active
        ],
        "job_posts_hold": [
            {
                "id": job_post.id,
                "client": job_post.client,
                "role": job_post.role,
                "experience_min": job_post.experience_min,
                "experience_max": job_post.experience_max,
                "budget_min": job_post.budget_min,
                "budget_max": job_post.budget_max,
                "location": job_post.location,
                "shift_timings": job_post.shift_timings,
                "notice_period": job_post.notice_period,
                "detailed_jd": job_post.detailed_jd,
                "jd_pdf": job_post.jd_pdf,  # Assuming this is a binary field containing PDF data
                "mode": job_post.mode,
                "recruiter": job_post.recruiter,
                "management": job_post.management,
                "job_status": job_post.job_status,
                "job_type": job_post.job_type,
                "skills": job_post.skills,
                "date_created": str(job_post.date_created),
                "time_created": str(job_post.time_created)
                # Include other attributes as needed
            }
            for job_post in job_posts_hold
        ]
    }

    # Return JSON response
    return jsonify(response_data)

def send_notification(recruiter_email):
    msg = Message('New Job Posted', sender='saiganeshkanuparthi@gmail.com', recipients=[recruiter_email])
    msg.body = 'A new job has been posted. Check your dashboard for more details.'
    mail.send(msg)

@app.route('/other_job_posts', methods=['GET'])
def other_job_posts():
    if 'user_id' in session and 'user_type' in session:
        if session['user_type'] == 'recruiter':
            # Retrieve the logged-in user's ID from the session
            user_id = session['user_id']

            # Retrieve the recruiter's name based on user ID
            recruiter_name = User.query.get(user_id).name

            job_posts = JobPost.query.filter(JobPost.recruiter != recruiter_name).distinct(JobPost.client).all()

            return render_template('other_job_posts.html', job_posts=job_posts)

    # Redirect or render an appropriate page if the conditions are not met
    return redirect(url_for('login'))

@app.route('/recruiter_job_posts', methods=['GET'])
def recruiter_job_posts():
    no_doc_message = request.args.get('no_doc_message')
    if 'user_id' in session and 'user_type' in session:
        if session['user_type'] == 'recruiter':
            # Retrieve the logged-in user's ID from the session
            user_id = session['user_id']
            user_name = session['user_name']
            count_notification_no = Notification.query.filter(Notification.notification_status == 'false',
                                                              Notification.recruiter_name == user_name).count()
            career_count_notification_no = Career_notification.query.filter(Career_notification.notification_status == 'false',
                                                              Career_notification.recruiter_name == user_name).count()
            recruiter_name = User.query.get(user_id).name

            job_posts = JobPost.query.filter(JobPost.recruiter.contains(recruiter_name),
                                             JobPost.job_status == 'Active').order_by(JobPost.id).all()
            job_posts_hold = JobPost.query.filter(JobPost.recruiter.contains(recruiter_name),
                                                  JobPost.job_status == 'Hold').order_by(JobPost.id).all()

            notifications = Notification.query.filter(Notification.recruiter_name.contains(recruiter_name)).all()

            for notification in notifications:
                if notification.notification_status == False:
                    notification.notification_status = True
                    db.session.commit()

            # for job_post in job_posts:
            #     if job_post.notification == 'no':
            #         job_post.notification = 'yes'
            #         db.session.commit()

            return render_template('recruiter_job_posts.html', count_notification_no=count_notification_no,
                                   job_posts=job_posts, user_name=user_name, job_posts_hold=job_posts_hold,
                                   redirect_url=url_for('add_candidate'), recruiter_job_posts=recruiter_job_posts,
                                   no_doc_message=no_doc_message, career_count_notification_no=career_count_notification_no)

    return redirect(url_for('login'))

import io

@app.route('/view_resume/<int:candidate_id>', methods=['GET'])
def view_resume(candidate_id):
    # Retrieve the resume data from the database using SQLAlchemy
    candidate = Candidate.query.filter_by(id=candidate_id).first()

    if not candidate:
        return 'Candidate not found'

    # Create a file-like object (BytesIO) from the resume data
    resume_file = io.BytesIO(candidate.resume)
    is_pdf = resume_file.getvalue().startswith(b"%PDF")

    if is_pdf:
        return send_file(
            resume_file,
            mimetype='application/pdf',
            as_attachment=False
        )
    else:
        return send_file(
            resume_file,
            mimetype='application/msword',
            as_attachment=False
        )


@app.route('/viewfull_jd/<int:id>')
def viewfull_jd(id):
    user_type = session['user_type']
    job_post = JobPost.query.get(id)
    return render_template('viewfull_jd.html', job_post=job_post,user_type=user_type)

@app.route('/add_candidate_view')
def add_candidate_view():
    user_id = session['user_id']
    user_type = session['user_type']
    user_name = session['user_name']

    if user_type == 'recruiter':
        recruiter = User.query.filter_by(id=user_id, user_type='recruiter').first()
        if recruiter:
            candidates = Candidate.query.filter_by(
                recruiter=recruiter.name).all()  # Filter candidates by recruiter's name
            # data = json.dumps(candidates, sort_keys=False)
            results = db.session.query(JobPost.client, JobPost.recruiter).filter(
                JobPost.recruiter.contains(user_name)).all()
            client_names = sorted(list(set([result.client for result in results])))
            count_notification_no = Notification.query.filter(Notification.notification_status == 'false',
                                                              Notification.recruiter_name == user_name).count()
            return render_template('add_candidate_view.html', user=recruiter, user_type=user_type, user_name=user_name,
                                   candidates=candidates, count_notification_no=count_notification_no,
                                   client_names=client_names)
    elif user_type == 'management':
        users = User.query.all()
        candidates = Candidate.query.all()
        JobsPosted = JobPost.query.all()
        clients = db.session.query(JobPost.client).all()
        client_names = list(set([client[0] for client in clients]))

        return render_template('add_candidate_view.html', users=users, user_type=user_type, user_name=user_name,
                               JobsPosted=JobsPosted, client_names=client_names)

import os
import shutil
from flask import Flask, request, send_file, redirect, url_for
from zipfile import ZipFile

@app.route('/download_resumes')
def download_resumes():
    candidate_ids = request.args.getlist('candidate_ids')
    
    # Create a temporary directory to store resume files
    temp_dir = 'temp_resumes'
    os.makedirs(temp_dir, exist_ok=True)
    
    resume_paths = []

    for candidate_id in candidate_ids:
        candidate = Candidate.query.get(candidate_id)
        if candidate is None or candidate.resume is None:
            continue
        
        resume_file = io.BytesIO(candidate.resume)
        is_pdf = resume_file.getvalue().startswith(b"%PDF")
        if is_pdf : 
            resume_filename = f"{candidate.name}_resume.pdf" 
            resume_path = os.path.join(temp_dir, resume_filename)
            with open(resume_path, 'wb') as file:
                file.write(candidate.resume)
            
            resume_paths.append(resume_path)
        else:
            resume_filename = f"{candidate.name}_resume.docx" 
            resume_path = os.path.join(temp_dir, resume_filename)
            with open(resume_path, 'wb') as file:
                file.write(candidate.resume)
            
            resume_paths.append(resume_path)

    # Create a zip file containing all resume files
    zip_filename = 'resumes.zip'
    with ZipFile(zip_filename, 'w') as zipf:
        for resume_path in resume_paths:
            zipf.write(resume_path, os.path.basename(resume_path))
    
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
    
    # Send the zip file for download
    return send_file(zip_filename, as_attachment=True)


@app.route('/assign_job/<int:job_id>', methods=['GET','POST'])
def assign_job(job_id):
    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = None

    if 'user_id' in session and 'user_type' in session and session['user_type'] == 'management':
        job_post = JobPost.query.get(job_id)  # Retrieve the job post by its ID

        if not job_post:
            return jsonify({"error_message": "Job not found"}), 404

        current_recruiters = job_post.recruiter.split(', ') if job_post.recruiter else []

        if request.method == 'POST':
            new_recruiter_names = request.json.get('recruiters', [])
            all_recruiter_names = current_recruiters + new_recruiter_names
            joined_recruiters = ', '.join(all_recruiter_names)
            job_post.recruiter = joined_recruiters
            db.session.commit()

            # Send notification emails to the newly assigned recruiters
            new_recruiter_emails = [recruiter.email for recruiter in
                                    User.query.filter(User.name.in_(new_recruiter_names),
                                                      User.user_type == 'recruiter')]
            for email in new_recruiter_emails:
                send_notification(email)

            # Define an empty list to hold Notification instances
            notifications = []

            if ',' in joined_recruiters:
                recruiter_names_lst = joined_recruiters.split(',')
                for recruiter_name in recruiter_names_lst:
                    if recruiter_name.strip() in new_recruiter_names:
                        notification_status = False  # Set the initial status
                        notification = Notification(
                            recruiter_name=recruiter_name.strip(),
                            notification_status=notification_status
                        )
                        # Append each Notification instance to the notifications list
                        notifications.append(notification)
            else:
                recruiter_name = joined_recruiters
                if recruiter_name in new_recruiter_names:
                    notification_status = False  # Set the initial status
                    notification = Notification(
                        recruiter_name=recruiter_name,
                        notification_status=notification_status
                    )
                    # Append each Notification instance to the notifications list
                    notifications.append(notification)

            # Commit the notifications to the database session
            db.session.add_all(notifications)
            db.session.commit()
            return jsonify({"message": "Job re-assigned successfully"}), 200

        recruiter_names = [recruiter.name for recruiter in User.query.filter_by(user_type='recruiter')]
        return jsonify({
            "user_name": user_name,
            "job_post": job_post.serialize(),
            "current_recruiters": current_recruiters,
            "recruiters": recruiter_names
        })

    return jsonify({"error_message": "Unauthorized: You must log in as management user to access this page"}), 401


@app.route('/assign_candidate', methods=['POST'])
def assign_candidate():
    assignment_message = request.args.get('assignment_message')
    if 'user_id' in session and 'user_type' in session and session['user_type'] == 'management':
        user_name = session['user_name']
        recruiters = User.query.filter_by(user_type='recruiter').all()

        selected_recruiter_id = request.json.get('selected_recruiter_id')
        selected_candidate_id = request.json.get('selected_candidate_id')
        assign_recruiter_id = request.json.get('assign_recruiter_id')
        assign_candidate_id = request.json.get('assign_candidate_id')

        selected_recruiter = None
        selected_candidate = None
        assigned_recruiter = None

        if selected_recruiter_id:
            selected_recruiter = User.query.get(selected_recruiter_id)

        if selected_candidate_id:
            selected_candidate = Candidate.query.get(selected_candidate_id)

        if assign_recruiter_id:
            assigned_recruiter = User.query.get(assign_recruiter_id)

        if request.method == 'POST':
            selected_candidate_ids = request.json.get('selected_candidate_ids')
            if assigned_recruiter and selected_candidate_ids:
                for candidate_id in selected_candidate_ids:
                    candidate = Candidate.query.get(candidate_id)
                    if candidate:
                        candidate.recruiter = assigned_recruiter.name
                db.session.commit()
                return jsonify({"message": "Candidates Assigned Successfully"}), 200

            if selected_candidate_id:
                selected_candidate = Candidate.query.get(selected_candidate_id)

        candidates = []
        if selected_recruiter:
            candidates = Candidate.query.filter(
                Candidate.recruiter == selected_recruiter.name,
                Candidate.status.in_(['None', "SCREENING","L1 - SCHEDULED" ,"L1 - SELECTED", 'L1 - FEEDBACK', 'L1 - RESCHEDULE',"L2 - SCHEDULED" ,"L2 - SELECTED",
                                      'L2 - FEEDBACK', 'L2 - RESCHEDULE', 'HOLD(POSITION)', 'CANDIDATE HOLD', 'OFFERED',
                                      "L2 - SELECTED"])
            ).all()
        return jsonify({
            "recruiters": [recruiter.serialize() for recruiter in recruiters],
            "candidates": [candidate.serialize() for candidate in candidates],
            "selected_recruiter": selected_recruiter.serialize() if selected_recruiter else None,
            "selected_candidate": selected_candidate.serialize() if selected_candidate else None,
            "assigned_recruiter": assigned_recruiter.serialize() if assigned_recruiter else None,
            "assignment_message": assignment_message,
            "user_name": user_name
        })

    return jsonify({"error_message": "Unauthorized: You must log in as management user to access this page"}), 401


@app.route('/disable_user', methods=['GET', 'POST'])
def disable_user():
    user_name = session['user_name']
    if request.method == 'POST':
        username = request.form.get('user_name')
        user = User.query.filter_by(username=username).first()

        if user is None:
            return render_template('deactivate_user.html', message='User not found', active_users=User.query.filter_by(is_active=True).all())

        user.is_active = False
        db.session.commit()

        return render_template('deactivate_user.html', message='User deactivated successfully',user_name=user_name, active_users=User.query.filter_by(is_active=True).all())

    return render_template('deactivate_user.html', message='', active_users=User.query.filter_by(is_active=True).all(),user_name=user_name)

@app.route('/active_users', methods=['POST'])
def update_user_status():
    data = request.json
    username = data.get('user_name')
    new_status = data.get('new_status')

    try:
        user = User.query.filter_by(username=username).first()
        if user:
            user.is_verified = new_status
            db.session.commit()

            # Fetch updated active users list
            active_users_manager = User.query.filter_by(is_active=True, user_type='management').all()
            active_users_manager = sorted(active_users_manager, key=lambda user: user.id)
            active_users_recruiter = User.query.filter_by(is_active=True, user_type='recruiter').all()
            active_users_recruiter = sorted(active_users_recruiter, key=lambda user: user.id)

            return jsonify({
                "message": "User status updated successfully",
                "username": username,
                "active_users_manager": [user.serialize() for user in active_users_manager],
                "active_users_recruiter": [user.serialize() for user in active_users_recruiter]
            })
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        db.session.rollback()  # Rollback changes in case of error
        return jsonify({"message": "Error updating user status", "error": str(e)}), 500

        
@app.route('/verify_checkbox', methods=['POST'])
def verify_checkbox():
    data = request.json
    user_id = data.get('userId')
    checked = data.get('checked')
    user = User.query.get(user_id)
    user.is_verified = checked
    db.session.commit()
    return redirect(url_for('active_users'))

@app.route('/change_password', methods=['GET','POST'])
def change_password():
    if 'user_name' in session and 'user_type' in session and 'username' in session:
        user_name = session['user_name']
        user_type = session['user_type']
        username = session['username']

        data = request.json

        if data:
            form_username = data.get('username')
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')

            if username == form_username:
                user = User.query.filter_by(username=username).first()

                if user and user.password == old_password:
                    if new_password == confirm_password:
                        # Update the user's password in the database
                        user.password = new_password
                        db.session.commit()
                        if user_type == 'management':
                            return jsonify({"message": "Password changed successfully."})
                        else:
                            return jsonify({"message": "Password changed successfully."})
                    else:
                        return jsonify({"error": "New password and confirm password do not match."}), 400
                else:
                    return jsonify({"error": "Invalid username or old password."}), 400
            else:
                return jsonify({"error": "Logged in user does not match the provided username."}), 400
        else:
            return jsonify({"error": "No JSON data provided."}), 400

    else:
        return jsonify({"error": "Unauthorized: You must log in to access this page"}), 401
    


@app.route('/delete_job_post_message/<int:job_id>')
def delete_job_post_message(job_id):
    job_post = JobPost.query.get(job_id)
    id = job_post.id
    client = job_post.client
    role = job_post.role
    return redirect(url_for('view_all_jobs',client=client,role=role,id=id))

@app.route('/delete_job_post/<int:job_id>', methods=['POST'])
def delete_job_post(job_id):
    # data=request.json
    # job_id=data['job_id']
    job_post = JobPost.query.get(job_id)
    if job_post:
        JobPost.query.filter_by(id=job_id).delete()
        db.session.commit()
        return jsonify({"message": "Job Post Deleted Successfully"}), 200
    else:
        return jsonify({"error": "Job Post not found"}), 404

@app.route('/download_jd/<int:job_id>')
def download_jd(job_id):
    jobpost = JobPost.query.get(job_id)
    if jobpost is None or jobpost.jd_pdf is None:
        return redirect(url_for('dashboard'))

    # Save the resume file from the database
    jd_file = io.BytesIO(jobpost.jd_pdf)
    is_pdf = jd_file.getvalue().startswith(b"%PDF")
    if is_pdf : 
        jd_filename = f"{jobpost.client}_jd.pdf"  # Set the filename as desired
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
        with open(jd_path, 'wb') as file:
            file.write(jobpost.jd_pdf)

        # Send the saved resume file for download
        return send_file(jd_path, as_attachment=True)
    else:
        jd_filename = f"{jobpost.client}_jd.docx"  # Set the filename as desired
        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_filename)
        with open(jd_path, 'wb') as file:
            file.write(jobpost.jd_pdf)

        # Send the saved resume file for download
        return send_file(jd_path, as_attachment=True)


@app.route('/view_jd/<int:job_id>', methods=['GET'])
def view_jd(job_id):
    # Retrieve the resume data from the database using SQLAlchemy
    user_type = session['user_type']
    jobpost = JobPost.query.filter_by(id=job_id).first()
    if not jobpost:
        return 'Candidate not found'

    # Create a file-like object (BytesIO) from the resume data
    jd_file = io.BytesIO(jobpost.jd_pdf)
    is_pdf = jd_file.getvalue().startswith(b"%PDF")

    if jobpost.jd_pdf:
        if is_pdf:
            return send_file(
                jd_file,
                mimetype='application/pdf',
                as_attachment=False
            )
        else:
            return send_file(
                jd_file,
                mimetype='application/msword',
                as_attachment=False
            )
    if user_type == 'recruiter':
        return redirect(url_for('recruiter_job_posts',no_doc_message = 'No Document Available to View'))
    else:
        return redirect(url_for('view_all_jobs',no_doc_message = 'No Document Available to View'))
    

from flask import Flask, request, Response, render_template
import pandas as pd
from datetime import datetime
import openpyxl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@app.route('/generate_excel', methods=['GET','POST'])
def generate_excel():
    data = request.json

    message = data.get('message')
    user_name = data.get('user_name')

    if data.get('action') == 'View Reports':
        from_date_str = data.get('from_date')
        to_date_str = data.get('to_date')
        user_name = data.get('additional_value')

        try:
            from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
            to_date = datetime.strptime(to_date_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD format.'})

        recruiter_names = data.get('recruiter_names')

        if not recruiter_names:
            return jsonify({'error': 'Please Select any Recruiter'})

        session = Session()
        query = session.query(Candidate).filter(
            Candidate.recruiter.in_(recruiter_names),
            Candidate.date_created >= from_date,
            Candidate.date_created <= to_date
        )

        date_range = [from_date + timedelta(days=i) for i in range((to_date - from_date).days + 1)]

        data = []
        for candidate in query:
            data.append({
                "recruiter": candidate.recruiter,
                "date_created": candidate.date_created.strftime("%d-%m-%Y"),
            })

        complete_data = []
        for recruiter_name in recruiter_names:
            for date in date_range:
                complete_data.append({"recruiter": recruiter_name, "date_created": date.strftime("%d-%m-%Y")})

        complete_df = pd.DataFrame(complete_data)

        merged_df = pd.concat([pd.DataFrame(data), complete_df]).fillna(0)

        grouped = merged_df.groupby(['recruiter', 'date_created']).size().reset_index(name='count')

        grouped['date_created'] = pd.to_datetime(grouped['date_created'], format="%d-%m-%Y")

        # Sort the grouped DataFrame by 'date_created'
        grouped = grouped.sort_values(by='date_created')

        grouped['date_created'] = grouped['date_created'].dt.strftime("%Y-%m-%d")

        pivot_table = grouped.pivot_table(index='recruiter', columns='date_created', values='count', aggfunc='sum',
                                          fill_value=0, margins=True, margins_name='Grand Total')

        styled_pivot_table = pivot_table.copy()

        styled_pivot_table.iloc[:-1, :-1] = styled_pivot_table.iloc[:-1, :-1].applymap(
            lambda x: x - 1 if isinstance(x, int) else x)

        recruiter_sums = styled_pivot_table.iloc[:-1, :-1].sum(axis=1)
        date_sums = styled_pivot_table.iloc[:-1, :-1].sum()

        true_grand_total = recruiter_sums.sum()

        styled_pivot_table.iloc[-1, :-1] = date_sums
        styled_pivot_table.iloc[:-1, -1] = recruiter_sums
        styled_pivot_table.at['Grand Total', 'Grand Total'] = true_grand_total

        recruiters = session.query(User).filter_by(user_type='recruiter').all()
        recruiters = [recruiter.name for recruiter in recruiters]

        styled_pivot_table_json = styled_pivot_table.to_json()

        return jsonify({
            'recruiters': recruiters,
            'styled_pivot_table': styled_pivot_table_json,
            'user_name': user_name,
            'message': message,
            'from_date_str': from_date_str,
            'to_date_str': to_date_str
        })

    elif data.get('action') == 'Generate Report':
        # Handle 'Generate Report' action if needed
        pass

    # Return a default response if no action matches
    return jsonify({'error': 'Invalid action'})


def re_send_notification(recruiter_email, job_id):
    msg = Message('Job Update Notification', sender='saich5252@gmail.com', recipients=[recruiter_email])
    msg.body = f'Hello,\n\nThe job post with ID {job_id} has been updated.\n\nPlease check your dashboard for more details.'
    mail.send(msg)

@app.route('/edit_post_job/<int:job_id>/<int:page_no>', methods=['GET', 'POST'])
def edit_post_job(job_id,page_no):
    job_message = request.args.get('job_message')
    user_name = session.get('user_name')

    # Retrieve the job post from the database based on the job_id
    job_post = JobPost.query.get(job_id)

    if 'user_id' in session and 'user_type' in session:
        if session['user_type'] == 'management' and job_post:
            if request.method == 'POST':
                # Extract and process form data
                client = request.form['client']
                experience_min = request.form['experience_min']
                experience_max = request.form['experience_max']
                budget_min = request.form['budget_min']
                budget_max = request.form['budget_max']
                currency_type_min = request.form['currency_type_min']
                currency_type_max = request.form['currency_type_max']
                budget_min = currency_type_min + ' ' + budget_min
                budget_max = currency_type_max + ' ' + budget_max
                location = request.form['location']
                shift_timings = request.form['shift_timings']
                notice_period = request.form['notice_period']
                role = request.form['role']
                detailed_jd = request.form['detailed_jd']
                mode = request.form['mode']
                job_status = request.form['job_status']
                job_type = request.form.get('job_type', '')
                skills = request.form['skills']
                
                jd_pdf_file = request.files['jd_pdf']
                jd_pdf_binary = job_post.jd_pdf if job_post.jd_pdf else b''
                if jd_pdf_file.filename != '':
                    jd_pdf_binary = jd_pdf_file.read()

                if job_type == 'Contract':
                    job_type_details = request.form.get('job_type_details', '')
                    job_type = f"{job_type} ({job_type_details} Months)"

                # Update the job post attributes
                job_post.client = client
                job_post.experience_min = experience_min
                job_post.experience_max = experience_max
                job_post.budget_min = budget_min
                job_post.budget_max = budget_max
                job_post.location = location
                job_post.shift_timings = shift_timings
                job_post.notice_period = notice_period
                job_post.role = role
                job_post.detailed_jd = detailed_jd
                job_post.mode = mode
                job_post.job_status = job_status
                job_post.job_type = job_type
                job_post.skills = skills
                job_post.jd_pdf = jd_pdf_binary

                # Update associated notifications if needed
                recruiter_names = request.form.getlist('recruiter[]')
                joined_recruiters = ', '.join(recruiter_names)
                job_post.recruiter = joined_recruiters

                # Clear existing notifications and update with new ones
                job_post.notifications = []
                notifications = []
                for recruiter_name in recruiter_names:
                    notification_status = False
                    notification = Notification(
                        recruiter_name=recruiter_name.strip(),
                        notification_status=notification_status
                    )
                    notifications.append(notification)
                    db.session.add(notification)
                job_post.notifications = notifications

                # Commit changes to the database
                db.session.commit()

                # Send email notifications to recruiters
                recruiter_emails = [recruiter.email for recruiter in User.query.filter(User.name.in_(recruiter_names), User.user_type == 'recruiter',User.is_active == True, User.is_verified == True)]
                for email in recruiter_emails:
                    re_send_notification(email,job_id)

                return redirect(url_for('view_all_jobs', job_id=job_post.id, page_no=page_no ,job_message='Job updated successfully'))

            # Prepare data for rendering the edit_job_post.html template
            recruiter_names = [recruiter.name for recruiter in User.query.filter_by(user_type='recruiter', is_active=True, is_verified=True)]
            clients = db.session.query(JobPost.client).all()
            client_names = list(set([client[0] for client in clients]))
            return render_template('post_job_edit.html',
                                   recruiter_names=recruiter_names,
                                   user_name=user_name,
                                   client_names=client_names,
                                   job_post=job_post,
                                   job_message=job_message)

    return redirect(url_for('dashboard'))
    
@app.route('/get_candidate_data')
def get_candidate_data():
    candidates = Candidate.query.all()
    candidate_data = []
    for candidate in candidates:
        candidate_data.append({
            'id': candidate.id,
            'name': candidate.name,
            'email': candidate.email,
            'client': candidate.client,
            'current_company':candidate.current_company,
            'position': candidate.position,
            'profile': candidate.profile,
            'current_job_location':candidate.current_job_location,
            'preferred_job_location':candidate.preferred_job_location,
            'skills':candidate.skills,
            'status':candidate.status,
        })
    return jsonify(candidate_data)


@app.route('/send_email', methods=['POST'])
def send_email():
    recipient_email = request.form.get('recipient_email')

    if not recipient_email:
        flash('Recipient email is required.', 'error')
        return redirect(url_for('careers'))

    # Create a link to the page you want to send
    page_link = 'http://127.0.0.1:5001/careers'  # Replace with the actual link

    # Create the email content with a hyperlink
    email_content = f"Click the link below to view active job posts: <a href='{page_link}'>{page_link}</a>"

    # Create an email message
    message = Message('Active Job Posts', sender='saiganeshkanuparthi@gmail.com', recipients=[recipient_email])
    message.html = email_content

    # Send the email
    mail.send(message)

    flash('Email sent successfully!', 'success')
    return redirect(url_for('careers'))

#new
@app.route('/careers', methods=['GET'])
def careers():
    user_type = session.get('user_type', None)
    is_logged_in = 'user_id' in session
    candidate_message = request.args.get('candidate_message')
    print(candidate_message)

    # Query the database to retrieve active job posts and sort them by date_created in descending order
    active_jobs = JobPost.query.filter_by(job_status='Active').order_by(JobPost.date_created.desc()).all()

    return render_template('careers.html', jobs=active_jobs, user_type=user_type, is_logged_in=is_logged_in,candidate_message=candidate_message)

#new
@app.route('/apply_careers', methods=['GET', 'POST'])
def apply_careers():
    user_id = session.get('user_id')
    if not user_id:
        # User is not authenticated, you can redirect them to a login page or take appropriate action
        return redirect(url_for('career_login'))
    user = Career_user.query.get(user_id)
    if request.method == 'GET':
        job_id = request.args.get('job_id')
        client = request.args.get('client')
        profile = request.args.get('profile')
        name = user.name
        email = user.email

        if job_id:
            matching_job_post = JobPost.query.filter(and_(JobPost.id == job_id, JobPost.job_status == 'Hold')).first()
            if matching_job_post:
                return render_template('job_on_hold.html')
        
        job_post = JobPost.query.get(job_id)
        experience_min = job_post.experience_min

        job_ids = db.session.query(JobPost.id).filter(JobPost.client == client, JobPost.job_status == 'Active').all()
        job_roles = db.session.query(JobPost.role).filter(JobPost.client == client).all()

        ids = [job_id[0] for job_id in job_ids]
        roles = [job_role[0] for job_role in job_roles]

        candidate_data = None
        if 'candidate_data' in request.args:
            candidate_data = ast.literal_eval(request.args['candidate_data'])

        return render_template('apply_careers.html', candidate_data=candidate_data, job_id=job_id,
                               client=client, profile=profile, ids=ids, roles=roles,
                               name=name, email=email,experience_min=experience_min)

    if request.method == 'POST':
        try:
            job_id = request.form['job_id']
            name = request.form['name']
            mobile = request.form['mobile']
            email = request.form['email']
            client = request.form['client']
            profile = request.form['profile']
            skills = request.form['skills']

            # Ensure client and job_id are integers
            job_id = int(job_id)

            # Check if the job post is active
            matching_job_post = JobPost.query.filter(and_(JobPost.id == job_id, JobPost.job_status == 'Active')).first()
            if not matching_job_post:
                return render_template('job_on_hold.html')

            # Handle other form fields...
            current_company = request.form['current_company']
            position = request.form['position']
            current_job_location = request.form['current_job_location']
            preferred_job_location = request.form['preferred_job_location']
            qualifications = request.form['qualifications']
            experience = request.form['experience']
            exp_months = request.form['exp_months']
            experience = experience + '.' + exp_months
            relevant_experience = request.form['relevant_experience']
            relevant_exp_months = request.form['relevant_exp_months']
            relevant_experience = relevant_experience + '.' + relevant_exp_months
            currency_type_current = request.form['currency_type_current']
            currency_type_except = request.form['currency_type_except']
            current_ctc = currency_type_current + " " + request.form['current_ctc']
            expected_ctc = currency_type_except + " " + request.form['expected_ctc']
            linkedin = request.form['linkedin']

            # Handle file upload
            filename = None
            resume_binary = None
            if 'resume' in request.files:
                resume_file = request.files['resume']
                if resume_file and allowed_file(resume_file.filename):
                    # Convert the resume file to binary data
                    resume_binary = resume_file.read()
                    filename = secure_filename(resume_file.filename)
                else:
                    return render_template('apply_careers.html', error_message='Invalid file extension')

            notice_period = request.form['notice_period']
            last_working_date = None
            buyout = False
            period_of_notice = None

            if notice_period == 'yes':
                last_working_date = request.form['last_working_date']
                buyout = 'buyout' in request.form
            elif notice_period == 'no':
                period_of_notice = request.form['months']
                buyout = 'buyout' in request.form
            elif notice_period == 'completed':
                last_working_date = request.form['last_working_date']

            holding_offer = request.form['holding_offer']

            if holding_offer == 'yes':
                total = request.form['total']
                if total == '':
                    total = 0
                else:
                    total = int(request.form['total'])
                package_in_lpa = request.form['package_in_lpa']
                if package_in_lpa == '':
                    package_in_lpa = 0
                else:
                    package_in_lpa = float(request.form['package_in_lpa'])
            else:
                total = None
                package_in_lpa = None

            reason_for_job_change = request.form.get('reason_for_job_change')
            remarks = request.form.get('remarks')

            reference = request.form['reference']
            reference_name = None
            reference_position = None
            reference_information = None

            if reference == 'yes':
                reference_name = request.form['reference_name']
                reference_position = request.form['reference_position']
                reference_information = request.form['reference_information']
            elif reference == 'no':
                reference_name = None
                reference_position = None
                reference_information = None

            existing_candidate = Candidate.query.filter(
                and_(Candidate.profile == profile, Candidate.client == client, Candidate.email == email,
                     Candidate.mobile == mobile)).first()
            if existing_candidate:
                return render_template('candidate_exists.html',
                                       error_message='Candidate with the same profile and client already exists')

            # Create a new Candidate object
            new_candidate = Candidate(
                job_id=job_id,
                name=name,
                mobile=mobile,
                email=email,
                client=client,
                current_company=current_company,
                position=position,
                profile=profile,
                resume=resume_binary,
                current_job_location=current_job_location,
                preferred_job_location=preferred_job_location,
                qualifications=qualifications,
                experience=experience,
                relevant_experience=relevant_experience,
                current_ctc=current_ctc,
                expected_ctc=expected_ctc,
                notice_period=notice_period,
                last_working_date=last_working_date if notice_period == 'yes' or notice_period == 'completed' else None,
                buyout=buyout,
                holding_offer=holding_offer,
                total=total,
                package_in_lpa=package_in_lpa,
                linkedin_url=linkedin,
                reason_for_job_change=reason_for_job_change,
                status='None',
                remarks=remarks,
                skills=skills,
                period_of_notice=period_of_notice,
                reference=reference,
                reference_name=reference_name,
                reference_position=reference_position,
                reference_information=reference_information
            )

            new_candidate.date_created = date.today()
            new_candidate.time_created = datetime.now().time()

            # Commit the new candidate to the database
            db.session.add(new_candidate)
            db.session.commit()

            try:
                msg = Message('Successful Submission of Your Job Application', sender='saich5252@gmail.com', recipients=[email])
                msg.body = f"Dear { name },\n Congratulations! Your job application has been successfully submitted for the position at {client} for the role of {profile}. We appreciate your interest in joining our team.\n\n  Our dedicated recruiter will review your application, and you can expect to hear from us within the next 24 hours.\n\nBest wishes for your application process!\n\n Regards, \n\nTeam\nMakonis Talent Track Pro\nrecruiterpro@makonissoft.com\n"
                mail.send(msg)
            except Exception as e:
                # Handle email sending errors, log the error
                return render_template('error.html', error_message=f"Error sending thank-you email: {str(e)}")

            return redirect(url_for('careers', candidate_message='Candidate Added Successfully'))

        except Exception as e:
            # Handle any exceptions here (e.g., log the error, return an error page)
            return render_template('error.html', error_message=str(e))

    return redirect(url_for('careers'))


#new
# User Login
@app.route('/career_login', methods=['GET', 'POST'])
def career_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Career_user.query.filter_by(username=username, password=password).first()

        if user:
            # Store the user's session or token
            session['user_id'] = user.id
            return redirect(url_for('careers'))

    return render_template('career_login.html')

#new
@app.route('/career_logout')
def career_logout():
    # Clear the user's session
    session.pop('user_id', None)
    return redirect(url_for('careers'))

#new
@app.route('/career_register', methods=['GET', 'POST'])
def career_register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Create a new user and add it to the database
        new_user = Career_user(username=username, name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('career_login'))

    return render_template('career_registration.html')

#new
@app.route('/career_dashboard')
def career_dashboard():
    edit_candidate_message = request.args.get('edit_candidate_message')
    if 'user_id' in session and 'user_type' in session:
        page_no = request.args.get('page_no')
        candidate_message = request.args.get('candidate_message')
        signup_message = request.args.get('signup_message')
        job_message = request.args.get('job_message')
        update_candidate_message = request.args.get('update_candidate_message')
        delete_message = request.args.get("delete_message")

        user_id = session['user_id']
        user_type = session['user_type']
        user_name = session['user_name']

        if user_type == 'management':
            users = User.query.all()
            candidates = Candidate.query.filter((Candidate.reference.is_not(None))).all()
            candidates = sorted(candidates, key=lambda candidate: candidate.id)
            JobsPosted = JobPost.query.all()
            # data = json.dumps(candidates, sort_keys=False)
            return render_template('career_dashboard.html', users=users, user_type=user_type, user_name=user_name,
                                   candidates=candidates, update_candidate_message=update_candidate_message,
                                   candidate_message=candidate_message, delete_message=delete_message,
                                   JobsPosted=JobsPosted, signup_message=signup_message, job_message=job_message,
                                   page_no=page_no, edit_candidate_message=edit_candidate_message)
        elif user_type == 'recruiter':
            recruiter = User.query.filter_by(id=user_id, user_type='recruiter').first()
            recruiter_name = User.query.get(user_id).name
            if recruiter:
                candidates = Candidate.query.filter(and_(Candidate.recruiter == recruiter.name,
                                                         Candidate.reference.is_not(None))).all()
                candidates = sorted(candidates, key=lambda candidate: candidate.id)
                career_count_notification_no = Career_notification.query.filter(Career_notification.notification_status == 'false',
                                                                  Career_notification.recruiter_name == user_name).count()
                career_notifications = Career_notification.query.filter(
                    Career_notification.recruiter_name.contains(recruiter_name)).all()

                for career_notification in career_notifications:
                    if career_notification.notification_status == False:
                        career_notification.notification_status = True
                        db.session.commit()
                return render_template('career_dashboard.html', user=recruiter, user_type=user_type, user_name=user_name,
                                       candidates=candidates, candidate_message=candidate_message,
                                       update_candidate_message=update_candidate_message,
                                       career_count_notification_no=career_count_notification_no,
                                       edit_candidate_message=edit_candidate_message, page_no=page_no)
        else:
            user = User.query.filter_by(id=user_id).first()
            if user:
                candidates = Candidate.query.filter_by(recruiter=user.name).all()  # Filter candidates by user's name
                return render_template('career_dashboard.html', user=user, user_type=user_type, candidates=candidates)

    return redirect(url_for('index'))

#new
@app.route('/website_candidate_assign', methods=['GET', 'POST'])
def website_candidate_assign():
    assignment_message = request.args.get('assignment_message')
    if 'user_id' in session and 'user_type' in session and session['user_type'] == 'management':
        user_name = session['user_name']
        recruiters = User.query.filter_by(user_type='recruiter').all()

        if request.method == 'POST':
            assign_recruiter_id = request.form.get('assign_recruiter_id')
            selected_candidate_ids = request.form.getlist('selected_candidate_ids')

            if assign_recruiter_id and selected_candidate_ids:
                assigned_recruiter = User.query.get(assign_recruiter_id)
                if assigned_recruiter:
                    # Fetch selected candidates by their IDs
                    candidates = Candidate.query.filter(
                        Candidate.id.in_(selected_candidate_ids),
                        Candidate.recruiter.is_(None),
                        Candidate.management.is_(None)
                    ).all()

                    for candidate in candidates:
                        # Assign the selected recruiter to the candidate
                        candidate.recruiter = assigned_recruiter.name
                        # Send an email to the assigned recruiter
                        send_career_email(assigned_recruiter.email, 'Alert! New Candidate Assignment ',
                                          f'Dear {assigned_recruiter.name}\n\n,A new candidate application has been assigned to you. Please access your dashboard to view the details.\n\nCandidate Name: {candidate.name}\n\nClient: {candidate.client}\n\nRole: {candidate.profile}\n\nAssigned by Manager: {user_name}\n\nFeel free to reach out if you have any questions during the recruitment process.\n\nRegards,\n\nTeam\nMakonis Talent Track Pro\nrecruiterpro@makonissoft.com')

                    db.session.commit()

                    # Create notifications for the assigned recruiter
                    notifications = []
                    for candidate in candidates:
                        notification = Career_notification(
                            recruiter_name=assigned_recruiter.name,
                            notification_status=False  # You may set this to True for unread notifications
                        )
                        notifications.append(notification)

                    db.session.add_all(notifications)
                    db.session.commit()

                    return redirect(
                        url_for('website_candidate_assign', assignment_message='Candidates Assigned Successfully'))

        candidates = Candidate.query.filter(
            Candidate.recruiter.is_(None),
            Candidate.management.is_(None)
        ).all()

        candidate_count = Candidate.query.filter(
            Candidate.recruiter.is_(None),
            Candidate.management.is_(None)
        ).count()

        return render_template(
            'website_candidate_assign.html',
            recruiters=recruiters,
            candidates=candidates,
            assignment_message=assignment_message,
            user_name=user_name,
            candidate_count=candidate_count
        )

    return redirect(url_for('index'))

#new
def send_career_email(to, subject, message):
    msg = Message(subject, sender='saiganeshkanuparthi@gmail.com', recipients=[to])
    msg.body = message
    mail.send(msg)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=5000)

