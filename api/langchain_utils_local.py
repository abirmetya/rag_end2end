from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from model_utils import select_llm
from chroma_utils import vectorstore
from dotenv import load_dotenv

load_dotenv()

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


## Rewrite and contexualized the User query
rewrite_prompt_context = """
You are given:
- A conversation history between a user and an assistant.
- The most recent user question, which may depend on or reference earlier context.

Your task:
- Reformulate the latest user question into a clear, standalone query that can be understood without seeing the prior chat.
- Preserve the user’s original intent and meaning.
- If the question is already self-contained, return it unchanged.
- Do not attempt to answer the question.
"""

contextualized_q_prompt = ChatPromptTemplate.from_messages([
    ('system',rewrite_prompt_context),
    MessagesPlaceholder("chat_history"),
    ('human',"{input}")
])

## Now using the above history_aware_retriever we now need to create an LLM chain. for that we can used stuffed document chain of LLM to stuff the whole content retrived to LLM.


qa_prompts = ChatPromptTemplate.from_messages([
    ("system", "You are helpful AI Assistant. Use the following context to answer the user's question."),
    ("system", "Context: {context}"),
     MessagesPlaceholder(variable_name="chat_history"),
     ("human", "{input}")
])

def get_rag_chain(model="gpt-4o-mini"):
    llm = select_llm(model= model)
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualized_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm,qa_prompts)  ## This will create a stuff document chain. That means stuff all the documents inside the context and then call LLM to genetrate the answer.
    rag_chain = create_retrieval_chain(history_aware_retriever,question_answer_chain) ## This will retrieved the documents after contextualized from the user query and then passed to stuff document chain and generate the answer.

    return rag_chain