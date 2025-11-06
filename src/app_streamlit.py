import streamlit as st
from nlu import detect_intent, detect_language
from retriever import Retriever
from composer import compose_response
from gtts import gTTS
from io import BytesIO
import base64

# Initialize retriever
retriever = Retriever()

# Page setup
st.set_page_config(page_title="NyayaAI SMS Demo", layout="centered")
st.title("📱 NyayaAI — SMS-based Legal Rights Assistant")

# --- SESSION STATE SETUP ---
if "reply" not in st.session_state:
    st.session_state.reply = ""
if "lang" not in st.session_state:
    st.session_state.lang = "en"

# --- USER INPUT ---
user_input = st.text_input("📩 Type your question (like an SMS):")

# --- SEND BUTTON ---
if st.button("Send"):
    if not user_input.strip():
        st.warning("Please type a question first.")
    else:
        lang = detect_language(user_input)
        intent = detect_intent(user_input)
        results = retriever.retrieve(user_input)
        reply = compose_response(intent, results, lang)

        # store in session
        st.session_state.reply = reply
        st.session_state.lang = lang

# --- DISPLAY REPLY (persisted, single display) ---
if st.session_state.reply:
    st.success(st.session_state.reply)

    # --- AUDIO OPTION ---
    if st.checkbox("🔈 Hear this message"):
        try:
            tts_lang = 'ta' if st.session_state.lang == 'ta' else 'en'
            tts = gTTS(text=st.session_state.reply, lang=tts_lang, slow=False)

            # Generate in memory
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)

            # Convert to base64 for HTML player
            b64 = base64.b64encode(audio_buffer.read()).decode()
            audio_html = f"""
            <audio controls autoplay style="margin-top:10px; width: 100%;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                Your browser does not support audio playback.
            </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Audio generation failed: {e}")
