from textblob import TextBlob
from transformers import BartTokenizer, BartForConditionalGeneration
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

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

# Sentiment model
sentiment_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
sentiment_analyzer = pipeline("sentiment-analysis", model=sentiment_model_name, device=0 if torch.cuda.is_available() else -1)

# GPT Model
model_name = "EleutherAI/gpt-neo-2.7B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Move model to correct device (GPU or CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # This line ensures that device is set to CPU or GPU correctly
model = model.to(device)

def generate_advice(text):
    # Perform sentiment analysis
    sentiment = sentiment_analyzer(text)
    print("Sentiment:", sentiment)

    # Prepare input for GPT model
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024).to(device)
    
    # Generate output
    output = model.generate(**inputs, max_length=300, pad_token_id=tokenizer.eos_token_id)  # Fix pad_token_id issue
    
    # Decode the output to get the response
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return response

# Sample input
prompt = f"This is a summary of my day: {journal}. As my therapist, give me advice to improve my day. What steps should I take to get into a better headspace?"
p = "Hi. How are you?"

# Generate advice
result = generate_advice(prompt)
print(result)