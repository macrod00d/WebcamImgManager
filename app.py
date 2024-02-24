import streamlit as st
import cv2
import os

def main():
    # Set Streamlit page configuration
    st.set_page_config(page_title="Web Cam Manager")
    st.title("Web Cam Manager")
    st.caption("Project 1 by Mishca de Costa")
    
    # Open the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Failed to open the webcam")
        return
    
    # Create a placeholder to display the webcam frame
    frame_placeholder = st.empty()
    
    # Create buttons for stopping and taking pictures
    stop_button_pressed = st.button("Stop")
    take_picture_button_pressed = st.button("Take Picture")
    
    # Initialize variables for picture counter and flag to track if a picture has been taken
    picture_counter = 1
    picture_taken = False
    
    # Start the webcam capture loop
    while cap.isOpened() and not stop_button_pressed:
        # Read the frame from the webcam
        ret, frame = cap.read()
        if not ret:
            st.write("Video Capture Ended")
            break
        
        # Convert the frame to RGB format for display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Display the frame in the placeholder
        frame_placeholder.image(frame, channels="RGB")
        
        # Check if the stop button or the q keyboard button is pressed
        if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
            break
        
        # Check if the take picture button is pressed and a picture has not been taken yet
        if take_picture_button_pressed and not picture_taken:
            # Define the picture path
            picture_path = f"./img/picture{picture_counter}.jpg"
            
            # Convert the frame back to BGR format for saving
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            try:
                # Save the picture
                cv2.imwrite(picture_path, frame_bgr)
                st.write(f"Picture saved: {picture_path}")
                
                # Increment the picture counter and set the flag to indicate a picture has been taken
                picture_counter += 1
                picture_taken = True
            except Exception as e:
                st.error(f"Failed to save picture: {e}")
    
    # Release the webcam and destroy any remaining windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()