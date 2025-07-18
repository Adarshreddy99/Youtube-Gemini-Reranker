import streamlit as st
import speech_recognition as sr
from main import process_query

# Page setup
st.set_page_config(page_title="🎙️ YouTube Gemini Ranker", layout="centered")
st.markdown("<h1 style='text-align: center;'>🔍 YouTube Search + Gemini Ranking</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Search YouTube using <b>text or voice</b> in <b>Hindi or English</b></p>", unsafe_allow_html=True)
st.markdown("---")

# --- Input Controls ---
query = ""

# Input Method
st.subheader("🎛️ Input Method")
input_mode = st.radio(
    label="",
    options=["📝 Text", "🎤 Voice"],
    horizontal=True,
    help="Choose whether to type or speak your query."
)

# Language Choice
st.subheader("🌐 Language")
lang_mode = st.radio(
    label="",
    options=["🇬🇧 English", "🇮🇳 Hindi"],
    horizontal=True,
    help="Select the language of your query."
)
lang_code = "en-IN" if lang_mode == "🇬🇧 English" else "hi-IN"

# Query Input
st.subheader("💬 Your Search Query")

if input_mode == "📝 Text":
    placeholder = "Enter your query in English..." if lang_code == "en-IN" else "अपना प्रश्न हिंदी में लिखें..."
    query = st.text_input("", placeholder=placeholder, max_chars=100)

else:
    st.markdown("Click below and speak clearly into the microphone:")
    if st.button("🎤 Start Voice Recording"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            with st.spinner("🎧 Listening... (You have 15 seconds)"):
                try:
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
                    query = recognizer.recognize_google(audio, language=lang_code)
                    st.success(f"✅ You said: **{query}**")
                except sr.WaitTimeoutError:
                    st.error("⌛ You didn’t start speaking in time.")
                except sr.UnknownValueError:
                    st.error("😕 Could not understand your voice.")
                except sr.RequestError:
                    st.error("🚫 Could not connect to Speech API.")

# --- Search and Display ---
st.markdown("---")
if query:
    if st.button("🔍 Search YouTube and Rank with Gemini"):
        with st.spinner("⏳ Processing query and ranking videos..."):
            try:
                best_video, all_videos = process_query(query)

                if not best_video:
                    st.warning("❌ No relevant videos found. Try another topic.")
                else:
                    # Top Recommendation
                    st.success("✅ Top result selected by Gemini!")
                    st.markdown("## 🏆 Gemini's Top Pick")

                    st.markdown(f"### 🎬 {best_video['title']}")
                    st.write(f"🔗 [Watch on YouTube]({best_video['url']})")

                    col1, col2, col3 = st.columns(3)
                    col1.metric("⏱ Duration", f"{best_video['duration_min']} min")
                    col2.metric("📅 Published", best_video['published_at'].split('T')[0])
                    col3.metric("👁️ Views", f"{int(best_video['views']):,}")

                    # Other Videos
                    st.markdown("---")
                    st.markdown("### 📋 Other Results From top 20")
                    count = 1
                    for vid in all_videos:
                        if vid["url"] == best_video["url"]:
                            continue  # Skip duplicate of best
                        st.markdown(f"{count}. [{vid['title']}]({vid['url']})")
                        count += 1

            except Exception as e:
                st.error(f"🚨 An error occurred while processing your query:\n`{e}`")
