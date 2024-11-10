from textblob import TextBlob
import re

class JournalAdvisor:
    def __init__(self):
        # Define emotional patterns and corresponding advice
        self.emotion_patterns = {
            'stressed': {
                'keywords': ['stress', 'overwhelm', 'pressure', 'anxiety', 'worried'],
                'advice': [
                    "Take 5 deep breaths using the 4-7-8 technique",
                    "Go for a 10-minute walk outside",
                    "Write down what's causing your stress and prioritize tasks",
                    "Try a quick meditation session"
                ]
            },
            'tired': {
                'keywords': ['tired', 'exhausted', 'fatigue', 'sleepy', 'drained'],
                'advice': [
                    "Take a 20-minute power nap if possible",
                    "Get some fresh air and sunlight",
                    "Have a healthy snack and drink water",
                    "Do some light stretching exercises"
                ]
            },
            'sad': {
                'keywords': ['sad', 'lonely', 'depressed', 'down', 'upset', 'unhappy'],
                'advice': [
                    "Reach out to a friend or family member",
                    "Listen to your favorite uplifting music",
                    "Write down three things you're grateful for",
                    "Plan something enjoyable for later today"
                ]
            },
            'angry': {
                'keywords': ['angry', 'frustrated', 'annoyed', 'mad', 'irritated'],
                'advice': [
                    "Take a timeout to cool down",
                    "Practice progressive muscle relaxation",
                    "Write down what's bothering you",
                    "Channel the energy into exercise"
                ]
            }
        }

    def analyze_text(self, text):
        """Analyze the journal text and return sentiment and detected emotions."""
        # Get sentiment using TextBlob
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        
        # Detect emotions based on keywords
        detected_emotions = []
        lower_text = text.lower()
        
        for emotion, data in self.emotion_patterns.items():
            if any(keyword in lower_text for keyword in data['keywords']):
                detected_emotions.append(emotion)
        
        return sentiment_score, detected_emotions

    def get_sentiment_advice(self, sentiment_score):
        """Generate general advice based on sentiment score."""
        if sentiment_score < -0.3:
            return "I notice you're feeling quite down today. Remember that it's okay to not be okay, and tomorrow is a new day."
        elif sentiment_score < 0:
            return "You seem to be feeling a bit low. Let's focus on some simple ways to lift your spirits."
        elif sentiment_score < 0.3:
            return "You're maintaining a balanced mood. Let's build on that with some positive activities."
        else:
            return "You're in a good mood! Let's keep that positive energy going."

    def generate_advice(self, text):
        """Main function to analyze journal and generate personalized advice."""
        if not text.strip():
            return "Please provide a journal entry to analyze."

        # Analyze the text
        sentiment_score, detected_emotions = self.analyze_text(text)
        
        # Prepare advice
        advice = []
        
        # Add sentiment-based general advice
        advice.append(("Overall Mood", self.get_sentiment_advice(sentiment_score)))
        
        # Add specific advice based on detected emotions
        import random
        for emotion in detected_emotions:
            specific_advice = random.choice(self.emotion_patterns[emotion]['advice'])
            advice.append((f"Because you seem {emotion}", specific_advice))
        
        # If no specific emotions detected, add general positive advice
        if not detected_emotions:
            general_advice = [
                "Take a moment to practice mindfulness",
                "Do something kind for yourself today",
                "Set one small achievable goal for today",
                "Connect with someone you care about"
            ]
            advice.append(("General Suggestion", random.choice(general_advice)))

        return advice

    def format_advice(self, advice_list):
        """Format the advice into a readable string."""
        output = "💭 Journal Analysis & Suggestions 💭\n\n"
        for category, suggestion in advice_list:
            output += f"📌 {category}:\n   {suggestion}\n\n"
        return output

def run():
    # Example usage
    advisor = JournalAdvisor()

    # Get journal entry from user
    with open('transcript.txt', encoding='utf8') as file_object:
    # Text from File
        journal = file_object.read()

    # Generate and print advice
    advice_list = advisor.generate_advice(journal)
    return advice_list