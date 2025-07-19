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
        "joy": {
            "tip": "It's great to hear you're feeling joyful! Keep doing what makes you happy.",
        },
        "sadness": {
            "tip": "I'm sorry you're feeling sad. Try journaling, a short walk, or speaking to a close friend.",
        },
        "anger": {
            "tip": "Anger is natural. Try a short walk or deep breathing to cool off.",
        },
        "fear": {
            "tip": "Exams can be stressful. You're not alone. Try the 4-7-8 breathing technique:\n- Inhale 4 sec\n- Hold 7 sec\n- Exhale 8 sec",
            "note": "💡 Tip: Break your study into small chunks and take short breaks. You’ll feel more in control.",
            "link": "🎧 Try this 5-minute guided meditation for exam stress"
        },
        "love": {
            "tip": "That’s beautiful! Connect with people who matter to you.",
        },
        "surprise": {
            "tip": "Surprises can be good or confusing. Take time to reflect and understand your emotions.",
        }
    }
    return suggestions.get(emotion, {"tip": "I'm here for you. Remember to take care of yourself."})

def analyze_input(user_input):
    lang = detect(user_input)
    translated = GoogleTranslator(source='auto', target='en').translate(user_input) if lang != 'en' else user_input
    sentiment_result = sentiment_pipe(translated)[0]
    sentiment_label = sentiment_result['label'].upper()
    sentiment_score = round(sentiment_result['score'] * 100, 2)

    emotion, confidence = detect_emotion(translated)
    suggestion_block = generate_suggestion(emotion)
    
    bar_blocks = int(confidence * 20)  # 20 bars max
    confidence_bar = '█' * bar_blocks + ' ' * (20 - bar_blocks)

    response = f"""🧠 Chat Analysis  
🔸 Original Input: {user_input}  
🔄 Translated Text: {translated}  
📊 Sentiment: {sentiment_label} ({sentiment_score}%)  
💬 Detected Emotion: {emotion.upper()} ({round(confidence * 100, 2)}%)

📈 Emotion Confidence Level  
{confidence_bar} {round(confidence * 100, 2)}%

🧘‍♀️ Personalized Coping Tip  
{suggestion_block.get("tip")}

{suggestion_block.get("note", "")}
{suggestion_block.get("link", "")}
"""
    return response
