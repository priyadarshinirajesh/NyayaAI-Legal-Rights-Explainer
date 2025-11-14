import streamlit as st
from pathlib import Path
import sys
import json
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import settings
from config.logging_config import log
from src.core.retriever import HybridRetriever
from src.nlp.query_processor import QueryProcessor
from src.generation.response_generator import ResponseGenerator
from src.nlp.translator import Translator
from gtts import gTTS
import pyttsx3
import base64
from io import BytesIO

# Initialize components
@st.cache_resource
def init_components():
    """Initialize all components"""
    retriever = HybridRetriever()
    query_processor = QueryProcessor()
    response_generator = ResponseGenerator()
    translator = Translator()
    return retriever, query_processor, response_generator, translator

def main():
    st.set_page_config(
        page_title="NyayaAI - Legal Rights Assistant",
        page_icon="⚖️",
        layout="wide"
    )
    
    # Header
    st.title("⚖️ NyayaAI - Your Legal Rights Assistant")
    st.markdown("**Get simple explanations of your legal rights in your language**")
    
    # Initialize components
    retriever, query_processor, response_generator, translator = init_components()
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # Language selection
        language = st.selectbox(
            "Select Language",
            options=list(settings.SUPPORTED_LANGUAGES.keys()),
            format_func=lambda x: settings.SUPPORTED_LANGUAGES[x]
        )
        
        # Category filter
        category = st.selectbox(
            "Select Category",
            options=['All', 'Pension', 'Domestic Violence', 'Land', 'Labor'],
            index=0
        )
        
        # Voice options
        use_voice = st.checkbox("Enable Voice Output", value=True)
        
        # User context
        st.subheader("Your Information (Optional)")
        user_state = st.selectbox(
            "State",
            options=['', 'Delhi', 'Maharashtra', 'Tamil Nadu', 'Karnataka', 'Other'],
            index=0
        )
        
        user_type = st.multiselect(
            "I am a",
            options=['Woman', 'Senior Citizen', 'Person with Disability', 'Worker', 'Farmer'],
            default=[]
        )
        
        # Help section
        st.markdown("---")
        st.subheader("📞 Emergency Contacts")
        st.markdown("""
        - **Women Helpline:** 181
        - **Police:** 100
        - **Legal Aid:** 15100
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Query input
        st.subheader("Ask Your Question")
        
        # Sample questions
        sample_questions = [
            "How to apply for widow pension?",
            "My husband beats me, what should I do?",
            "My employer has not paid my salary",
            "Government wants to take my land"
        ]
        
        selected_sample = st.selectbox(
            "Or select a sample question:",
            options=[''] + sample_questions,
            index=0
        )
        
        user_query = st.text_area(
            "Type your question here:",
            value=selected_sample,
            height=100,
            placeholder="Example: How can I apply for old age pension?"
        )
        
        # Voice input button (placeholder)
        col1_1, col1_2, col1_3 = st.columns([1, 1, 2])
        with col1_1:
            if st.button("🎤 Voice Input", disabled=True):
                st.info("Voice input coming soon!")
        
        with col1_2:
            search_button = st.button("🔍 Search", type="primary")
    
    # Process query
    if search_button and user_query:
        with st.spinner("Finding information..."):
            
            # Build user context
            user_context = {
                'language': language,
                'state': user_state,
                'user_type': user_type,
                'category': category.lower() if category != 'All' else None
            }
            
            # Process query
            query_info = query_processor.process_query(user_query, user_context)
            
            # Retrieve documents
            retrieved_docs = retriever.retrieve_with_context(
                query_info['expanded_query'],
                user_context,
                k=5
            )
            
            # Generate response
            response = response_generator.generate_response(
                query_info,
                retrieved_docs,
                user_context
            )
            
            # Display response
            st.markdown("---")
            st.subheader("📋 Answer")
            
            # Main answer
            st.info(response['answer'])
            
            # Emergency info if urgent
            if response.get('emergency_info'):
                st.error(f"**Emergency Contact:** {response['emergency_info']['name']} - {response['emergency_info']['helpline']}")
            
            # Practical steps
            if response.get('practical_steps'):
                st.subheader("✅ What You Should Do")
                for i, step in enumerate(response['practical_steps'], 1):
                    st.markdown(f"{i}. {step}")
            
            # Voice output
            if use_voice:
                try:
                    # Generate audio
                    tts = gTTS(text=response['answer'], lang=language if language != 'en' else 'en-in')
                    audio_buffer = BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    
                    # Display audio player
                    st.audio(audio_buffer, format='audio/mp3')
                except Exception as e:
                    log.error(f"TTS error: {e}")
                    st.warning("Voice output not available")
            
            # Sources
            if response.get('sources'):
                with st.expander("📚 Sources"):
                    for source in response['sources']:
                        st.markdown(f"- {source}")
            
            # Confidence
            confidence_percent = int(response.get('confidence', 0) * 100)
            st.progress(confidence_percent / 100)
            st.caption(f"Confidence: {confidence_percent}%")
            
            # Follow-up questions
            if response.get('follow_up_questions'):
                st.subheader("❓ Related Questions")
                for question in response['follow_up_questions']:
                    st.markdown(f"• {question}")
    
    with col2:
        # Information panel
        st.subheader("ℹ️ How to Use")
        st.markdown("""
        1. **Type or speak** your legal question
        2. **Select language** if not English
        3. **Get simple explanation** of your rights
        4. **Follow the steps** provided
        5. **Contact helpline** if urgent
        """)
        
        st.subheader("📱 SMS Service")
        st.info("Send your question to **+91-XXXXXXXXXX** to get help via SMS")
        
        st.subheader("🔒 Privacy")
        st.success("Your questions are private and not stored")

if __name__ == "__main__":
    main()