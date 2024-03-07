import logging
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import CharacterTextSplitter
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Chroma

logging.basicConfig(format="%(process)d-%(levelname)s-%(message)s")


logging.info("Loading CSV file")
loader = CSVLoader("decisions_2023.csv", encoding="utf-8")
documents = loader.load()

logging.info("Initialise models")
text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=64)
docs = text_splitter.split_documents(documents)

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

logging.info("Storing document in the vector storage")
db = Chroma.from_documents(
    docs, embedding_function, persist_directory="./chroma_db_sentence_trm"
)
logging.info("Job complete")
