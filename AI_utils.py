import streamlit as st

import base64
import requests

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def describe_image(image_path):

    try:
        api_key = st.session_state['api_key']
    except KeyError:
        st.error("Please set your OpenAI API key in the Settings page.")
        return "API Key Has Not Been Set, please set it in the settings page."

    base64_image = encode_image(image_path)

    headers = {   
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Provide a description of this image"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    try:
        return response.json()['choices'][0]['message']['content']
    except KeyError:
        return response.json()