import streamlit as st
import time
from faqChatbot import get_faq_answer

st.set_page_config(page_title="Ask HR Chatbot", page_icon="💬")
st.title("💬 Ask HR Chatbot")

topics = [
    "jatah cuti",
    "mekanisme cuti",
    "pelatihan kerja",
    "pajak gaji lembur",
    "BPJS & fasilitas kesehatan",
    "WFH dan fleksibilitas kerja",
    "penilaian kinerja",
    "pindah divisi",
    "perpanjangan kontrak",
    "PHK & pemberhentian kerja",
    "THR & bonus tahunan",
]

with st.expander("📚 Topik yang biasa ditanyakan"):
    st.markdown("Chatbot ini bisa membantu menjawab pertanyaan terkait topik-topik berikut:")
    st.markdown("\n".join([f"- {t}" for t in topics]))

# Setup state animasi
if 'anim_index' not in st.session_state:
    st.session_state.anim_index = 0
    st.session_state.last_update = time.time()

if time.time() - st.session_state.last_update > 0.5:
    st.session_state.anim_index += 1
    st.session_state.last_update = time.time()

animated_topic = topics[st.session_state.anim_index % len(topics)]

st.markdown(
    f"""
    <div style='font-size: 24px; font-weight: 500; margin-top: 10px;'>
        Selamat datang di FAQ HR Chatbot, tanyakan tentang 
        <span style='color: #FF4B4B; font-weight: 700;'>{animated_topic}</span>
    </div>
    """,
    unsafe_allow_html=True
)

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

prompt = st.chat_input("Ketik pertanyaan Anda...")

# Proses pertanyaan
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = get_faq_answer(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})