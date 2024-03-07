import logging
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain.vectorstores import Chroma

query = "What happened to Mr. B?"

if __name__ == "__main__":
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(
        persist_directory="chroma_db_sentence_trm",
        embedding_function=embedding_function,
    )
    docs = db.similarity_search(query)
    print(docs[0].page_content)
