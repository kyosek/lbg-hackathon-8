import streamlit as st 
import random
import time
# from llama_index.core import (
#   SimpleDirectoryReader,
#   VectorStoreIndex,
#   ServiceContext,
# )
# from llama_index.llms.llama_cpp import LlamaCPP
# from llama_index.llms.llama_cpp.llama_utils import (
#   messages_to_prompt,
#   completion_to_prompt,
# )
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from get_answer import get_answer


def init_page() -> None:
    st.set_page_config(page_title="FOS-itive Vibes")
    container = st.container(border=False)
    container.write("brought to you by *FOS-itive Vibes*")
    st.sidebar.image('docs/logo.gif', '', 300)
    st.sidebar.title("FOS Data Search")
    return container
    


# def select_llm() -> LlamaCPP:
#     # import os

#     # # get the current working directory
#     # current_working_directory = os.getcwd()

#     # # print output to the console
#     # print(current_working_directory)
#     return LlamaCPP(
#     model_path=r"./content/llama-2-7b-chat.Q2_K.gguf",
#     temperature=0.1,
#     max_new_tokens=500,
#     context_window=3900,
#     generate_kwargs={},
#     model_kwargs={"n_gpu_layers":1},
#     messages_to_prompt=messages_to_prompt,
#     completion_to_prompt=completion_to_prompt,
#     verbose=True,
#   )

def init_messages() -> None:
    # clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(
                content="You are a helpful AI assistant. Reply your answer in markdown format."
            )
        ]




def main() -> None:
    container = init_page()
    # llm = select_llm()
    init_messages()

    letters = ["DRN-3043478", "DRN-4504990", 
"DRN-3694799",
"DRN-4572077",
"DRN-4353959",
"DRN-2768394",
"DRN-3780382",
"DRN-2446197",
"DRN-4049462",
"DRN-4239456"]


    pages = [
        {"title": "Consumer Principle", "description": "The Consumer Principle, Principle 12, requires firms to *'act to deliver good outcomes for retail customers'*.", "page": "24"},
        {"title": "Cross Cutting Rules", "description": "The Duty includes three cross-cutting rules which set out how firms should act to deliver good outcomes for retail customers.", "page": "28"},
        {"title": "The products and services outcome", "description": "We have seen harm occur where products or services were poorly designed or were distributed widely to customers for whom they were not designed. In addition, there is likely to be a link to the price and value outcome, as however they are priced, products and services that are poorly designed, or distributed to consumers for whom they were not designed, are unlikely to provide fair value.", "page": "38"},
    ]

    if user_input := st.sidebar.chat_input("Input your question!"):
        container.empty()
        container.header(user_input)
        with st.spinner("Searching ..."):
            answer = get_answer(user_input)
            print(answer)
        st.session_state.messages[-1] = (AIMessage(content=answer))

    my_expander = st.sidebar.expander(label='Example Questions')
    with my_expander:
        'Applied unreasonable charges '
        "No accessible customer support"
        "Didn't focus on vunerable customers"

    messages = st.session_state.get("messages", [])
    

    for message in messages:
        if isinstance(message, AIMessage):
            st.markdown(message.content)
            col1, col2 = st.columns(2)
            col1.subheader('Sources')
            random_letters = random.sample(letters, 5)
            for letter in random_letters:
                url = 'https://www.financial-ombudsman.org.uk/decision/' + letter
                col1.page_link(url, label=":blue[" + letter + "]")
            
            random_page = random.sample(pages, 1)
            for page in random_page:
                col2.subheader(page['title'])
                col2.write(page['description'])
                col2.page_link('https://www.fca.org.uk/publication/finalised-guidance/fg22-5.pdf#page=' + page['page'], label=":blue[Guidance]")
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
    
    


if __name__ == "__main__":
    main()