import streamlit as st

st.sidebar.page_link("pages/scan_page.py", label="Scan", icon="📸")
st.sidebar.page_link("pages/edit_page.py", label="Edit", icon="📝")

# read reame.md file as a markdown string
with open('README.md', 'r') as f:
    readme = f.read()

st.markdown(body=readme)