import sys
import os
from flask import Blueprint, render_template, request, jsonify
import time
from werkzeug.utils import secure_filename

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import senti

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

@main_bp.route('/sentiment_analysis', methods=['POST'])
def sentimental_analysis():
    # Check if the 'video' is part of the request
    if 'video' not in request.files:
        return jsonify({
            'success': False,
            'message': 'No video file uploaded.',
        })
    
    video = request.files['video']
    filename = secure_filename(video.filename)
    
    # Define the upload folder
    upload_folder = 'uploads'

    # Ensure the upload directory exists
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # Define the file path
    file_path = os.path.join(upload_folder, filename)
    
    # Save the video to disk
    video.save(file_path)

    # Run sentiment analysis or other processing on the video file
    senti.run()  # Assuming senti.run() processes the file in the specified location
    
    # Simulate AI-based analysis results
    time.sleep(1)  # Simulate some processing delay
    
    return jsonify({
        'success': True,
        'message': 'Your journal entry has been submitted and analyzed.',
        'current_mood': '😊',
        'ai_advice': "Based on your journal entry, it seems you're doing well. Keep up the positive attitude and remember to take breaks when needed."
    })
