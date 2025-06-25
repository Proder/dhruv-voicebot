import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import uuid
import asyncio
import edge_tts
from io import BytesIO
import base64
from personality import get_personality_prompt, get_system_instructions

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API Key not found. Please set GOOGLE_API_KEY in your environment or Streamlit secrets.")
    st.stop()

genai.configure(api_key=api_key)

st.set_page_config(
    page_title="Dhruv AI - Personal Voice Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title with improved styling
st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #1f77b4; margin-bottom: 0.5rem;'>🧠 Dhruv AI</h1>
        <p style='color: #666; font-size: 1.1rem;'>Personal Voice Assistant</p>
    </div>
""", unsafe_allow_html=True)

# Initialize components
try:
    recognizer = sr.Recognizer()
    model = genai.GenerativeModel("gemini-1.5-flash")
    PERSONALITY_PROMPT = get_personality_prompt()
except Exception as e:
    st.error(f"Initialization error: {str(e)}")
    st.stop()

if "persona_added" not in st.session_state:
    st.session_state.persona_added = True

# Record audio with improved error handling
def record_audio():
    try:
        with sr.Microphone() as source:
            # Adjust for ambient noise for better recognition
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            st.info("🎙️ Speak now...")
            # Increased timeout and phrase time limit for better capture
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
        
        with st.spinner("Processing speech..."):
            text = recognizer.recognize_google(audio)
            st.success(f"Heard: {text}")
            return text
            
    except sr.WaitTimeoutError:
        st.warning("No speech detected. Please try again.")
    except sr.UnknownValueError:
        st.error("Could not understand audio. Please speak clearly.")
    except sr.RequestError as e:
        st.error(f"Speech recognition service error: {str(e)}")
    except Exception as e:
        st.error(f"Audio recording error: {str(e)}")
    
    return None

# Use Edge TTS


# Generate audio with improved error handling
def speak_text(text, voice="en-GB-RyanNeural"):
    try:
        # Clean and validate text
        if not text or not text.strip():
            return None
            
        # Limit text length to avoid very long audio files
        if len(text) > 1000:
            text = text[:1000] + "..."
        
        audio_buffer = BytesIO()

        async def generate_audio():
            try:
                communicate = edge_tts.Communicate(text, voice)
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_buffer.write(chunk["data"])
                audio_buffer.seek(0)
            except Exception as e:
                st.error(f"Audio generation error: {str(e)}")
                return None

        asyncio.run(generate_audio())
        
        if audio_buffer.getvalue():
            return audio_buffer
        else:
            return None
            
    except Exception as e:
        st.error(f"Speech generation error: {str(e)}")
        return None

# Streamlit audio playback with error handling
def display_audio(audio_bytes_io):
    try:
        if audio_bytes_io is None:
            st.error("No audio to play")
            return
        
        audio_bytes_io.seek(0)
        audio_data = audio_bytes_io.read()
        
        if not audio_data:
            st.error("Empty audio file")
            return
        
        b64 = base64.b64encode(audio_data).decode()
        audio_html = f"""
            <audio controls autoplay style="width: 100%; margin: 10px 0;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Audio playback error: {str(e)}")

# Add welcome message for new users
if not st.session_state.chat_history:
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
            <p style='margin: 0; text-align: center; color: #666;'>
                👋 Hi! I'm Dhruv's AI assistant. Ask me about his background, projects, or experiences!
                <br><small>You can type your question or use the mic button 🎤</small>
            </p>
        </div>
    """, unsafe_allow_html=True)


# Render all messages with improved styling
with st.container():
    for entry in st.session_state.chat_history:
        if entry["type"] == "user":
            st.markdown(f"""
                <div style='background-color: #e3f2fd; padding: 10px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #2196f3;'>
                    <strong>🧑 You:</strong> {entry['content']}
                </div>
            """, unsafe_allow_html=True)
        elif entry["type"] == "bot":
            st.markdown("""
                <div style='background-color: #f3e5f5; padding: 10px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #9c27b0;'>
                    <strong>🧠 Dhruv:</strong>
                </div>
            """, unsafe_allow_html=True)
            display_audio(entry["content"])

# Input area with improved styling
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 25px;
        padding: 12px 20px;
        font-size: 16px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #007bff;
        box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([8, 1])

# Initialize input clearing mechanism and counter for forcing widget reset
if "input_counter" not in st.session_state:
    st.session_state.input_counter = 0

with col1:
    # Use dynamic key to force widget recreation and clearing
    user_input = st.text_input("Type your message", key=f"text_input_{st.session_state.input_counter}", 
                              label_visibility="collapsed", placeholder="Ask me anything about Dhruv...")
with col2:
    mic = st.button("🎤", help="Click to speak", use_container_width=True)

# Capture mic input
if mic:
    spoken = record_audio()
    if spoken:
        user_input = spoken

# Process input with improved error handling
if user_input and user_input.strip():  # Check for non-empty input
    # Check if this input was already processed
    if "last_processed_input" not in st.session_state:
        st.session_state.last_processed_input = ""
    
    # Only process if it's a new input
    if user_input != st.session_state.last_processed_input:
        # Mark this input as processed
        st.session_state.last_processed_input = user_input
        
        # Add user message to history
        st.session_state.chat_history.append({"type": "user", "content": user_input})

        # Build prompt
        prompt = f"{PERSONALITY_PROMPT}\nUser: {user_input}"

        # Generate reply with error handling
        try:
            with st.spinner("Dhruv is thinking..."):
                response = model.generate_content(prompt)
                reply_text = response.text

                # Generate audio from response
                audio_bytes = speak_text(reply_text)

            # Only append if audio was generated successfully
            if audio_bytes:
                st.session_state.chat_history.append({"type": "bot", "content": audio_bytes})
            else:
                st.error("Failed to generate audio response")

            # Increment counter to force new widget creation (clears input)
            st.session_state.input_counter += 1

            # Rerun to update the display
            st.rerun()
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            # Remove the user message from history if processing failed
            if st.session_state.chat_history and st.session_state.chat_history[-1]["type"] == "user":
                st.session_state.chat_history.pop()

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 2rem; padding: 1rem; color: #666; font-size: 0.9rem;'>
        <a href='https://dhruvshah-portfolio.vercel.app/' target='_blank'>Dhruv's Portfolio</a>
    </div>
""", unsafe_allow_html=True)