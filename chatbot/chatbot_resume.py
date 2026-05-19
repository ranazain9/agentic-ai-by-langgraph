import streamlit as st
from back_end import workflow
import uuid
from langchain_core.messages import HumanMessage


def genrate_thread_id():
    return str(uuid.uuid4())


def chat_thread(thread_id):
    if thread_id not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread_id)


def reset():
    thread_id = genrate_thread_id()
    st.session_state['thread_id'] = thread_id
    chat_thread(thread_id)
    st.session_state['message_history'] = []


def load_conversation(thread_id):
    try:
        state = workflow.get_state(
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )
        return state.values.get('messages', [])
    except Exception as e:
        st.warning(f"Could not load conversation: {str(e)}")
        return []

def get_chat_name(messages):
    if messages and len(messages) > 0:
        first_msg = messages[0].content
        return first_msg[:40] + "..." if len(first_msg) > 40 else first_msg
    return "....."


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = genrate_thread_id()

if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread'] = []


chat_thread(st.session_state['thread_id'])

CONFIG = {
    "configurable": {
        "thread_id": st.session_state['thread_id']
    }
}


# Display old messages
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


# Sidebar
st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset()

st.sidebar.header("My Conversations")


for thread_id in st.session_state['chat_thread'][::-1]:
    messages = load_conversation(thread_id)
    chat_name = get_chat_name(messages)
    
    if st.sidebar.button(chat_name, key=thread_id):
        st.session_state['thread_id'] = thread_id
        temp_messages = []

        for msg in messages:

            if isinstance(msg, HumanMessage):
                role = "user"
            else:
                role = "assistant"

            temp_messages.append({
                "role": role,
                "content": msg.content
            })

        st.session_state['message_history'] = temp_messages


# User input
userinput = st.chat_input("Type here...")


if userinput:

    # Save user message
    st.session_state['message_history'].append({
        "role": "user",
        "content": userinput
    })

    # Show user message
    with st.chat_message("user"):
        st.markdown(userinput)

    # AI response
    with st.chat_message("assistant"):

        ai_response = st.write_stream(
            chunk.content
            for chunk, metadata in workflow.stream(
                {
                    "messages": [
                        HumanMessage(content=userinput)
                    ]
                },
                config=CONFIG,
                stream_mode="messages"
            )
            if chunk.content
        )

    # Save AI response
    st.session_state['message_history'].append({
        "role": "assistant",
        "content": ai_response
    })