import sys
import os
from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename

import transcriber
import senti
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
    
    # Save the video file
    video.save(file_path)
    
    try:
        # Transcribe the video file
        transcriber.run(file_path)  # Pass the file_path to transcriber.run()

        # Run sentiment analysis on the transcribed data or video file
        sentiment_result = senti.run()  # Assuming senti.run() processes the file
        
        # Simulate AI-based analysis results (this part may depend on your sentiment model output)
        current_mood = sentiment_result[0][1] if sentiment_result else "Neutral"
        ai_advice = f"Based on your journal entry, it seems you are feeling {current_mood}. {sentiment_result[1][0]}: {sentiment_result[1][1]}" if sentiment_result else "No advice available at this time."
        
        # Simulate processing delay
        time.sleep(1)
        
        return jsonify({
            'success': True,
            'message': 'Your journal entry has been submitted.',
            'current_mood': current_mood,
            'ai_advice': ai_advice
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500