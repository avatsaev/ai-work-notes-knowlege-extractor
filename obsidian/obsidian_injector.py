from obsidian.custom_milvus import Milvus
from obsidian.custom_obsidian_loader import CustomObsidianLoader
from langchain.text_splitter import MarkdownTextSplitter
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings

load_dotenv()

def inject_data_into_milvus(override=False):
    loader = CustomObsidianLoader('./avatsaev')
    docs = loader.load()
    markdown_splitter = MarkdownTextSplitter(chunk_size=1200, chunk_overlap=0)
    docs = markdown_splitter.split_documents(docs)

    # print(docs)

    embeddings = hf_emeddings()
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


def hf_emeddings():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    return HuggingFaceEmbeddings(model_name=model_name)

# if __name__ == "__main__":
#
#
#     vector = inject_data_into_milvus(override=True)
#     print(vector)
