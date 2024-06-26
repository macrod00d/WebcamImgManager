import streamlit as st
import cv2
import numpy as np
import os
from datetime import datetime
from components import details_form, capture_form
from models import ImageMetadataDAO

# Instantiate the DAO for database operations
metadata_dao = ImageMetadataDAO()

def save_image(cv2_img, base_path='./img'):
    """
    Save the OpenCV image to a file.

    Parameters:
    - cv2_img: The OpenCV image to be saved.
    - base_path: The base path where the image will be saved. Default is './img'.

    Returns:
    - save_path: The path where the image is saved.
    """
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"img_{timestamp}.png"
    save_path = os.path.join(base_path, filename)
    cv2.imwrite(save_path, cv2_img)
    cv2.imwrite(f"{save_path[:-4]}-ORIGINAL.png", cv2_img)
    return save_path

def submit_details_cb():
    """
    Callback function for submitting image details.

    It retrieves the title, description, and tags from the session state and adds the image metadata to the database.
    If successful, it displays a success message, resets the session state, and reruns the app.
    Otherwise, it displays an error message.
    """
    title = st.session_state.get('title', '')
    description = st.session_state.get('description', '')
    tags = st.session_state.get('tags', '')
    if 'image_path' in st.session_state and title and description:
        metadata = metadata_dao.add_image_metadata(title, description, st.session_state['image_path'], tags)
        if metadata:
            st.success(f"Image metadata for '{title}' added successfully.")
            st.session_state.page = 'capture'
            st.session_state['title'] = ''
            st.session_state['description'] = ''
            st.session_state['tags'] = ''
            st.rerun()
        else:
            st.error('Failed to add image metadata.')

def save_image_cb(img_file_buffer):
    """
    Callback function for saving the captured image.

    It decodes the image file buffer, saves the image, and updates the session state with the image path.
    If successful, it switches the app page to 'details' and reruns the app.
    Otherwise, it displays an error message.
    """
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    save_path = save_image(cv2_img)
    if save_path:
        st.session_state['image_path'] = save_path
        st.session_state.page = 'details'
        st.rerun()
    else:
        st.error('Failed to save the image.')

def main():
    """
    Main function of the app.

    It sets up the app title and session state variables.
    Depending on the current app page, it displays the capture form or the details form.
    """
    st.title("Webcam Picture Capture")
    st.subheader("Capture an image and add metadata")
    st.caption("Please click the take photo button to capture an image and press save to proceed to labelling. You will then be prompted to input data and save the image to the db.\n\n Note you may have to allow the browser access to the camera before the video will appear.")

    st.sidebar.page_link("pages/scan_page.py", label="Scan", icon="📸")
    st.sidebar.page_link("pages/edit_page.py", label="Edit", icon="📝")
    st.sidebar.page_link("pages/settings.py", label="Settings", icon="⚙️")
    
    if 'page' not in st.session_state:
        st.session_state['page'] = 'capture'
    if 'title' not in st.session_state:
        st.session_state['title'] = ''
    if 'description' not in st.session_state:
        st.session_state['description'] = ''
    if 'tags' not in st.session_state:
        st.session_state['tags'] = ''
    
    if st.session_state.page == 'capture':
        capture_form(save_image_cb)
    elif st.session_state.page == 'details':
        if 'image_path' in st.session_state:
            st.image(st.session_state['image_path'], caption="Captured Image", width=175) #display the captured image and resize to fit
        details_form(submit_details_cb)

if __name__ == "__main__":
    main()