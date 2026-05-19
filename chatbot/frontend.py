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


    output=workflow.invoke({"messages":userinput},config=CONFIG)
    ai_response=output['messages'][-1].content
    st.session_state['message_history'].append({
        'role': 'assistant',
        'content': ai_response
    })
    with st.chat_message('assistant'):
       st.text(ai_response)
    