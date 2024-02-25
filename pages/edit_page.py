import streamlit as st
from models import ImageMetadataDAO, ImageMetadataModel
from streamlit_modal import Modal

st.sidebar.page_link("pages/app.py", label="Scan", icon="📸")
st.sidebar.page_link("pages/edit_page.py", label="Edit", icon="📝")

# Initialize the Data Access Object
dao = ImageMetadataDAO()

# Fetch all image metadata from the database
images_metadata = dao.get_all_image_metadata()

# Set a title for the Streamlit app
st.title('Image Grid Display')

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
    Display the edit form in a modal for a specific image.

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

            # Submit button for the form
            submit_changes = st.button("Submit Changes", key=f"submit-{image_id}")

            # If the submit button is pressed, update the database and close the modal
            if submit_changes:
                try:
                    dao.update_image_metadata(image_id, new_title, new_description)
                    st.success("Changes saved successfully!")
                    edit_modal.close()
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error occurred while saving changes: {str(e)}")
                st.success("Changes saved successfully!")
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