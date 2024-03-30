import streamlit as st
import requests
st.title("Upload File to S3")

file = st.file_uploader("Choose a file")

if file:
    progress_bar = st.progress(0)
    st.write("File ready to Upload!")

    # Button to trigger file upload
    if st.button("Upload to S3"):
        # Send file to FastAPI endpoint
        files = {"file": (file.name, file.getvalue())}
        response = requests.post("http://backend:8000/upload", files=files, stream=True)

        if response.status_code == 200:
            st.success("File uploaded successfully to S3!")
        else:
            st.error("Failed to upload file. Error: {}".format(response.text))

        # total_size = int(response.headers.get('content-length', 0))

        # uploaded_size = 0
        # for chunk in response.iter_content(chunk_size=1024):
        #     uploaded_size += len(chunk)
        #     progress = uploaded_size / total_size
        #     progress_bar.progress(progress)
