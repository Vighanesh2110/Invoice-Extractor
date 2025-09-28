import os
import streamlit as st

from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# Initialize Google API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-2.0-flash")

# Function to load image details
def get_gemini_response(user_input, image_parts, context_text):
    # Convert raw bytes to base64
    image_b64 = base64.b64encode(image_parts[0]["data"]).decode("utf-8")

    response = model.generate_content([
        {
            "role": "user",
            "parts": [
                {"text": context_text},
                {"text": user_input},
                {
                    "inline_data": {
                        "mime_type": image_parts[0]["mime_type"],
                        "data": image_b64
                    }
                }
            ]
        }
    ])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App setup
st.set_page_config(page_title="Multilanguage Invoice Extractor", layout="centered")

# Custom CSS for styling with AI animation background and improved UI
st.markdown(
    """
    <style>
    /* Custom styling */
    body {
        background-color:rgb(172, 59, 59);
        font-family: 'Arial', sans-serif;
        background: url('https://your-animation-url.com/ai-animation.gif') no-repeat center center fixed;
        background-size: cover;
        animation: fadeIn 2s ease-in-out;
    }
    
    /* Button Styling */
    .stButton button {
        background-color: #007BFF;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 15px 25px;
        width: 100%;
        transition: background-color 0.3s;
    }
    
    .stButton button:hover {
        background-color: #0056b3;
    }

    /* File uploader */
    .stFileUploader {
        border: 2px dashed #007BFF;
        padding: 20px;
        border-radius: 8px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    
    .stFileUploader:hover {
        transform: scale(1.05);
        border-color: #0056b3;
    }

    /* Input fields */
    .stTextInput input {
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #ddd;
        width: 100%;
        margin-bottom: 20px;
        transition: border-color 0.2s;
    }

    .stTextInput input:focus {
        border-color: #007BFF;
    }

    /* Image display */
    .stImage {
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }

    /* Footer styling */
    footer {
        visibility: hidden;
    }

    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Header and Description
st.title("🧾 MultiLanguage Invoice Extractor")
st.write("""
    This tool uses AI to extract and understand information from invoices in various languages.
    Upload your invoice image and get insights about it in just a few clicks!
    """)
st.markdown("---")

# Input section
st.markdown("### 📥 Input Details")
input_prompt = st.text_input("What would you like to know about the invoice?", key="input", placeholder="e.g., 'What is the total amount?'")

# File uploader section
st.markdown("### 📸 Upload Invoice Image")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice Image", use_container_width=True)  # ✅ updated here

# Submit button and output section
submit = st.button("🔍 Extract Details")

if submit:
    if uploaded_file is None:
        st.warning("Please upload an image of the invoice first.")
    elif input_prompt.strip() == "":
        st.warning("Please enter a prompt to ask about the invoice.")
    else:
        try:
            image_data = input_image_details(uploaded_file)
            response = get_gemini_response(
                input_prompt,
                image_data,
                "You are an expert in understanding invoices. Analyze the provided invoice and answer the question."
            )
            
            # Display response
            st.subheader("💡 The Response is:")
            st.write(response)
        except FileNotFoundError as e:
            st.error(f"Error: {e}")

# Footer section
st.markdown("""
    ---
    Made with ❤️ by InvoIntelli. 
    """)


#for running program type this command in terminal = "python -m streamlit run app.py"

