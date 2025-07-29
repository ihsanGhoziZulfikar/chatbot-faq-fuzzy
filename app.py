import streamlit as st
from faqChatbot import get_faq_answer

st.set_page_config(page_title="FAQ HR Chatbot", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@700&display=swap');

    body {
        font-family: 'Lato', sans-serif;
    }

    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 25vh;
        margin-top: 1rem;
    }

    h1 {
        font-size: 2.5rem;
        color: #0f4c81;
        font-family: 'Lato', sans-serif;
        font-weight: 700;
        text-align: center;
    }

    .typewriter {
        --caret: #0f4c81;
    }

    .typewriter::before {
        content: "";
        animation: typing 6s infinite;
    }

    .typewriter::after {
        content: "";
        border-right: 2px solid var(--caret);
        animation: blink 0.5s step-end infinite;
        margin-left: 2px;
    }

    @keyframes typing {
        0%, 12.5%   { content: "Mekanisme Pengajuan Cuti"; }
        25%, 37.5%  { content: "Fasilitas Kesehatan"; }
        50%, 62.5%  { content: "Besaran THR"; }
        75%, 87.5%  { content: "Lembur dan Pajaknya"; }
        100%        { content: "Perpindahan Divisi"; }
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50%      { opacity: 0; }
    }

    div[data-baseweb="select"] > div {
        background-color: #f3f9ff;
        border: 1px solid #0f4c81;
        border-radius: 10px;
        padding: 10px;
    }

    .stSelectbox label {
        font-weight: bold;
        font-size: 1rem;
        color: #0f4c81;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="centered">
        <h1>Selamat datang di TanyaHR!<br>tanyakan tentang <span class="typewriter"></span></h1>
    </div>
    """,
    unsafe_allow_html=True
)

# === Dropdown Topik ===
st.markdown("### 🎯 Topik yang Bisa Ditanyakan")

with st.container():
    topic = st.selectbox(
        "Pilih salah satu topik di bawah:",
        (
            "Jatah Cuti",
            "Mekanisme Pengajuan Cuti",
            "Besaran THR",
            "Lembur dan Pajaknya",
            "Perpindahan Divisi",
            "Pelatihan dan Sertifikasi",
            "Kerja dari Rumah (WFH)",
            "Fasilitas Kesehatan",
            "Sisa Cuti",
        ),
        index=None,
        placeholder="Pilih topik pertanyaan HR...",
    )

    if topic:
        st.info(f"💡 Kamu memilih topik: **{topic}**. Silakan tanyakan pertanyaan spesifik yang berkaitan dengan menyertakan kata kunci sesuai dengan topik untuk mendapatkan jawaban yang maksimal.")

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Tanyakan pertanyaan HR kamu di sini...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    response = get_faq_answer(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({'role': 'assistant', 'content': response})