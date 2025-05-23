import chromadb
from chromadb.config import Settings
import openai
from openai.embeddings_utils import get_embedding
import uuid
import os
import ast

openai.api_key = os.getenv("OPENAI_API_KEY")

client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="chroma_db"))
collection = client.get_or_create_collection("support_knowledge")

def process_text_and_store(text):
    prompt = f"""
    Extract structured FAQ-style data from the following text and return as a list of dictionaries:
    [{{'question': '...', 'answer': '...'}}, ...]
    Text:
    """
    prompt += text

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    structured_data = ast.literal_eval(response.choices[0].message.content.strip())

    for qa in structured_data:
        doc = qa['question'] + ' ' + qa['answer']
        emb = get_embedding(doc, engine="text-embedding-ada-002")
        collection.add(
            documents=[doc],
            embeddings=[emb],
            ids=[str(uuid.uuid4())]
        )
    client.persist()
