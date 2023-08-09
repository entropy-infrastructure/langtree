import chromadb
import chromadb.config
from langtree.models.openai import OpenAIEmbedding

def chroma_db_example():
    client = chromadb.PersistentClient(path=".")

    emb_fn = OpenAIEmbedding(model="text-embedding-ada-002")

    collection = client.create_collection(name="my_collection", embedding_function=emb_fn, get_or_create=True)

    collection.add(
        documents=["lorem ipsum...", "doc2", "doc3"],
        metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}],
        ids=["id1", "id2", "id3"]
    )

    res = collection.query(
        query_texts=["doc10", "thus spake zarathustra"],
        n_results=10,
        where={"chapter": "3"},
        where_document={"$contains": "doc"}
    )

    print(res)

if __name__ == "__main__":
    chroma_db_example()