import streamlit as st
import pathlib
import textwrap
import google.generativeai as genai
from gtts import gTTS
import PIL.Image
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to convert text to Markdown format
def to_markdown(text):
    """Convert text to Markdown format with proper indentation."""
    text = text.replace('•', '  *')  # Convert bullet points for Markdown
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Streamlit app layout
def main():
    st.title("Gemini 1.0 Pro Vision - Image Analysis and Text Generation")
    
    # File uploader for images
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

    if uploaded_file is not None:
        try:
            # Display the uploaded image
            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

            # Load the image for processing
            img = PIL.Image.open(uploaded_file)

            # Generate content using the Gemini model
            response = model.generate_content(img)
            generated_text = response.text

            # Convert and display the generated text in Markdown format
            st.write("Generated Text:")
            st.markdown(to_markdown(generated_text))

            # Convert generated text to speech and play audio
            tts = gTTS(generated_text)
            audio_path = 'output.mp3'
            tts.save(audio_path)
            st.audio(audio_path, format='audio/mp3', start_time=0)

            # Clean up the audio file after use
            if os.path.exists(audio_path):
                os.remove(audio_path)

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # Configure Google API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        st.error("API key not found. Please provide a valid API key in the .env file.")
    else:
        genai.configure(api_key=api_key)

        # List available models (optional)
        # Uncomment the code below to list models that support 'generateContent'
        # for m in genai.list_models():
        #     if 'generateContent' in m.supported_generation_methods:
        #         st.write("Model Name:", m.name)

        # Load the Gemini model
        try:
            model = genai.GenerativeModel("gemini-1.5-pro")
            main()
        except Exception as e:
            st.error(f"Failed to load the model: {e}")
