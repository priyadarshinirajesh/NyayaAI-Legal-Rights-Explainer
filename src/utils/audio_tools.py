# src/utils/audio_tools.py
import streamlit as st
from audiorecorder import audiorecorder

def record_audio():
    audio = audiorecorder("🎤", "🛑")
    if len(audio) > 0:
        filepath = "voice_input.wav"
        audio.export(filepath, format="wav")
        return filepath
    return None
