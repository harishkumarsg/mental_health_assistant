import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from langdetect import detect
from deep_translator import GoogleTranslator

@torch.no_grad()
def load_pipelines():
    sentiment_pipe = pipeline("sentiment-analysis")
    emotion_model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
    tokenizer = AutoTokenizer.from_pretrained(emotion_model_name)
    model = AutoModelForSequenceClassification.from_pretrained(emotion_model_name)
    model.eval()
    return sentiment_pipe, tokenizer, model

sentiment_pipe, emotion_tokenizer, emotion_model = load_pipelines()

def detect_emotion(text):
    inputs = emotion_tokenizer(text, return_tensors="pt")
    outputs = emotion_model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    top_idx = torch.argmax(probs, dim=1).item()
    label = emotion_model.config.id2label[top_idx]
    confidence = probs[0][top_idx].item()
    return label, confidence

def generate_suggestion(emotion):
    suggestions = {
        "joy": "It's great to hear you're feeling joyful! Keep doing what makes you happy.",
        "sadness": "I'm sorry you're feeling sad. Talking to someone you trust or engaging in a relaxing activity can help.",
        "anger": "It's okay to feel angry. Deep breathing and a short walk may help calm your mind.",
        "fear": "Fear is natural. Try grounding yourself with calming techniques like deep breathing.",
        "love": "That's beautiful! Spread the love and connect with others.",
        "surprise": "Surprises can be exciting or shocking. Take a moment to process what you're feeling."
    }
    return suggestions.get(emotion, "I'm here for you. Remember to take care of yourself.")

def analyze_input(user_input):
    lang = detect(user_input)
    translated = GoogleTranslator(source='auto', target='en').translate(user_input) if lang != 'en' else user_input
    sentiment = sentiment_pipe(translated)[0]
    emotion, confidence = detect_emotion(translated)
    suggestion = generate_suggestion(emotion)
    return {
        "original": user_input,
        "translated": translated,
        "sentiment": sentiment['label'],
        "emotion": emotion,
        "confidence": round(confidence * 100, 2),
        "suggestion": suggestion
    }
