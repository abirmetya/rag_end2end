from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredHTMLLoader
from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from model_utils import embed_model

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200,
    length_function=len
)
vectorstore = Chroma(persist_directory='./chroma_db', embedding_function=embed_model)

# def load_documents(folder_path: str) -> List[Document]:
#     ## Loading for multiple documents ##
#     documents = []
#     for filename in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, filename)
#         if filename.endswith('.pdf'):
#             loader = PyPDFLoader(file_path)
#         elif filename.endswith('.docx'):
#             loader = Docx2txtLoader(file_path)
#         else:
#             print(f"Unsupportd file type: {file_path}")
#         documents.extend(loader.load())

#     return documents

def load_documents(filename: str) -> List[Document]:
    ## Loading for single document and split it Recursively ##       
    if filename.endswith('.pdf'):
        loader = PyPDFLoader(filename)
    elif filename.endswith('.docx'):
        loader = Docx2txtLoader(filename)
    elif filename.endswith('.html'):
        loader = UnstructuredHTMLLoader(filename)
    else:
        raise ValueError(f"Unsupportd file type: {filename}")
    
    documents = loader.load()

    return text_splitter.split_documents(documents)

def ingestion_2_vectordb(filename: str, file_id: int) -> bool :
    try:
        splits = load_documents(filename)
        ## Add meta data to each chunks
        for split in splits:
            split.metadata['file_id'] = file_id
        
        vectorstore.add_documents(splits)
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False
    
def delete_doc_from_chroma(file_id: int):
    try:
        docs = vectorstore.get(where={"file_id": file_id})
        print(f"Found {len(docs['ids'])} document chunks for file_id {file_id}")
        
        vectorstore._collection.delete(where={"file_id": file_id})
        print(f"Deleted all documents with file_id {file_id}")
        
        return True
    except Exception as e:
        print(f"Error deleting document with file_id {file_id} from Chroma: {str(e)}")
        return False






