import requests
import streamlit as st

def get_api_response(question, session_id, model):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "query": question,
        "model": model
    }
    if session_id:
        data["session_id"] = session_id

    try:
        print(session_id, data)
        response = requests.post("http://localhost:8000/chat", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API request failed with status code {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def upload_document(file):
    files = {"file": (file.name, file, file.type)} 
    '''
        Here files is a dictionary in the format that requests expects:
        {field_name: (filename, fileobj, content_type)} field_name should be exactly same as per the argument of the FastAPI endpoint that is upload-doc
        field_name → "file" (must match the parameter name on backend: file: UploadFile).
        file.name → becomes the filename part of the multipart form.
        file → is the actual file object (stream).
        file.type → sets the MIME type (application/pdf, application/msword, etc.).
        When this POST request is sent, requests builds a multipart/form-data payload like this:
        Content-Disposition: form-data; name="file"; filename="mydoc.pdf"
        Content-Type: application/pdf
        (binary content here)
    '''
    response = requests.post("http://localhost:8000/upload-doc", files=files)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to upload document: {response.status_code} - {response.text}")
        return None

def list_documents():
    response = requests.get("http://localhost:8000/list-docs")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch documents: {response.status_code} - {response.text}")
        return []
    

def delete_document(file_id):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {"file_id": file_id}

    try:
        response = requests.post("http://localhost:8000/delete-doc", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to delete document. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while deleting the document: {str(e)}")
        return None