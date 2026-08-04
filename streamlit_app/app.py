import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze"

# --- Page Configuration ---
st.set_page_config(
    page_title="🧠 ConscienceAI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS for Styling ---
st.markdown("""
<style>
/* Navigation Bar */
.navbar {
    background-color: #4B0082;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
.navbar a {
    color: white;
    font-weight: bold;
    margin: 0 20px;
    text-decoration: none;
    font-size: 18px;
}
.navbar a:hover {
    color: #FFDD57;
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px;
    background-color: #4B0082;
    color: white;
    border-radius: 10px;
    margin-top: 50px;
}

/* Feature Cards */
.card {
    background: #F0F8FF;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

/* Buttons */
.button {
    background-color:#6A5ACD;
    color:white;
    border:none;
    padding:10px 20px;
    border-radius:8px;
    cursor:pointer;
}
.button:hover {
    background-color:#4B0082;
}
</style>
""", unsafe_allow_html=True)

# --- Navigation Bar ---
st.markdown("""
<div class="navbar">
    <a href="#home">Home</a>
    <a href="#analyze">Analyze</a>
    <a href="#about">About</a>
    <a href="#contact">Contact</a>
</div>
""", unsafe_allow_html=True)

# --- Landing Page / Hero Section ---
st.markdown("<a id='home'></a>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding:80px; background: linear-gradient(135deg,#6A5ACD,#4B0082); border-radius:15px; color:white;">
    <h1 style='font-size:60px; font-weight:bold;'>🧠 ConscienceAI</h1>
    <h3>Audit AI outputs for bias and get ethical guidance instantly</h3>
    <p style='font-size:18px;'>Detect gender, racial, and social biases in AI-generated content. Make your AI applications trustworthy.</p>
    <a href="#analyze" class="button">Start Analysis 🔍</a>
</div>
""", unsafe_allow_html=True)
st.divider()

# --- Analyze Section ---
st.markdown("<a id='analyze'></a>", unsafe_allow_html=True)
st.subheader("🔍 Analyze AI-generated Text")
user_text = st.text_area(
    "Paste your AI-generated output here...",
    placeholder="Example: Men are better at engineering than women...",
    height=200
)

col1, col2 = st.columns([1, 2])
with col1:
    analyze_btn = st.button("Analyze for Bias", use_container_width=True)
with col2:
    st.caption("Send text to backend for ethical evaluation. Fast and insightful!")

if analyze_btn:
    if not user_text.strip():
        st.warning("⚠️ Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing text for bias..."):
            try:
                resp = requests.post(API_URL, json={"text": user_text}, timeout=8)
                if resp.status_code == 200:
                    data = resp.json()
                    tabs = st.tabs(["📊 Bias Scores", "⚠️ Highlights", "✅ Corrected Output", "📚 Sources"])

                    # --- Bias Scores Tab ---
                    with tabs[0]:
                        st.subheader("Bias Severity by Category")
                        scores = data.get("scores", {})
                        for cat, score in sorted(scores.items()):
                            if cat == "overall": continue
                            color = "#FF3B3B" if score >= 4 else "#FFB400" if score >= 2 else "#28A745"
                            st.markdown(f"""
                                <div style="display:flex; align-items:center; margin-bottom:10px;">
                                    <strong style='width:150px'>{cat.capitalize()}</strong>
                                    <div style='flex:1; background-color:#EDEDED; border-radius:10px; margin-right:10px;'>
                                        <div style='width:{(score/5)*100}%; background-color:{color}; height:22px; border-radius:10px;'></div>
                                    </div>
                                    <span style='color:{color}; font-weight:bold;'>{score}/5</span>
                                </div>
                            """, unsafe_allow_html=True)

                    # --- Highlights Tab ---
                    with tabs[1]:
                        st.subheader("Detected Biased Phrases & Explanation")
                        highlights = data.get("highlights", {})
                        if highlights:
                            for cat, items in highlights.items():
                                with st.expander(f"{cat.capitalize()} — explanation & matches"):
                                    if items:
                                        st.markdown(f"**Explanation:** {items[0]}")
                                        if len(items) > 1:
                                            st.markdown("**Matched phrases:**")
                                            for phrase in items[1:]:
                                                st.markdown(f"<span style='background-color:#FFDD57; color:#000; padding:4px 8px; border-radius:5px;'>{phrase}</span>", unsafe_allow_html=True)
                                    else:
                                        st.write("No specific matches found.")
                        else:
                            st.info("No biased phrases detected 🎉")

                    # --- Corrected Output Tab ---
                    with tabs[2]:
                        st.subheader("Ethically Corrected Version")
                        st.success(data.get("corrected", "No corrected output returned."))

                    # --- Sources Tab ---
                    with tabs[3]:
                        st.subheader("Sources & Guidance")
                        for i, s in enumerate(data.get("sources", []), 1):
                            with st.expander(f"📖 Source {i}: {s.get('title','')}"):
                                st.write(s.get("content", ""))

                else:
                    st.error(f"API Error: {resp.status_code}")
                    st.text(resp.text)

            except requests.exceptions.ConnectionError:
                st.error("🚫 Unable to connect to backend. Make sure FastAPI is running.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# --- About Section ---
st.markdown("<a id='about'></a>", unsafe_allow_html=True)
st.subheader("📌 About ConscienceAI")

st.markdown("""
<div class="card">
<h4>✅ Detect Biases</h4>
<p>Identify gender, racial, and social biases in AI-generated content.</p>
</div>
<div class="card">
<h4>📝 Explain Clearly</h4>
<p>Highlights biased phrases and provides understandable insights.</p>
</div>
<div class="card">
<h4>💡 Suggest Corrections</h4>
<p>Offers ethically improved alternatives for problematic content.</p>
</div>
<div class="card">
<h4>🛠 Guide Developers</h4>
<p>Helps maintain fairness and accountability in AI systems.</p>
</div>
""", unsafe_allow_html=True)

# --- Contact Section ---
st.markdown("<a id='contact'></a>", unsafe_allow_html=True)
st.subheader("📬 Contact Us")
st.markdown("""
- Email: contact@conscienceai.com  
- Phone: +91 9876543210  
- Website: [www.conscienceai.com](http://www.conscienceai.com)  
- Twitter: [@ConscienceAI](https://twitter.com)
""")

