import streamlit as st

def main():
    """
    Main function of the settings page
    Allows user to input their OpenAI API key for image description generation
    """
    st.title("Settings")
    st.subheader("OpenAI Services")
    st.caption("Please input your OpenAI API key to enable image description generation.")

    st.sidebar.page_link("pages/scan_page.py", label="Scan", icon="📸")
    st.sidebar.page_link("pages/edit_page.py", label="Edit", icon="📝")
    st.sidebar.page_link("pages/settings.py", label="Settings", icon="⚙️")
    
    api_key = st.text_input("OpenAI API Key", type="password")
    st.session_state['api_key'] = api_key

if __name__ == "__main__":
    main()