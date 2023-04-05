from langchain.embeddings.openai import OpenAIEmbeddings
from custom_milvus import Milvus
from custom_obsidian_loader import CustomObsidianLoader
from langchain.text_splitter import MarkdownTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

def inject_data_into_milvus(override=False):
    loader = CustomObsidianLoader('./avatsaev')
    docs = loader.load()
    markdown_splitter = MarkdownTextSplitter(chunk_size=1200, chunk_overlap=0)
    docs = markdown_splitter.split_documents(docs)

    # print(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_KEY"), model="text-embedding-ada-002")
    vector_db = Milvus.from_documents(
        docs,
        embeddings,
        connection_args={"host": "localhost", "port": "19530"},
        collection_name='flight_records',
        text_field='contents',
        override=override
    )
    print("Injection finished!")

    return vector_db

# if __name__ == "__main__":
#
#
#     vector = inject_data_into_milvus(override=True)
#     print(vector)
