import logging
from langchain_openai import OpenAI
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain.vectorstores import Chroma
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFacePipeline
from ragatouille import RAGPretrainedModel

query = "What happened to Mr. B?"
# READER_MODEL_NAME = "McGill-NLP/flan-t5-base-weblinx"
# EVALUATE_MODEL_NAME = "McGill-NLP/flan-t5-base-weblinx"
# RERANKER = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")

# model = AutoModelForCausalLM.from_pretrained(READER_MODEL_NAME)
# tokenizer = AutoTokenizer.from_pretrained(READER_MODEL_NAME)
# eval_model = AutoModelForCausalLM.from_pretrained(EVALUATE_MODEL_NAME)
# eval_tokenizer = AutoTokenizer.from_pretrained(EVALUATE_MODEL_NAME)
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

openai_llm = OpenAI(temperature=0)

# READER_LLM = pipeline(
#     model=model,
#     tokenizer=tokenizer,
#     task="text-generation",
#     do_sample=True,
#     temperature=0.2,
#     repetition_penalty=1.1,
#     return_full_text=False,
#     max_new_tokens=500,
# )
#
# EVAL_LLM = pipeline(
#     model=eval_model,
#     tokenizer=eval_tokenizer,
#     task="text-generation",
#     do_sample=True,
#     temperature=0.1,
#     repetition_penalty=1.1,
#     return_full_text=False,
#     max_new_tokens=500,
# )

# llm = HuggingFacePipeline(pipeline=READER_LLM)
# eval_llm = HuggingFacePipeline(pipeline=EVAL_LLM)

# RAG_PROMPT_TEMPLATE = tokenizer.apply_chat_template(
#     prompt_in_chat_format, tokenize=False, add_generation_prompt=True
# )


def retrieve_context(db, query):
    docs = db.similarity_search(query, k=10)

    retrieved_docs_text = [
        doc.page_content for doc in docs
    ]
    context = "\nExtracted documents:\n"
    context += "".join(
        [f"Document {i}:::\n{doc}" for i, doc in enumerate(retrieved_docs_text)]
    )
    return context


def generate_response(query, context):
    final_prompt = f"""
        "role": "system"\n
        content: Using the information contained in the context,
        give a comprehensive answer to the query.
        Respond only to the question asked, response should be concise and relevant to the question.
        Provide the number of the source document when relevant.
        If the answer cannot be deduced from the context, do not give an answer.
        "role": "user",
        "content": "Context:
        {context}
        ---
        Now here is the question you need to answer.
        
        Question: {query}
"""

    response = openai_llm(final_prompt)
    return response


def evaluate_response(query, context, response):
    evaluation_prompt = PromptTemplate(
        template="""You are a grader assessing the quality of the response given a user query and the context.\n
            Here is the context document: \n {context} \n
            Here is the user query: \n {query} \n
            Here is the generated response: \n {response} \n
            If the response does not include the key words from the question, the response is not good.\n
            If the response does not contain the reference of the context, the response is not good.\n
            Give a binary score 'yes' or 'no' score to indicate whether the response is relevant to the question. \n
            If the binary score is 'yes', provide the score as a text variable with a single key 'score'
            and no preamble or explanation.\n
            If the binary score is 'no', re-write the query in the way it helps to retrieve more revelent context.
            """,
        input_variables=["query", "question", "context"],
    )

    eval_response = eval_llm(evaluation_prompt)

    return eval_llm


def main(query: str):
    i = 0
    db = Chroma(
        persist_directory="chroma_db_sentence_trm",
        embedding_function=embedding_function,
    )
    context = retrieve_context(db, query)
    response = generate_response(query, context)

    return response

    # eval_response = evaluate_response(query, context, response)
    # if eval_response == "yes":
    #     return response
    # else:
    #     query = response
    #     i += 1
    #     while i < 3 & eval_response != "yes":
    #         context = retrieve_context(db, query)
    #         response = generate_response(query, context)
    #
    #         eval_response = evaluate_response(query, context, response)
    #
    #     return response


if __name__ == "__main__":
    response = main(query)
    print(response)
