from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
import os

os.environ['OPENAI_API_KEY'] = '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'

def index_data(path):
    documents = SimpleDirectoryReader(path).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist()
    return index

def query_data(index, query):
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response