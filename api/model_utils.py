from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

embed_model = SentenceTransformerEmbeddings(model_name = "all-MiniLM-L6-v2")

def select_llm(model = 'gpt-4o'):
    llm = ChatOpenAI(model=model)
    return llm