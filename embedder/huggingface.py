from langchain.embeddings import HuggingFaceEmbeddings


def hf_emeddings():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    return HuggingFaceEmbeddings(model_name=model_name)
