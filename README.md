# Webcam Image Manager
### Developed by Mishca de Costa for ENGM4620 Project #1 and 3

This is a simple webcam image capture application which implements a web UI to capture an image from a user's local machine.
Once the image has been captured, the user is prompted to input some metadata which then gets stored in an sqlite db

## Features
* Welcome page with documentation
* Scan page
    * Shows a live view of the default camera connected to the local machine
    * Allows the user to take a picture
    * Prompts user for a title and description
    * Saves metadata to sqlite db, and image to local folder
* Edit page
    * Shows all saved images
    * Provides an edit feature to edit the title or description, or delete the image
    * Allows user to select from 4 filters which apply image processing using the Python Image Library:
       * Greyscale
       * Sepia
       * Sketch (edge detection and thresholding to make a sketch like image from the source)
       * Invert (invert colours)
    * Allows the user to reset the image modifications to the original
    * AI Powered Image Describer - Uses GPT-4 Vision model to describe the image for the user

## How to Run 
Ensure you have python 3.10 other versions are not tested. Conda is reccomended as python version can be easily specified

### First create a virtual environment:
You can use either venv or anaconda, anaconda is reccomended. Do not use both, pick one. 
#### Using Venv:
```
python3 -m venv .webcamimg
.webcamimg\Scripts\activate.bat
pip install -r requirements.txt
```

#### Using Anaconda (reccomended):
```
conda create -n webcamimg python=3.10
conda activate webcamimg
pip install -r requirements.txt
```

### Next initialize the sqlite db
```
python dbinit.py
```

### Finally run the application, it should auto launch the browser to the UI
```
streamlit run main.py
```

### Cleanup
An img_cleanup.py script has been provided which will delete any images which do not exist in the db in case any extra images are generated during testing. 

## Goals
* Application implements OOP principles using a class for images
* SQLAlchemy is used as an ORM to leverage pythonic class notation
* Error handling is implemented to provide user details on why critical functions may have failed
* Input validation is applied in case user attempts to perform an illegal operation such as not filling out all metadata fields
* Streamlit is used for the UI to simplify interface development, future scope could include migration to Django/Flask
* Image processing features
* AI features
