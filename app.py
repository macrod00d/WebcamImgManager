import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import os

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.sqlite import JSON

engine = create_engine('sqlite:///image_metadata.db', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

from typing import List
def insert_image_metadata(title: str, description: List[str], filepath: str) -> None:
    # Create a new session

    session = Session()
    try:
        # Create a new ImageMetadataModel instance with the provided data
        new_image_metadata = ImageMetadataModel(
            title=title,
            description=description,
            filepath=filepath
        )
        
        # Add the new instance to the session
        session.add(new_image_metadata)
        
        # Commit the session to save the data to the database
        session.commit()
        print(f"Image metadata for '{title}' added successfully.")
    except Exception as e:
        # Rollback the session in case of error
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        # Close the session
        session.close()

class ImageMetadataModel(Base):
    __tablename__ = 'image_metadata'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)  # Timestamp is generated when a record is inserted
    filepath = Column(String, nullable=False)

# Function to save the image with a timestamp
def save_image(cv2_img, base_path='./img'):
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"img_{timestamp}.png"
    save_path = os.path.join(base_path, filename)
    cv2.imwrite(save_path, cv2_img)
    return save_path

# Initialize session state
if 'page' not in st.session_state:
    st.session_state['page'] = 'capture'

def details_form():
    st.subheader("Enter details for your image")
    with st.form(key='details_form'):
        # Initialize session state for title and description if not present
        if 'title' not in st.session_state:
            st.session_state['title'] = ''
        if 'description' not in st.session_state:
            st.session_state['description'] = ''

        # Create text input fields within the form
        title = st.text_input("Title", value=st.session_state['title'])
        description = st.text_area("Description", value=st.session_state['description'])

        # Create a form submit button
        submitted = st.form_submit_button("Submit Details")
        if submitted:
            # Update session state with the latest input values
            st.session_state['title'] = title
            st.session_state['description'] = description

            # Call the callback function to handle the form submission
            submit_details_cb()

def submit_details_cb():
    # Retrieve title and description from st.session_state
    title = st.session_state.get('title', '')
    description = st.session_state.get('description', '')

    # Continue with the database insertion using the retrieved values
    if 'image_path' in st.session_state:
        insert_image_metadata(title, description, st.session_state['image_path'])
        st.success(f"Image metadata for '{title}' added successfully.")
        # Reset the form and go back to capture page
        st.session_state.page = 'capture'
        # Optionally, clear the form inputs
        st.session_state['title'] = ''
        st.session_state['description'] = ''
        st.rerun()

def capture_form():
    with st.form("capture_form"):
        img_file_buffer = st.camera_input("Take a picture")

        # The form_submit_button is the trigger for the form submission
        submitted = st.form_submit_button("Save Image")

        if submitted:
            if img_file_buffer is not None:
                # If an image has been taken and the button is clicked, call the save_image_cb
                save_image_cb(img_file_buffer)
            else:
                # If no image has been taken, display a warning message
                st.warning("Please take a picture before saving.")

def save_image_cb(img_file_buffer):
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    save_path = save_image(cv2_img)
    st.session_state['image_path'] = save_path  # Save path in session state
    st.session_state.page = 'details'  # Change page to details form
    st.experimental_rerun()

def main():
    # Initialize session state for page navigation if not present
    if 'page' not in st.session_state:
        st.session_state['page'] = 'capture'

    # Main logic for page navigation
    if st.session_state.page == 'capture':
        capture_form()
    elif st.session_state.page == 'details':
        if 'image_path' in st.session_state:
            st.image(st.session_state['image_path'], caption="Captured Image", width=200)
        details_form()

if __name__ == "__main__":
    main()