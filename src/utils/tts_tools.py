# src/utils/tts_tools.py
import edge_tts
import asyncio
import uuid
from pathlib import Path
import tempfile

# Map ISO language -> Microsoft neural voice
VOICE_MAP = {
    "hi": "hi-IN-SwaraNeural",
    "ta": "ta-IN-PallaviNeural",
    "te": "te-IN-ShrutiNeural",
    "kn": "kn-IN-SapnaNeural",
    "bn": "bn-IN-TanishaaNeural",
    "mr": "mr-IN-AarohiNeural",
    "gu": "gu-IN-DhwaniNeural",
    "pa": "pa-IN-AmanNeural",
    "en": "en-IN-NeerjaNeural",
}

async def _tts_async(text: str, voice: str, out_file: str):
    communicate = edge_tts.Communicate(text, voice)
    # communicate.save() is available in new edge-tts versions
    await communicate.save(out_file)
    return out_file

def generate_tts(text: str, lang: str = "en") -> str:
    """
    Generate TTS mp3 for `text` in language `lang` (ISO code like 'hi','ta','en').
    Returns local mp3 filepath.
    """
    voice = VOICE_MAP.get(lang[:2], VOICE_MAP["en"])
    outfile = Path(tempfile.gettempdir()) / f"nyayaai_tts_{uuid.uuid4().hex}.mp3"
    # run async
    asyncio.run(_tts_async(text, voice, str(outfile)))
    return str(outfile)
