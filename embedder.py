import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

def openai_embed(text):
    embedding = openai.Embedding.create(
        input=text, model="text-embedding-ada-002"
    )["data"][0]["embedding"]
    return embedding
