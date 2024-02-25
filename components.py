import streamlit as st
from streamlit_tags import st_tags

def details_form(submit_details_cb):
    """
    Renders form for entering details of image after image has been captured using capture_form.

    Args:
        submit_details_cb (function): Callback function to be executed when details are submitted.
    """
    st.subheader("Enter details for your image")
    with st.form(key='details_form'):
        title = st.text_input("Title", value=st.session_state.get('title', ''))
        description = st.text_area("Description", value=st.session_state.get('description', ''))
        # tags = st.text_input("Tags (comma-separated)", value=st.session_state.get('tags', ''))
        # tagz = st.multiselect("Relevant Tags", ['Webcam'])
        tags = st_tags(
            label='## Enter tags:',
            text='You can type another tag, enter to save',
            value=['Webcam','Selfie'],
            suggestions=['Webcam','Selfie'],
            maxtags = -1,
            key='1')
        submitted = st.form_submit_button("Submit Details")
        if submitted:
            if not title or not description or not tags:
                if not title:
                    st.warning('Title is required.')
                if not description:
                    st.warning('Description is required.')
                if not tags:
                    st.warning('Tags are required.')
                st.stop()
            else:
                st.session_state['title'] = title
                st.session_state['description'] = description
                st.session_state['tags'] = [tag.strip() for tag in tags]
                submit_details_cb()

def capture_form(save_image_cb):
    """
    Renders form for capturing and saving an image using st.camera_input.

    Args:
        save_image_cb (function): Callback function to be executed when image is saved.
    """
    with st.form("capture_form"):
        img_file_buffer = st.camera_input("Take a picture")
        submitted = st.form_submit_button("Save Image")
        if submitted:
            if img_file_buffer is not None:
                save_image_cb(img_file_buffer)
            else:
                st.warning("Please take a picture before saving.")