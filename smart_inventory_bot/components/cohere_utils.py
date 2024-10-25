import cohere
from dotenv import load_dotenv
import os
load_dotenv()

cohere_api_key = os.getenv('COHERE_API_KEY')
co = cohere.Client(cohere_api_key)

def cohere_embed(
    text : str,
    model : str = "embed-english-v3.0",
    input_type : str = "search_document"
):

    response = co.embed(
        texts=[text], model=model, input_type=input_type
    )
    return response.embeddings[0]



def cohere_text_generation(
    query : str,
    model : str = "command-r-plus",
    temperature : float = 0.5,
):
        response = co.chat(
        model=model,
        message=query,
        temperature=temperature
        )

        return response.text


def cohere_rerank(
        query : str,
        docs : list[dict],
        model : str = "rerank-english-v3.0",
    ):
    
    documents = [str(doc['section_content']) for doc in docs]
    response = co.rerank(
        model=model,
        query=query,
        documents=documents,
        top_n=3,
    )

    new_docs = []
    for r in response.results:
        new_docs.append(docs[r.index])
    
    return new_docs

# x = cohere_embed("Hello")
# print(x)