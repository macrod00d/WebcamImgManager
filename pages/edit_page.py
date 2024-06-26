import streamlit as st
from models import ImageMetadataDAO, ImageMetadataModel
from streamlit_modal import Modal
from streamlit_tags import st_tags
from AI_utils import describe_image

st.sidebar.page_link("pages/scan_page.py", label="Scan", icon="📸")
st.sidebar.page_link("pages/edit_page.py", label="Edit", icon="📝")
st.sidebar.page_link("pages/settings.py", label="Settings", icon="⚙️")


# Initialize the Data Access Object
dao = ImageMetadataDAO()

# Fetch all image metadata from the database
images_metadata = dao.get_all_image_metadata()

# Set a title for the Streamlit app
st.title('Browse Captured Images')
st.caption('Click the "Edit" button to modify the metadata for each image.')

# Calculate the number of rows needed for the grid
num_images = len(images_metadata)
num_columns = 3
num_rows = (num_images + num_columns - 1) // num_columns

# Create containers for each row
rows = [st.columns(num_columns) for _ in range(num_rows)]

# Placeholder for the modal
edit_modal = Modal(
    "Edit Image Metadata",
    key="edit-modal",
    padding=20,
    max_width=744
)

# Function to display the edit form within the modal
def display_edit_form(image_id):
    """
    Display the edit form for a specific image.

    Parameters:
    image_id (int): The ID of the image to edit.

    Returns:
    None
    """
    if edit_modal.is_open():
        with edit_modal.container():
            # Retrieve the specific image metadata from the database
            image_metadata = dao.get_image_metadata(image_id)

            # Display the image and current metadata
            st.image(image_metadata.filepath, use_column_width=True)
            new_title = st.text_input("Title", value=image_metadata.title, key=f"title-{image_id}")
            new_description = st.text_area("Description", value=image_metadata.description or "", key=f"desc-{image_id}")
            image_describe = st.button("Get AI Generated Description (WARNING - existing description will be overwritten)", key=f"add-desc-{image_id}")
            loading_message = st.empty()


            tags = st_tags(
                label='## Enter tags:',
                text='You can type another tag, enter to save',
                value=image_metadata.tags.split(', '),
                suggestions=['Webcam','Selfie'],
                maxtags = -1,
                key=f"tags-{image_id}"
            )

            selected_filter = st.selectbox(
                "Filter",
                options=["None", "Greyscale", "Sepia", "Sketch", "Invert"],
                index=0,
                key=f"filter-{image_id}"
            )

            brightness_factor = st.slider("Brightness", 0.5, 1.5, 1.0, 0.01, key=f"brightness-{image_id}")
            contrast_factor = st.slider("Contrast", 0.5, 1.5, 1.0, 0.01, key=f"contrast-{image_id}")



            # Create columns for Submit and Delete buttons
            col1, col2, col3 = st.columns(3)
            
            # Submit button for the form
            submit_changes = col1.button("Submit Changes", key=f"submit-{image_id}")
            
            # Delete button for the form
            delete_image = col2.button("Delete Image", key=f"delete-{image_id}")

            restore_image = col3.button("Restore Image", key=f"restore-{image_id}")

            # If the submit button is pressed, update the database and close the modal
            if image_describe:
                loading_message.text("Description Generation in Progress, this may take a while...")
                new_description = describe_image(image_metadata.filepath)
                print(new_description)
                
                dao.update_image_metadata(image_id, new_title, new_description, tags)
                loading_message.empty()
                st.experimental_rerun()

            if submit_changes:
                if selected_filter == "Greyscale":
                    dao.apply_greyscale_effect(image_id)
                elif selected_filter == "Sepia":
                    dao.apply_sepia_effect(image_metadata.filepath)
                elif selected_filter == "Sketch":
                    dao.apply_sketch_effect(image_metadata.filepath)
                elif selected_filter == "Invert":
                    dao.apply_invert_effect(image_metadata.filepath)

                dao.adjust_brightness(image_metadata.filepath, brightness_factor)
                dao.adjust_contrast(image_metadata.filepath, contrast_factor)

                dao.update_image_metadata(image_id, new_title, new_description, tags)
                st.success("Changes saved successfully!")
                edit_modal.close()
                st.experimental_rerun()
            
            # If the delete button is pressed, delete the image metadata and close the modal
            if delete_image:
                dao.delete_image_metadata(image_id)
                st.success("Image deleted successfully!")
                edit_modal.close()
                st.experimental_rerun()

            if restore_image:
                dao.restore_original(image_metadata.filepath)
                st.success("Image restored successfully!")
                edit_modal.close()
                st.experimental_rerun()

# Show or hide the edit form based on the session state
if 'edit_image_id' in st.session_state and st.session_state['edit_image_id'] is not None:
    display_edit_form(st.session_state['edit_image_id'])

# Iterate over the images and place them in the grid
for index, image_metadata in enumerate(images_metadata):
    # Calculate the row and column index
    row_idx, col_idx = divmod(index, num_columns)
    
    # Access the appropriate Streamlit container for the current image
    container = rows[row_idx][col_idx].container()
    
    # Display the image and its title
    container.image(image_metadata.filepath, use_column_width=True, caption=image_metadata.title)

    # Add an edit button for each image
    edit_button = container.button("Edit", key=f"edit-{image_metadata.id}")

    # If the edit button is clicked, open the modal and set the session state to show the edit form
    if edit_button:
        st.session_state['edit_image_id'] = image_metadata.id
        edit_modal.open()