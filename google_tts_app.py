import streamlit as st
from google.cloud import texttospeech
from io import BytesIO

# Google Cloud Text-to-Speech Function
def generate_audio_google(text, language="en-US", voice_name="en-US-Wavenet-F", audio_format="MP3"):
    """Generate audio using Google Cloud Text-to-Speech."""
    try:
        # Initialize the Text-to-Speech client
        client = texttospeech.TextToSpeechClient()

        # Configure the text input
        input_text = texttospeech.SynthesisInput(text=text)

        # Configure the voice
        voice = texttospeech.VoiceSelectionParams(
            language_code=language,
            name=voice_name
        )

        # Configure the audio format
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding[audio_format]
        )

        # Request audio synthesis
        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )

        # Save audio content to a BytesIO object
        audio_stream = BytesIO(response.audio_content)
        audio_stream.seek(0)  # Reset pointer to the start
        return audio_stream
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit App
st.title("Google Cloud Text-to-Speech App")

# Input for Text-to-Speech
sample_text = st.text_area("Enter text to convert to speech:", height=200, placeholder="Type your text here...")

# Language and Voice Selection
language = st.selectbox("Select Language", ["English (US)", "German", "Dutch"])
voice_options = {
    "English (US)": ("en-US", "en-US-Wavenet-F"),
    "German": ("de-DE", "de-DE-Wavenet-F"),
    "Dutch": ("nl-NL", "nl-NL-Wavenet-F")
}
selected_language_code, selected_voice_name = voice_options[language]

# Generate and Play Audio
if st.button("Convert to Speech"):
    if sample_text.strip():  # Ensure text is not empty
        st.info(f"Generating audio in {language}...")
        audio_file = generate_audio_google(
            text=sample_text,
            language=selected_language_code,
            voice_name=selected_voice_name,
            audio_format="MP3"
        )
        if isinstance(audio_file, BytesIO):
            # Streamlit audio playback
            audio_bytes = audio_file.getvalue()  # Extract raw audio bytes
            st.success("Audio generated successfully! Playing below:")
            st.audio(audio_bytes, format="audio/mp3", start_time=0)
        else:
            st.error(audio_file)  # Display error if audio generation fails
    else:
        st.warning("Please enter some text to convert.")
