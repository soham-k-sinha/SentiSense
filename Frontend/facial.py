# # Import necessary libraries
# import cv2
# import numpy as np
# from deepface import DeepFace
# import os
# from datetime import datetime
# import json
# from collections import deque
# import time
# import threading
# import tkinter as tk
# from PIL import Image, ImageTk

# # Define class to handle emotion detection tasks
# class EmotionDetector:
#     def __init__(self):
#         self.emotion_history = deque(maxlen=100)
#         self.emotion_timestamps = deque(maxlen=100)

#     def detect_emotion(self, frame):
#         try:
#             # Use DeepFace to analyze emotions
#             result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)[0]
#             emotion_label = result.get('dominant_emotion', None)
#             return emotion_label, result['emotion'].get(emotion_label, 0)
#         except Exception as e:
#             print(f"Error in detecting emotion: {e}")
#             return None, 0

#     def get_emotion_stats(self):
#         if not self.emotion_history:
#             return {}
        
#         emotion_counts = {}
#         for emotion in self.emotion_history:
#             emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
#         total = len(self.emotion_history)
#         return {emotion: count / total * 100 for emotion, count in emotion_counts.items()}

#     def reset_emotion_history(self):
#         self.emotion_history.clear()
#         self.emotion_timestamps.clear()

# # Real-time facial emotion detection with GUI control
# class EmotionDetectionApp:
#     def __init__(self):
#         self.cap = cv2.VideoCapture(0)
#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#         self.detector = EmotionDetector()
#         self.detection_active = False
#         self.root = tk.Tk()
#         self.setup_ui()

#     def setup_ui(self):
#         self.root.title("Emotion Detection Control Panel")

#         self.start_button = tk.Button(self.root, text="Start Detection", command=self.start_detection)
#         self.start_button.pack(pady=10)

#         self.stop_button = tk.Button(self.root, text="Stop Detection", command=self.stop_detection)
#         self.stop_button.pack(pady=10)

#         self.camera_frame = tk.Label(self.root)
#         self.camera_frame.pack()

#         self.emotion_stats_label = tk.Label(self.root, text="Emotion Statistics will be displayed here.")
#         self.emotion_stats_label.pack(pady=10)

#         self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
#         self.update_frame()
#         self.root.mainloop()

#     def start_detection(self):
#         if not self.detection_active:
#             self.detector.reset_emotion_history()  # Reset history when starting a new detection session
#             self.detection_active = True
#             threading.Thread(target=self.run_detection, daemon=True).start()

#     def stop_detection(self):
#         if self.detection_active:
#             self.detection_active = False
#             stats = self.detector.get_emotion_stats()
#             if stats:
#                 stats_text = "Emotion statistics:\n" + "\n".join([f"{emotion}: {percentage:.2f}%" for emotion, percentage in stats.items()])
#                 self.emotion_stats_label.config(text=stats_text)

#     def run_detection(self):
#         while self.detection_active:
#             # Capture frame from webcam
#             ret, frame = self.cap.read()
#             if not ret:
#                 print("Error: Could not read frame.")
#                 break

#             # Flip frame horizontally for natural mirror effect
#             frame = cv2.flip(frame, 1)
            
#             # Detect emotion from the entire frame
#             emotion, confidence = self.detector.detect_emotion(frame)
#             if emotion:
#                 self.detector.emotion_history.append(emotion)
#                 self.detector.emotion_timestamps.append(datetime.now())

#     def update_frame(self):
#         ret, frame = self.cap.read()
#         if ret:
#             frame = cv2.flip(frame, 1)
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             img = Image.fromarray(frame)
#             imgtk = ImageTk.PhotoImage(image=img)
#             self.camera_frame.imgtk = imgtk
#             self.camera_frame.configure(image=imgtk)
#         self.root.after(10, self.update_frame)

#     def on_closing(self):
#         self.detection_active = False
#         self.cap.release()
#         cv2.destroyAllWindows()
#         self.root.destroy()

# if __name__ == "__main__":
#     EmotionDetectionApp()

import cv2
import numpy as np
from deepface import DeepFace
from datetime import datetime
from collections import deque
import os
from flask import Flask, request, jsonify

# Define class to handle emotion detection tasks
class EmotionDetector:
    def __init__(self):
        self.emotion_history = deque(maxlen=100)
        self.emotion_timestamps = deque(maxlen=100)

    def detect_emotion(self, frame):
        try:
            # Use DeepFace to analyze emotions
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)[0]
            emotion_label = result.get('dominant_emotion', None)
            return emotion_label, result['emotion'].get(emotion_label, 0)
        except Exception as e:
            print(f"Error in detecting emotion: {e}")
            return None, 0

    def get_emotion_stats(self):
        if not self.emotion_history:
            return {}
        
        emotion_counts = {}
        for emotion in self.emotion_history:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        total = len(self.emotion_history)
        return {emotion: count / total * 100 for emotion, count in emotion_counts.items()}

    def reset_emotion_history(self):
        self.emotion_history.clear()
        self.emotion_timestamps.clear()

# Flask app to handle video file upload and emotion analysis
app = Flask(__name__)

# Function to process uploaded video for emotion analysis
def process_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Initialize the emotion detector
    detector = EmotionDetector()

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        # Detect emotion from the current frame
        emotion, confidence = detector.detect_emotion(frame)
        if emotion:
            detector.emotion_history.append(emotion)
            detector.emotion_timestamps.append(datetime.now())
        
        frame_count += 1
        print(f"Processed frame {frame_count} | Detected Emotion: {emotion} with Confidence: {confidence}")

    # Close the video capture object
    cap.release()

    # Get and display the emotion statistics
    stats = detector.get_emotion_stats()
    return stats

# Endpoint to receive the video from the frontend and process it
@app.route('/emotion_analysis', methods=['POST'])
def emotion_analysis():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    video_path = os.path.join('uploads', video_file.filename)
    
    # Save the video file to disk
    video_file.save(video_path)
    
    # Process the video to detect emotions
    emotion_stats = process_video(video_path)

    # Return the emotion statistics as a JSON response
    return jsonify(emotion_stats)

if __name__ == '__main__':
    # Make sure the upload folder exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    app.run(debug=True)
