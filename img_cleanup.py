import os
from models import ImageMetadataDAO

# Initialize the Data Access Object
dao = ImageMetadataDAO()

# Fetch all image metadata from the database
image_metadata_list = dao.get_all_image_metadata()

# Extract the filepaths from the database entries
db_filepaths = {metadata.filepath for metadata in image_metadata_list}
# trim ./img from the filepaths
db_filepaths = {fp.replace('./img/', '') for fp in db_filepaths}

print(db_filepaths)

# Define the directory where images are stored
img_directory = './img'

# List all files in the img directory
img_files = {f for f in os.listdir(img_directory) if os.path.isfile(os.path.join(img_directory, f))}

print(img_files)

# Find the files that are not present in the database by comparing sets
files_to_delete = img_files - db_filepaths

print(files_to_delete)

# Delete the files that are not in the database
for file in files_to_delete:
    file_path = os.path.join(img_directory, file)
    print(f"Deleting file: {file_path}")
    os.remove(file_path)

print("Cleanup complete. Files not found in the database have been deleted.")