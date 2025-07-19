import streamlit as st
from chatbot_logic import analyze_input

# Streamlit page configuration
st.set_page_config(page_title="Mental Health Assistant", page_icon="💬", layout="centered")

# Custom CSS for better UI
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
        .stMarkdown h1 {
            text-align: center;
            color: #2c3e50;
        }
        .stMarkdown p {
            font-size: 16px;
        }
        .suggestion-box {
            background-color: #e3f2fd;
            padding: 12px;
            border-radius: 8px;
            font-style: italic;
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

    # Analysis output
    st.markdown("---")
    st.subheader("🧠 Chat Analysis")
    
    st.markdown(f"**🔸 Original Input:** {result['original']}")
    st.markdown(f"**🔄 Translated Text:** {result['translated']}")
    st.markdown(f"**📊 Sentiment:** `{result['sentiment'].capitalize()}`")
    st.markdown(f"**💬 Detected Emotion:** `{result['emotion'].capitalize()}` ({result['confidence']}%)")

    # Suggestion box
    st.markdown("---")
    st.markdown("#### 🧘‍♀️ Suggested Coping Tip")
    st.markdown(f"<div class='suggestion-box'>{result['suggestion']}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("This assistant is a prototype research tool. Please consult professionals for serious mental health concerns.")
