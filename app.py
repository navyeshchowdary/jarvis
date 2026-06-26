import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime
import time
import base64
from PIL import Image
import io
from fpdf import FPDF
import uuid

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(
    page_title="Jarvis AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@400;700&display=swap');

.stApp {
    background: #000000;
    font-family: 'Inter', sans-serif;
    background-image: radial-gradient(ellipse at top center, #1c0500 0%, #000000 65%);
}

[data-testid="stSidebar"] {
    background: #000000 !important;
    border-right: 1px solid #1a1a1a !important;
}

[data-testid="stSidebarNav"] {
    display: none !important;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

.jarvis-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(180deg, #ff6600 0%, #cc3300 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 6px;
    margin: 0;
    padding: 0;
}

.jarvis-sub {
    text-align: center;
    color: #663300 !important;
    font-size: 11px;
    letter-spacing: 4px;
    margin-top: 6px;
    font-weight: 400;
    text-transform: uppercase;
}

.welcome-title {
    text-align: center;
    color: #ff5500 !important;
    font-size: 22px;
    font-weight: 600;
    margin-top: 40px;
    margin-bottom: 8px;
}

.welcome-sub {
    text-align: center;
    color: #442200 !important;
    font-size: 14px;
    margin-bottom: 20px;
}

[data-testid="stChatMessage"] {
    background: rgba(255, 60, 0, 0.03) !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 14px !important;
    margin: 6px 0 !important;
    animation: slideIn 0.3s ease;
    padding: 4px 8px !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: rgba(255, 69, 0, 0.06) !important;
    border: 1px solid rgba(255, 69, 0, 0.2) !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #000000 !important;
    border: 1px solid #1a1a1a !important;
}

[data-testid="stChatMessage"] p {
    color: #e8d5c8 !important;
    line-height: 1.75 !important;
    font-size: 15px !important;
}

[data-testid="stChatInput"] {
    background: #111111 !important;
    border: none !important;
    border-radius: 0 !important;
    color: #e8d5c8 !important;
    font-size: 15px !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: none !important;
}

[data-testid="stChatInputContainer"] {
    background: #111111 !important;
    border: 1px solid rgba(255,69,0,0.4) !important;
    border-radius: 14px !important;
    box-shadow: none !important;
    padding: 4px 8px !important;
}

[data-testid="stChatInputContainer"]:focus-within {
    border-color: rgba(255,69,0,0.7) !important;
}

[data-testid="stChatInputContainer"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #ff4500 !important;
}

[data-testid="stBottom"] {
    background: #000000 !important;
    padding: 8px 0 16px !important;
    border: none !important;
}

[data-testid="stBottom"] > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 20px !important;
}

section[data-testid="stBottom"] > div > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

div:has(> [data-testid="stChatInput"]) {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.stButton > button {
    background: #000000 !important;
    color: #ff5500 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all 0.25s ease !important;
}

.stButton > button:hover {
    background: rgba(255,69,0,0.08) !important;
    border-color: rgba(255,69,0,0.4) !important;
    color: #ff6600 !important;
    transform: translateY(-1px) !important;
}

.stDownloadButton > button {
    background: #000000 !important;
    color: #ff5500 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
}

.stDownloadButton > button:hover {
    background: rgba(255,69,0,0.08) !important;
    border-color: rgba(255,69,0,0.4) !important;
    color: #ff6600 !important;
    transform: translateY(-1px) !important;
}

.history-card {
    background: #000000;
    border: 1px solid #1a1a1a;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 5px 0;
    transition: all 0.25s ease;
}

.history-card:hover {
    background: rgba(255,69,0,0.05);
    border-color: rgba(255,69,0,0.25);
}

.analysis-box {
    background: #0d0d0d;
    border: 1px solid #1a1a1a;
    border-left: 3px solid #ff4500;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 10px 0;
}

.upload-section {
    background: #0a0a0a;
    border: 1px solid rgba(255,69,0,0.2);
    border-radius: 14px;
    padding: 16px 20px;
    margin: 10px 0 16px;
}

/* Mobile styles */
@media (max-width: 768px) {
    .jarvis-title {
        font-size: 1.8rem !important;
        letter-spacing: 3px !important;
    }
    .jarvis-sub {
        font-size: 9px !important;
        letter-spacing: 2px !important;
    }
    .welcome-title {
        font-size: 18px !important;
    }
    [data-testid="stChatMessage"] p {
        font-size: 14px !important;
    }
}

hr { border-color: #1a1a1a !important; }
p, span, label { color: #c8a898 !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #000000; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #ff4500; }
.stSpinner > div { border-top-color: #ff4500 !important; }
.stAlert {
    background: rgba(255,69,0,0.05) !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 10px !important;
}
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Device ID
# ============================================================
def get_device_id():
    if "device_id" not in st.session_state:
        st.session_state.device_id = str(uuid.uuid4())
    return st.session_state.device_id

# ============================================================
# History functions
# ============================================================
HISTORY_FILE = "chat_history.json"

def load_all_sessions():
    device_id = get_device_id()
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            all_data = json.load(f)
            return all_data.get(device_id, {})
    return {}

def save_session(session_id, messages, title):
    device_id = get_device_id()
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            all_data = json.load(f)
    else:
        all_data = {}
    if device_id not in all_data:
        all_data[device_id] = {}
    all_data[device_id][session_id] = {
        "title": title,
        "messages": messages,
        "timestamp": datetime.now().strftime("%d %b, %I:%M %p")
    }
    with open(HISTORY_FILE, "w") as f:
        json.dump(all_data, f, indent=2)

def delete_session(session_id):
    device_id = get_device_id()
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            all_data = json.load(f)
        if device_id in all_data and session_id in all_data[device_id]:
            del all_data[device_id][session_id]
            with open(HISTORY_FILE, "w") as f:
                json.dump(all_data, f, indent=2)

def load_session(session_id):
    device_id = get_device_id()
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            all_data = json.load(f)
            device_data = all_data.get(device_id, {})
            return device_data.get(session_id, None)
    return None

# ============================================================
# PDF Export
# ============================================================
def export_chat_as_pdf(messages, title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(255, 80, 0)
    pdf.cell(0, 12, "JARVIS - Chat Export", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 8,
        f"Exported on {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
        ln=True, align="C")
    pdf.ln(6)
    pdf.set_draw_color(255, 69, 0)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    for message in messages:
        if message["role"] == "user":
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(255, 100, 0)
            pdf.cell(0, 8, "You:", ln=True)
        else:
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(50, 100, 255)
            pdf.cell(0, 8, "Jarvis:", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 40, 40)
        content = message["content"]
        content = content.replace("**", "").replace("*", "").replace("#", "")
        content = content.encode("latin-1", errors="replace").decode("latin-1")
        pdf.multi_cell(0, 7, content)
        pdf.ln(4)
    return bytes(pdf.output())

# ============================================================
# Web search
# ============================================================
def search_web(query):
    url = "https://serpapi.com/search"
    params = {"engine": "google", "q": query, "api_key": SERPAPI_KEY, "num": 5}
    response = requests.get(url, params=params)
    data = response.json()
    organic_results = data.get("organic_results", [])
    search_text = ""
    for i, result in enumerate(organic_results[:5]):
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        link = result.get("link", "")
        search_text += f"{i+1}. {title}\n{snippet}\nSource: {link}\n\n"
    return search_text

# ============================================================
# Image analysis
# ============================================================
def analyze_image(image_file):
    image = Image.open(image_file)
    if image.mode != "RGB":
        image = image.convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Analyze this image carefully. Identify who or what is in it. If people are present, try to identify them by name. Provide detailed information about them including profession, achievements and interesting facts. If unsure about identity, describe what you see honestly."
                    }
                ]
            }
        ],
        max_tokens=1024
    )
    return response.choices[0].message.content

# ============================================================
# Smart search detection
# ============================================================
def needs_web_search(question):
    no_search = [
        "hello", "hi", "hey", "how are you", "who are you",
        "thanks", "thank you", "bye", "ok", "okay", "joke"
    ]
    q = question.lower().strip()
    if len(q.split()) <= 2:
        return False
    for keyword in no_search:
        if keyword in q:
            return False
    return True

# ============================================================
# Get answer with streaming
# ============================================================
def get_answer(user_question, chat_history):
    if needs_web_search(user_question):
        search_text = search_web(user_question)
        search_context = f"\nWeb search results:\n{search_text}"
    else:
        search_context = ""
    messages = [
        {
            "role": "system",
            "content": "You are JARVIS, an intelligent AI assistant. For greetings respond naturally. For factual questions use web search results. Always use conversation history for follow-up questions. Give clear well structured answers."
        }
    ]
    for msg in chat_history:
        if msg["role"] in ["user", "assistant"]:
            messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({
        "role": "user",
        "content": f"Question: {user_question}{search_context}"
    })
    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.3,
        max_tokens=1024,
        stream=True
    )
    return stream

# ============================================================
# Session state
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
if "session_title" not in st.session_state:
    st.session_state.session_title = "New Chat"
if "show_upload" not in st.session_state:
    st.session_state.show_upload = False

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 12px'>
        <div style='font-family:Orbitron,monospace;font-size:18px;
        font-weight:700;color:#ff5500;letter-spacing:5px'>⬡ JARVIS</div>
        <div style='font-size:10px;color:#442200;letter-spacing:3px;
        margin-top:5px'>AI · WEB SEARCH · VISION</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    if st.button("＋  New Chat", use_container_width=True):
        if st.session_state.messages:
            save_session(
                st.session_state.session_id,
                st.session_state.messages,
                st.session_state.session_title
            )
        st.session_state.messages = []
        st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state.session_title = "New Chat"
        st.session_state.show_upload = False
        st.rerun()

    if st.button("📷  Analyze Image", use_container_width=True):
        st.session_state.show_upload = not st.session_state.show_upload
        st.rerun()

    if st.session_state.messages:
        pdf_bytes = export_chat_as_pdf(
            st.session_state.messages,
            st.session_state.session_title
        )
        st.download_button(
            label="📄  Export as PDF",
            data=pdf_bytes,
            file_name=f"jarvis_{datetime.now().strftime('%d%m%Y_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.divider()

    st.markdown("""
    <div style='font-size:11px;color:#663300;letter-spacing:3px;
    font-weight:600;margin-bottom:10px;text-transform:uppercase'>
    Recent Chats</div>
    """, unsafe_allow_html=True)

    all_sessions = load_all_sessions()
    if all_sessions:
        sorted_sessions = sorted(
            all_sessions.items(),
            key=lambda x: x[0],
            reverse=True
        )
        for session_id, session_data in sorted_sessions[:10]:
            col1, col2 = st.columns([5, 1])
            with col1:
                title = session_data['title'][:28]
                timestamp = session_data['timestamp']
                if st.button(
                    f"▶ {title}...\n{timestamp}",
                    key=f"load_{session_id}",
                    use_container_width=True
                ):
                    if st.session_state.messages:
                        save_session(
                            st.session_state.session_id,
                            st.session_state.messages,
                            st.session_state.session_title
                        )
                    loaded = load_session(session_id)
                    if loaded:
                        st.session_state.messages = loaded["messages"]
                        st.session_state.session_title = loaded["title"]
                        st.session_state.session_id = session_id
                        st.rerun()
            with col2:
                if st.button("✕", key=f"del_{session_id}"):
                    delete_session(session_id)
                    st.rerun()
    else:
        st.markdown("""
        <p style='color:#2a1000;font-size:12px;
        font-style:italic;text-align:center;margin-top:20px'>
        No conversations yet</p>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <p style='color:#2a1000;font-size:11px;text-align:center'>
    📱 On mobile? Tap ☰ top left to open this menu
    </p>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN AREA
# ============================================================
st.markdown("""
<div style='padding:40px 0 0'>
    <div class='jarvis-title'>J.A.R.V.I.S</div>
    <div class='jarvis-sub'>Just A Rather Very Intelligent System</div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.messages and not st.session_state.show_upload:
    st.markdown("""
    <div class='welcome-title'>How can I help you today?</div>
    <div class='welcome-sub'>
    Ask me anything — tap ☰ top left on mobile to access all features
    </div>
    """, unsafe_allow_html=True)

if st.session_state.show_upload:
    st.markdown("""
    <div class='upload-section'>
        <div style='color:#ff5500;font-size:13px;font-weight:600;
        letter-spacing:1px;margin-bottom:12px'>
        📷 Upload an image — Jarvis will identify it
        </div>
    </div>
    """, unsafe_allow_html=True)
    uploaded_image = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png", "webp"],
        key="image_uploader"
    )
    if uploaded_image is not None:
        img_bytes = uploaded_image.read()
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(img_bytes, use_container_width=True)
        with col2:
            with st.spinner("🔍 Jarvis is analyzing..."):
                analysis = analyze_image(io.BytesIO(img_bytes))
            st.markdown(f"""
            <div class='analysis-box'>
                <div style='color:#ff5500;font-size:11px;
                font-weight:600;letter-spacing:2px;margin-bottom:10px'>
                ⬡ JARVIS VISION ANALYSIS</div>
                <div style='color:#e8d5c8;font-size:14px;line-height:1.75'>
                {analysis}</div>
            </div>
            """, unsafe_allow_html=True)
    if st.button("✕ Close Image Upload"):
        st.session_state.show_upload = False
        st.rerun()
    st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message Jarvis..."):
    if st.session_state.session_title == "New Chat":
        st.session_state.session_title = prompt
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    })
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        spinner_text = "Searching the web..." if needs_web_search(prompt) else "Thinking..."
        with st.spinner(spinner_text):
            stream = get_answer(prompt, st.session_state.messages[:-1])
        answer = ""
        placeholder = st.empty()
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                answer += chunk.choices[0].delta.content
                placeholder.markdown(answer + "▋", unsafe_allow_html=True)
        placeholder.markdown(answer)
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    })
    save_session(
        st.session_state.session_id,
        st.session_state.messages,
        st.session_state.session_title
    )