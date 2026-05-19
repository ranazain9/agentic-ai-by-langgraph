import streamlit as st
from back_end import workflow


CONFIG={"configurable":{"thread_id":'thread_1'}}
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Show old messages
for message in st.session_state['message_history']:

    with st.chat_message(message['role']):
        st.text(message['content'])


# User input
userinput = st.chat_input(placeholder='Type here')

if userinput:

    # Save user message
    st.session_state['message_history'].append({'role': 'user',         'content':userinput})
    # Display user message
    with st.chat_message('user'):
        st.text(userinput)


    with st.chat_message('assistant'):
        ai_response = st.write_stream(
        message_chunk.content for message_chunk, metadata in workflow.stream({
        'messages':userinput},
        config= {"configurable":{"thread_id":'thread_1'}},
        stream_mode='messages'
        ))

    st.session_state['message_history'].append({
        'role': 'assistant',
        'content': ai_response
    })

