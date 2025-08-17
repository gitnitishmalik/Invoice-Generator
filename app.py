from dotenv import load_dotenv

load_dotenv()

from huggingface_hub import upload_file
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-2.5-flash') 

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data  
        }]
        return image_parts
    else:
        raise FileNotFoundError("No image uploaded")

st.set_page_config(page_title="Multi Language Invoice Extractor")

st.header("Multi Language Invoice Extractor")
input = st.text_input("input Prompt: ", key="input")
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], key="image")
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

submit = st.button("Tell me about the Invoice")

input_prompt = """
You are an expert in understanding invoices. We will upload an image as invoice
and you will have to answer any question based on the uploaded invoice image
"""

# submit button clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input, image_data, input_prompt)
    st.subheader("Response:")
    st.write(response)
