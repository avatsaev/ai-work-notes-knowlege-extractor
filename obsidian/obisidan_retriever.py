from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import Milvus
from langchain.vectorstores import Milvus
from dotenv import load_dotenv
import os

load_dotenv()


def get_obsidian_retriever():
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_KEY"), model="text-embedding-ada-002")

    vector_db = Milvus(
        connection_args={"host": "localhost", "port": "19530"},
        embedding_function=embeddings,
        collection_name='flight_records',
        text_field='contents'
    )

    return vector_db.as_retriever(search_kwargs={"k": 10})



# if __name__ == "__main__":
#     retriever = get_obsidian_retriever()
#     res_docs = retriever.get_relevant_documents("https://doctolib.atlassian.net")
#     # res_docs
#
#     vector = inject_data_into_milvus()
#     print(vector)
#
#





