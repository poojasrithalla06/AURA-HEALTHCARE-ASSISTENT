from flask import Blueprint, jsonify, request, render_template, make_response
from models.database import db, Medication, Feedback, SOSAlert, HealthTrend, User
from utils.ai_engine import predict_risk, chat_response
from datetime import datetime
import json
import pdfkit # In practice, user needs wkhtmltopdf installed or another library. We'll use a simple HTML print method via JS, but API is here.

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/predict_risk', methods=['POST'])
def get_risk():
    data = request.json
    # Expected: age, glucose, systolic_bp, diastolic_bp, heart_rate, sp02, temperature
    risk_score, explanation = predict_risk(data)
    
    # Save trend if user_id is provided
    if 'user_id' in data:
        trend = HealthTrend(
            user_id=data['user_id'],
            risk_score=risk_score,
            heart_rate=data.get('heart_rate'),
            sp02=data.get('sp02'),
            temperature=data.get('temperature')
        )
        db.session.add(trend)
        db.session.commit()
    
    return jsonify({
        'risk_score': risk_score,
        'category': 'Critical' if risk_score > 80 else 'High' if risk_score > 60 else 'Moderate' if risk_score > 30 else 'Low',
        'explanation': explanation
    })

@api_bp.route('/chatbot', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    language = data.get('language', 'en')
    user_id = data.get('user_id')
    
    response_text = chat_response(message, language, user_id)
    return jsonify({'response': response_text})

@api_bp.route('/sos', methods=['POST'])
def trigger_sos():
    data = request.json
    user_id = data.get('user_id')
    location = data.get('location', 'Unknown Location')
    
    alert = SOSAlert(user_id=user_id, location=location)
    db.session.add(alert)
    db.session.commit()
    
    return jsonify({'status': 'alert_sent', 'message': 'Emergency contacts notified successfully!'})

@api_bp.route('/medication', methods=['POST', 'GET'])
def handle_medication():
    if request.method == 'POST':
        data = request.json
        med = Medication(
            user_id=data['user_id'],
            name=data['name'],
            time=data['time'],
            frequency=data['frequency']
        )
        db.session.add(med)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        user_id = request.args.get('user_id')
        meds = Medication.query.filter_by(user_id=user_id).all()
        return jsonify([{'id': m.id, 'name': m.name, 'time': m.time} for m in meds])

@api_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    fb = Feedback(
        user_id=data.get('user_id'),
        content=data.get('comment'),
        helpful=data.get('helpful')
    )
    db.session.add(fb)
    db.session.commit()
    return jsonify({'status': 'feedback_received'})
