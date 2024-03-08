import streamlit as st 
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from get_answer import get_answer


def init_page() -> None:
    st.set_page_config(page_title="FOS Consumer Duty Chat Bot")
    st.header("FOS Consumer Duty Bot")
    st.sidebar.title("Options")


def init_messages() -> None:
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(
                content="you are a helpful AI assistant. Reply your answer in markdown format."
            )
        ]


def main() -> None:
    init_page()
    init_messages()
# lbg-square-logo.png
    with st.columns(3)[1]:
        st.image('../img/lbg-square-logo.png')
    
    # Define your suggestions
    suggestions = ["What is Consumer Duty?", "How can FOS data help with Consumer Duty?", "Give me a list of things you can help me with?"]

    # Add buttons for each suggestion
    for suggestion in suggestions:
        if st.button(suggestion):
            user_input = suggestion
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Bot is typing ..."):
                answer = get_answer(user_input)
                print(answer)
            st.session_state.messages.append(AIMessage(content=answer))

    # Add a select box to the sidebar
    # suggestion_input = st.sidebar.selectbox("Choose a suggestion", suggestions)
    # Add an input box
    user_input = st.chat_input("Input your question!")

    # Use the input from the suggestion box or the input box
    # user_input = suggestion_input if suggestion_input else text_input

    # if user_input or user_input := st.chat_input("Input your question!"):
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Bot is typing ..."):
            answer = get_answer(user_input)
            print(answer)
        st.session_state.messages.append(AIMessage(content=answer))

    messages = st.session_state.get("messages", [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)


if __name__ == "__main__":
    main()