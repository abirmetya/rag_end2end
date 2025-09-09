import streamlit as st
import time
from api_utils import upload_document, list_documents, delete_document

def model_selection():
    st.sidebar.selectbox(
        "Select LLM Model",
        ("gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"),
        key="model"
    )
   
   # Sidebar: Upload Document
    st.sidebar.header("Upload Document")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx", "html"])

    if uploaded_file is not None:
        if st.sidebar.button("Upload"):
            with st.spinner("Uploading..."):
                # upload_response = time.sleep(7)
                # upload_response = dict({'file_id':'1234'})
                # print(upload_response)
                upload_response = upload_document(uploaded_file)
                # files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                # print(uploaded_file.filename)
                if upload_response:
                    st.sidebar.success(f"File '{uploaded_file.name}' uploaded successfully with ID {upload_response['file_id']}.")
                    st.session_state.documents = list_documents()  # Refresh the list after upload

    # Sidebar: List Documents
    st.sidebar.header("Uploaded Documents")
    if st.sidebar.button("Refresh Document List"):
        with st.spinner("Refreshing..."):
            st.session_state.documents = list_documents()

     # Initialize document list if not present
    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.text(f"{doc['filename']} (ID: {doc['id']}, Uploaded: {doc['upload_timestamp']})")
        
        # Delete Document
        selected_file_id = st.sidebar.selectbox("Select a document to delete", options=[doc['id'] for doc in documents], format_func=lambda x: next(doc['filename'] for doc in documents if doc['id'] == x))
        print(selected_file_id)
        if st.sidebar.button("Delete Selected Document"):
            with st.spinner("Deleting..."):
                delete_response = delete_document(selected_file_id)
                if delete_response:
                    st.sidebar.success(f"Document with ID {selected_file_id} deleted successfully.")
                    st.session_state.documents = list_documents()  # Refresh the list after deletion
                else:
                    st.sidebar.error(f"Failed to delete document with ID {selected_file_id}.")