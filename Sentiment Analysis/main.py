from textblob import TextBlob
from transformers import BartTokenizer, BartForConditionalGeneration
import openai

# Open Text File
with open('Sentiment Analysis/transcript.txt', encoding='utf8') as file_object:
    # Text from File
    journal = file_object.read()

# Word Count
word_count = len(journal.split())


# Analyze the sentiment
blob = TextBlob(journal)

# Final Sentiment score between -1 (Negative) and 1 (Positive)
sentiment_score = blob.sentiment.polarity

# Mood between 0 and 100
mood = round(50 * (sentiment_score + 1))


# Generate Summary
def generate_summary(text):
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=160, min_length=75, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# summary = generate_summary(journal)

# NEED TO ADD ADVICE GENERATION