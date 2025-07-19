import streamlit as st
from chatbot_logic import analyze_input

# Streamlit page configuration
st.set_page_config(page_title="Mental Health Assistant", page_icon="💬", layout="centered")

# Custom CSS styling
st.markdown("""
    <style>
        .main {
            background-color: #f7f9fc;
        }
        .stTextInput>div>div>input {
            background-color: #ffffff;
            border: 1px solid #d3d3d3;
            border-radius: 8px;
            padding: 10px;
        }
        .stMarkdown h1, h2, h3, h4 {
            color: #2c3e50;
        }
        .emotion-bar {
            background-color: #ddd;
            border-radius: 20px;
            overflow: hidden;
            height: 20px;
            margin-bottom: 10px;
        }
        .emotion-fill {
            background-color: #4caf50;
            height: 100%;
            text-align: center;
            color: white;
            font-size: 14px;
            font-weight: bold;
            line-height: 20px;
        }
        .suggestion-box {
            background-color: #e3f2fd;
            padding: 16px;
            border-radius: 10px;
            font-style: italic;
            font-size: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("💬 Mental Health Assistant")
st.markdown("##### Type in **Tamil**, **Hindi**, or **English**. It will auto-detect and support you accordingly.")
st.markdown("Share your thoughts and receive real-time emotional support powered by multilingual NLP. 🌍")

# Input box
user_input = st.text_input("📝 What's on your mind today?", placeholder="e.g., I'm feeling overwhelmed with exams...")

if user_input:
    result = analyze_input(user_input)

    # Output section
    st.markdown("---")
    st.markdown("### 🧠 Chat Analysis")

    st.markdown(f"**🔸 Original Input:** {result['original']}")
    st.markdown(f"**🔄 Translated Text:** {result['translated']}")
    st.markdown(f"**📊 Sentiment:** `{result['sentiment'].upper()}` ({result['sentiment_score']}%)")
    st.markdown(f"**💬 Detected Emotion:** `{result['emotion'].upper()}` ({result['confidence']}%)")

    # Emotion Confidence Progress Bar
    st.markdown("### 📈 Emotion Confidence Level")
    confidence = float(result['confidence'])
    st.markdown(f"""
        <div class='emotion-bar'>
            <div class='emotion-fill' style='width: {confidence}%'>{confidence:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)

    # Coping Tip
    st.markdown("### 🧘‍♀️ Personalized Coping Tip")
    st.markdown(f"<div class='suggestion-box'>{result['suggestion']}</div>", unsafe_allow_html=True)

    # Optional extra tip
    if result.get("extra_tip"):
        st.markdown("### 💡 Extra Tip")
        st.markdown(f"- {result['extra_tip']}")

    # Optional guided meditation
    if result.get("meditation_link"):
        st.markdown("### 🎧 Try This")
        st.markdown(f"[{result['meditation_title']}]({result['meditation_link']})")

    st.markdown("---")
    st.caption("⚠️ This assistant is a prototype research tool. Please consult mental health professionals for serious concerns.")
