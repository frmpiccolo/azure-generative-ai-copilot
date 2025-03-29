import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.api import ask_openai
from app.ocr import extract_text_from_image_file
from app.processor import save_response
from io import BytesIO

st.set_page_config(page_title="Azure Generative AI Copilot")
st.title("🤖 Azure Generative AI Copilot")

tab1, tab2 = st.tabs(["Text / Image Prompt", "Graph API"])

with tab1:
    prompt_input = st.text_area("Type your prompt:", height=150)
    uploaded_file = st.file_uploader("...or upload a .txt, .png or .jpg file", type=["txt", "png", "jpg", "jpeg"])

    if st.button("Generate"):
        if uploaded_file:
            if uploaded_file.type.startswith("image"):
                prompt = extract_text_from_image_file(uploaded_file)
            else:
                prompt = uploaded_file.read().decode("utf-8")
        elif prompt_input:
            prompt = prompt_input
        else:
            st.warning("Please provide a prompt or file.")
            st.stop()

        with st.spinner("Generating..."):
            response = ask_openai(prompt)
            save_response("web_input_response.txt", response)

        st.success("Done!")
        st.text_area("AI Response", response, height=300)
        st.download_button("💾 Download result", response, file_name="web_input_response.txt")

with tab2:
    st.markdown("👉 Use the CLI to interact with Outlook or OneDrive via Microsoft Graph.")
    st.code("python -m app.main read-emails", language="bash")
    st.code("python -m app.main read-onedrive", language="bash")
