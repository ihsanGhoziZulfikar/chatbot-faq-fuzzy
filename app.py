import streamlit as st
from faqChatbot import get_faq_answer

# app title
st.title('Ask HR Chatbot')

# messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

# prompt input template
prompt = st.chat_input('input your prompt')

if prompt:
    st.chat_message('user').markdown(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    response = get_faq_answer(prompt)

    st.chat_message('assistant').markdown(response)
    
    st.session_state.messages.append(
        {'role': 'assistant', 'content': response}
    )