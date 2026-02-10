from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models.database import db, User, HealthTrend, Appointment

main_bp = Blueprint('main', __name__)

@main_bp.before_request
def require_login():
    if 'user_id' not in session and request.endpoint not in ['auth.login', 'auth.signup', 'main.index', 'static']:
        return redirect(url_for('auth.login'))

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    user = User.query.get(session['user_id'])
    trends = HealthTrend.query.filter_by(user_id=user.id).all()
    appointments = Appointment.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, trends=trends, appointments=appointments)

@main_bp.route('/doctor_dashboard')
def doctor_dashboard():
    user = User.query.get(session['user_id'])
    # In a real app check for user.role == 'doctor'
    appointments = Appointment.query.filter_by(doctor_id=user.id).all()
    return render_template('doctor_dashboard.html', user=user, appointments=appointments)

@main_bp.route('/admin_panel')
def admin_panel():
    user = User.query.get(session['user_id'])
    # In a real app check for user.role == 'admin'
    users = User.query.all()
    return render_template('admin_panel.html', users=users)

@main_bp.route('/create_appointment', methods=['GET', 'POST'])
def create_appointment():
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        reason = request.form['reason']
        date = request.form['date']
        
        appt = Appointment(user_id=session['user_id'], doctor_id=doctor_id, reason=reason, date=date)
        db.session.add(appt)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('appointment.html')
    
@main_bp.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@main_bp.route('/report')
def report():
    user = User.query.get(session['user_id'])
    trends = HealthTrend.query.filter_by(user_id=user.id).all()
    return render_template('report.html', user=user, trends=trends)

@main_bp.route('/medication')
def medication():
    return render_template('medication_reminder.html')

@main_bp.route('/emergency_sos', methods=['POST'])
def emergency_sos():
    # Trigger SOS logic here (e.g., notify emergency contacts)
    flash('Emergency Alert Sent!', 'danger')
    return redirect(url_for('main.dashboard'))
