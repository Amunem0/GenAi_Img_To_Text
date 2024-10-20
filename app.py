import streamlit as st
import pathlib
import textwrap
import google.generativeai as genai
from gtts import gTTS
import PIL.Image
import os
from dotenv import load_dotenv

load_dotenv()

def to_markdown(text):
    """Convert text to Markdown format with proper indentation."""
    text = text.replace('•', '  *') 
    return textwrap.indent(text, '> ', predicate=lambda _: True)


def main():
    st.title("Image Analysis and Text Generation")
    
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

    if uploaded_file is not None:
        try:
            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

            img = PIL.Image.open(uploaded_file)

            response = model.generate_content(img)
            generated_text = response.text

            st.write("Generated Text:")
            st.markdown(to_markdown(generated_text))

            tts = gTTS(generated_text)
            audio_path = 'output.mp3'
            tts.save(audio_path)
            st.audio(audio_path, format='audio/mp3', start_time=0)

            if os.path.exists(audio_path):
                os.remove(audio_path)

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    if not api_key:
        st.error("API key not found. Please provide a valid API key in the .env file.")
    else:
        genai.configure(api_key=api_key)

        try:
            model = genai.GenerativeModel("gemini-1.5-pro")
            main()
        except Exception as e:
            st.error(f"Failed to load the model: {e}")
