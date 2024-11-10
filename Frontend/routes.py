from flask import Blueprint, render_template, request, jsonify
import time

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('hello.html')

@main_bp.route('/submit_journal', methods=['POST'])
def submit_journal():
    # Simulate processing time
    time.sleep(1)
    
    # In a real application, you would process the video here
    # and use AI to analyze the journal entry
    
    return jsonify({
        'success': True,
        'message': 'Your journal entry has been submitted.',
        'current_mood': '😊',
        'ai_advice': "Based on your journal entry, it seems you're doing well. Keep up the positive attitude and remember to take breaks when needed."
    })