import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import os

from dbUtils import insert_image_metadata, init_db
from components import details_form, capture_form

def save_image(cv2_img, base_path='./img'):
    """
    Save the OpenCV image to a file.

    Args:
        cv2_img (numpy.ndarray): The OpenCV image.
        base_path (str, optional): The base path to save the image. Defaults to './img'.

    Returns:
        str: The path to the saved image.
    """
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"img_{timestamp}.png"
    save_path = os.path.join(base_path, filename)
    cv2.imwrite(save_path, cv2_img)
    return save_path

def submit_details_cb():
    """
    Callback function for submitting image details.

    This function retrieves the title and description from the session state,
    inserts the image metadata into the database, and resets the session state.
    """
    title = st.session_state.get('title', '')
    description = st.session_state.get('description', '')
    if 'image_path' in st.session_state:
        # Insert the image metadata into the database
        try:
            insert_image_metadata(title, description, st.session_state['image_path'])
            st.success(f"Image metadata for '{title}' added successfully.")
        except Exception as e:
            st.error(f"Error inserting image metadata: {e}")

        # Reset the session state
        st.session_state.page = 'capture'
        st.session_state['title'] = ''
        st.session_state['description'] = ''
        st.rerun() #neded to ensure the session state is reset

def save_image_cb(img_file_buffer):
    """
    Callback function for saving the captured image.

    This function decodes the image file buffer, saves the image, and updates the session state.
    
    Args:
        img_file_buffer (BytesIO): The image file buffer.
    """
    bytes_data = img_file_buffer.getvalue()
    
    try:
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    except Exception as e:
        st.error(f"Error decoding image: {e}")
    try:
        save_path = save_image(cv2_img)
    except Exception as e:
        st.error(f"Error saving image: {e}")

    # Update the session state
    st.session_state['image_path'] = save_path
    st.session_state.page = 'details'
    st.rerun()

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'capture'
    if st.session_state.page == 'capture':
        capture_form(save_image_cb)
    elif st.session_state.page == 'details':
        if 'image_path' in st.session_state:
            st.image(st.session_state['image_path'], caption="Captured Image", width=200)
        details_form(submit_details_cb)

if __name__ == "__main__":
    init_db()
    main()