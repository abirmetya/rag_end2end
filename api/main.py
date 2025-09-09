from fastapi import FastAPI, UploadFile, File, HTTPException
from db_utils import get_all_documents, insert_document_records, delete_document_record, get_chat_history, insert_application_logs
from chroma_utils import ingestion_2_vectordb, delete_doc_from_chroma
# from langchain_utils import get_rag_chain
from langchain_utils_local import retriever,get_rag_chain
import os
import shutil
import uuid
from pydantic_models import UserQuery, ModelName, DeleteFileRequest, QueryResponse
import logging

logging.basicConfig(filemode='app.log',level=logging.INFO)

app = FastAPI()

@app.post('/chat', response_model=QueryResponse)
def chat(UserInput: UserQuery):
    session_id = UserInput.session_id
    # print("User Input Model:", UserInput.model)
    model = UserInput.model.value if isinstance(UserInput.model, ModelName) else UserInput.model
    user_question1 = UserInput.query
    logging.info(f"Session ID: {session_id}, Model: {model}, User Query: {user_question1}")

    if not session_id:
        session_id = str(uuid.uuid4())
    
    chat_history = get_chat_history(session_id)
    rag_chain = get_rag_chain(model=model)
    response = rag_chain.invoke({"input":user_question1, "chat_history": chat_history})['answer']
    insert_application_logs(session_id, user_question1, response, model)
    logging.info(f"Session ID: {session_id}, AI Response: {response}")
    # return response
    return QueryResponse(answer=response, session_id=session_id, model=UserInput.model)

@app.get('/list-docs')
def list_documents():
    return get_all_documents()

@app.post('/upload-doc')
def upload_and_index_document(file: UploadFile = File(..., description="Upload a .pdf, .docx, or .html file")):
    allowed_extensions = ['.pdf', '.docx', '.html']
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a .pdf, .docx, or .html file.")
    
    temp_file_path = f"temp_{file.filename}"

    try:
        # Save the uploaded file to a temporary file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_id = insert_document_records(file.filename)
        status_ = ingestion_2_vectordb(temp_file_path, file_id)

        if status_:
            return {"status": "success", "file_id": file_id, "filename": file.filename}
        else:
            delete_document_record(file_id)
            raise HTTPException(status_code=500, detail=f"Failed to index document.{file.filename}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
    
@app.post('/delete-doc')
def delete_document(doc_id: DeleteFileRequest):
    delete_status_db = delete_document_record(doc_id.file_id)
    if delete_status_db:
        delete_status_chroma = delete_doc_from_chroma(doc_id.file_id)
        if delete_status_chroma:
            return {"status": "success", "message": f"Document with id {doc_id.file_id} deleted successfully."}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to delete document with id {doc_id.file_id} from vector store.")
    else:
        raise HTTPException(status_code=500, detail=f"Failed to delete document with id {doc_id.file_id} from database.")