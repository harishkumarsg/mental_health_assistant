import streamlit as st
from chatbot_logic import analyze_input

st.set_page_config(page_title="Mental Health Assistant", page_icon="💬", layout="centered")

st.title("💬 Mental Health Assistant")
st.markdown("**Type in Tamil, Hindi, or English. It will auto-detect and help you accordingly.**")

# Input box
user_input = st.text_input("📝 Share what's on your mind")

if user_input:
    result = analyze_input(user_input)

    st.divider()
    st.subheader("🧠 Chat Analysis")
    st.write(f"**You:** {result['original']}")
    st.write(f"**Translated:** {result['translated']}")
    st.write(f"**Sentiment:** {result['sentiment'].capitalize()}")
    st.write(f"**Emotion:** {result['emotion'].capitalize()} ({result['confidence']}%)")
    
    st.markdown(f"**Suggestion:** _{result['suggestion']}_")
