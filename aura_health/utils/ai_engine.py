import random

def predict_risk(data):
    # Mock AI Algorithm
    # In real world: Load pickled scikit-learn model here
    
    age = data.get('age', 30)
    systolic_bp = data.get('systolic_bp', 120)
    diastolic_bp = data.get('diastolic_bp', 80)
    heart_rate = data.get('heart_rate', 70)
    glucose = data.get('glucose_level', 90)
    
    risk_score = 0
    
    # Simple Heuristic Rule-based "Model"
    if systolic_bp > 140 or diastolic_bp > 90:
        risk_score += 30
    elif systolic_bp > 120:
        risk_score += 15
        
    if heart_rate > 100 or heart_rate < 50:
        risk_score += 20
        
    if glucose > 140:
        risk_score += 25
    elif glucose < 70:
        risk_score += 15
        
    if age > 50:
        risk_score += 10
        
    risk_score = min(risk_score, 100) # Cap at 100
    
    explanation = []
    if risk_score > 60:
        explanation.append("Multiple risk factors detected: high BP/Glucose.")
    elif risk_score > 30:
        explanation.append("Moderate risk. Lifestyle changes recommended.")
    else:
        explanation.append("Healthy vitals. Maintain current routine.")
        
    return risk_score, " ".join(explanation)

def chat_response(message, language, user_id):
    # Mock NLP Chatbot
    msg = message.lower()
    
    responses = {
        'en': {
            'hello': "Hello! I am Aura, your health assistant. How can I help you today?",
            'headache': "For a headache, try resting in a dark room and staying hydrated. If it persists, consult a doctor.",
            'fever': "Monitor your temperature. If it exceeds 102°F (39°C), seek medical attention immediately.",
            'appointment': "You can book an appointment from your dashboard. Would you like me to redirect you?",
            'default': "I'm not sure specifically, but I can help you track symptoms or book a doctor."
        },
        'hi': { # Hindi
            'hello': "Namaste! Main Aura hun, aapki swasthya sahayak.",
            'default': "Maaf kijiye, main abhi seekh rahi hun."
        }
        # Add other languages as needed
    }
    
    lang_responses = responses.get(language, responses['en'])
    
    if 'hello' in msg or 'hi' in msg:
        return lang_responses.get('hello')
    elif 'headache' in msg or 'pain' in msg:
        return lang_responses.get('headache', responses['en']['headache'])
    elif 'fever' in msg:
        return lang_responses.get('fever', responses['en']['fever'])
    else:
        return lang_responses.get('default')
