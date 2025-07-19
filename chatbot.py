from textblob import TextBlob
from googletrans import Translator
from transformers import pipeline

translator = Translator()
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)
sentiment_classifier = pipeline("sentiment-analysis")

def detect_language(text):
    try:
        return translator.detect(text).lang
    except:
        return "en"

def translate_to_english(text):
    lang = detect_language(text)
    if lang != 'en':
        translated = translator.translate(text, dest='en')
        return translated.text, lang
    return text, 'en'

def analyze_text(text):
    sentiment = sentiment_classifier(text)[0]
    emotion = emotion_classifier(text)[0][0]
    return sentiment['label'], emotion['label'], emotion['score']

def get_suggestion(emotion):
    suggestions = {
        "joy": "It's great to hear you're feeling joyful! Keep doing what makes you happy.",
        "sadness": "It's okay to feel sad. Talking to someone can help.",
        "anger": "Try deep breathing or a short walk to calm down.",
        "fear": "You're not alone. Try grounding techniques to feel safe.",
        "love": "Spread the love and stay connected.",
        "surprise": "Interesting! Can you share more about it?",
        "neutral": "Thanks for sharing. Keep observing your feelings."
    }
    return suggestions.get(emotion.lower(), "I'm here to listen. Keep talking.")
