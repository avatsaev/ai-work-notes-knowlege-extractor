# from langchain.vectorstores import Milvus
from embedder.huggingface import hf_emeddings
from obsidian.custom_milvus import Milvus
from dotenv import load_dotenv

load_dotenv()


def get_obsidian_retriever():

    vector_db = Milvus(
        connection_args={"host": "localhost", "port": "19530"},
        embedding_function=hf_emeddings(),
        collection_name='flight_records',
        text_field='contents'
    )

    return vector_db.as_retriever(search_kwargs={"k": 20})



# if __name__ == "__main__":
#     retriever = get_obsidian_retriever()
#     res_docs = retriever.get_relevant_documents("https://doctolib.atlassian.net")
#     # res_docs
#
#     vector = inject_data_into_milvus()
#     print(vector)
#






