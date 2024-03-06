import pandas as pd
import os
import weaviate
import weaviate.classes as wvc

from langchain_community.vectorstores import Weaviate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import Chroma

WEAVIATE_URL = os.environ["WEAVIATE_URL"]

loader = CSVLoader("decisions_2023.csv", encoding="utf-8")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

# db = Weaviate.from_documents(docs, embeddings, weaviate_url=WEAVIATE_URL, by_text=False)
db2 = Chroma.from_documents(docs, embeddings, persist_directory="./chroma_db")


# client = weaviate.connect_to_wcs(
#     cluster_url=os.getenv("WCS_CLUSTER_URL"),
#     auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WCS_API_KEY")),
#     headers={
#         "X-OpenAI-Api-Key": os.environ["OPENAI_APIKEY"]
#     }
# )
#
# try:
#     # ===== define collection =====
#     questions = client.collections.create(
#         name="Question",
#         vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
#         generative_config=wvc.config.Configure.Generative.openai()
#     )
#
#     # ===== import data =====
#     resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
#     data = json.loads(resp.text)  # Load data
#
#     question_objs = list()
#     for i, d in enumerate(data):
#         question_objs.append({
#             "answer": d["Answer"],
#             "question": d["Question"],
#             "category": d["Category"],
#         })
#
#     questions = client.collections.get("Question")
#     questions.data.insert_many(question_objs)  # This uses batching under the hood
#
#
# finally:
#     client.close()  # Close client gracefully
