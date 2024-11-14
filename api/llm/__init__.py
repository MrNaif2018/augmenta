import json

from langchain import hub
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama  # noqa
from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # noqa
from langchain_text_splitters import RecursiveCharacterTextSplitter

from api.settings import settings

# llm = ChatOllama(model="llama3:8b")

API_KEY = settings.openai_api_key

llm = ChatOpenAI(model="gpt-4o-mini", api_key=API_KEY)


def prepare_data(data):
    if isinstance(data, Document):
        return data
    return f"JSON data: {json.dumps(data)}"


def llm_summary(name, results):
    documents = [
        Document(page_content=f"{prepare_data(result['data'])}", metadata={"source": result["source"]}) for result in results
    ]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(api_key=API_KEY))
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = {"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()

    return {
        "ai_short_summary": rag_chain.invoke(f"What is {name}? Describe in no less than 5 sentences."),
        "ai_long_summary": rag_chain.invoke(f"What is {name}? Describe in no less than 10 sentences."),
        "ai_competitor_summary": rag_chain.invoke(
            f"What are the competitors of {name}? Describe in no less than 5 sentences."
        ),
    }
