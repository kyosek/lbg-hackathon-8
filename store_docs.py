from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Chroma


loader = CSVLoader("decisions_2023.csv", encoding="utf-8")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

db2 = Chroma.from_documents(docs, embeddings, persist_directory="./chroma_db")
