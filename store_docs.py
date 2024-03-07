from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import CharacterTextSplitter
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Chroma


loader = CSVLoader("decisions_2023.csv", encoding="utf-8")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=64)
docs = text_splitter.split_documents(documents)

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db_sentence_trm")
