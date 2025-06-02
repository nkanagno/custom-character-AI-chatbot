import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI
from chromadb.utils import embedding_functions
from pydantic import BaseModel

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_key, model_name="text-embedding-3-small"
)

# chroma client
chroma_client = chromadb.PersistentClient(path="./data/chroma_persistent_storage")
collection_name = "document_qa_collection"
collection = chroma_client.get_or_create_collection(
    name=collection_name,embedding_function=openai_ef
)

client = OpenAI(api_key=openai_key)

def retrieve_documents(question, n_results=4):
    # query_embedding = get_openai_embedding(question)
    results = collection.query(query_texts=question, n_results=n_results)

    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]

    return relevant_chunks

def augmented_prompt(question, relevant_chunks,prompt):
    context = "\n\n".join(relevant_chunks)
    prompt = (
        prompt +
        "\n\nQuestion:\n" + question + "\n\n"
        "\n\nContext:\n" + context + "\n\n"
    )
    return prompt

def generate_response(question, relevant_chunks,prompt):

    prompt = augmented_prompt(question, relevant_chunks,prompt)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    answer = response.choices[0].message.content
    return answer


