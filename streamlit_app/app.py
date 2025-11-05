import streamlit as st
import requests

# Backend URL (make sure FastAPI is running)
API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="ConscienceAI - Ethics Auditor", layout="centered")

st.title("🧠 ConscienceAI — Meta-AI Ethics Auditor")
st.write("Analyze AI outputs for bias and generate ethical corrections.")

# Text input area
user_text = st.text_area("Paste AI model output here:", height=150)

if st.button("🔍 Analyze for Bias"):
    if not user_text.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing..."):
            try:
                resp = requests.post(API_URL, json={"text": user_text})
                if resp.status_code == 200:
                    data = resp.json()

                    st.subheader("📊 Bias Scores")
                    cols = st.columns(len(data["scores"]))
                    for i, (k, v) in enumerate(data["scores"].items()):
                        with cols[i]:
                            st.metric(label=k.capitalize(), value=f"{v}/5")

                    st.subheader("⚠️ Highlights")
                    for k, v in data["highlights"].items():
                        st.write(f"- **{k.capitalize()}**: {v}")

                    st.subheader("✅ Corrected Version")
                    st.info(data["corrected"])

                    st.subheader("📚 Sources Used (RAG)")
                    if data["sources"]:
                        for s in data["sources"]:
                            st.write(f"- **{s['title']}** — {s['content']}")
                    else:
                        st.write("No sources found.")
                else:
                    st.error(f"Error: {resp.status_code} — {resp.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")
