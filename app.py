import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import requests

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ============================================================
# Function 1 - Search the web using SerpAPI
# ============================================================
def search_web(query):
    url = "https://serpapi.com/search"
    
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": 5
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    organic_results = data.get("organic_results", [])
    
    search_text = ""
    sources = []
    # sources is a NEW list we create to store links separately
    # we'll use this to show in the sidebar
    
    for i, result in enumerate(organic_results[:5]):
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        link = result.get("link", "")
        
        search_text += f"{i+1}. {title}\n{snippet}\nSource: {link}\n\n"
        
        sources.append({
            "title": title,
            "link": link
        })
        # we store each source as a dictionary with title and link
        # this makes it easy to display nicely in the sidebar
    
    return search_text, sources
    # now returning TWO things: the text AND the sources list

# ============================================================
# Function 2 - Get answer from Groq AI
# ============================================================
def get_answer(user_question, chat_history):
    # NEW: chat_history parameter added
    # this lets Jarvis remember previous messages
    
    search_text, sources = search_web(user_question)
    # get both search text and sources
    
    prompt = f"""You are JARVIS, a helpful and smart AI assistant.

The user asked: {user_question}

Here are the latest search results from the web:
{search_text}

Based on these search results, give a clear, accurate and helpful answer."""

    messages = [
        {
            "role": "system",
            "content": "You are JARVIS, a helpful AI assistant that answers questions based on web search results. Remember the conversation history and refer to it when relevant."
        }
    ]
    # start with system message giving Jarvis its personality
    
    for msg in chat_history[-6:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    # add last 6 messages from chat history
    # -6: means last 6 items in the list
    # this gives Jarvis memory of recent conversation
    # we limit to 6 to avoid sending too many tokens to the API
    
    messages.append({
        "role": "user",
        "content": prompt
    })
    # add current question as the last message
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        # now sending full conversation history!
        temperature=0.3,
        max_tokens=1024
    )
    
    answer = response.choices[0].message.content
    
    return answer, sources
    # return both answer AND sources for sidebar

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="Jarvis AI",
    page_icon="🤖",
    layout="wide"
    # layout="wide" gives us more space for sidebar
)

# ============================================================
# Sidebar - shows sources of last search
# ============================================================
with st.sidebar:
# everything inside this block appears in the left sidebar
    
    st.title("🔍 Jarvis")
    st.caption("AI Assistant with Live Web Search")
    
    st.divider()
    # draws a horizontal line
    
    st.subheader("📚 Sources")
    # this section shows sources from the last search
    
    if "last_sources" not in st.session_state:
        st.session_state.last_sources = []
    # initialize empty sources list on first load
    
    if st.session_state.last_sources:
        for i, source in enumerate(st.session_state.last_sources):
            st.markdown(f"**{i+1}. {source['title']}**")
            st.markdown(f"[Open link]({source['link']})")
            st.divider()
            # for each source show the title and a clickable link
    else:
        st.info("Sources will appear here after you ask a question")
        # show this message before any question is asked
    
    st.divider()
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.last_sources = []
        st.rerun()
    # clear chat button - resets everything
    # st.rerun() refreshes the page immediately

# ============================================================
# Main Chat Area
# ============================================================
st.title("🤖 Jarvis")
st.caption("Ask me anything — politics, sports, news, general knowledge")

if "messages" not in st.session_state:
    st.session_state.messages = []
# initialize empty chat history on first load

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# redraw all previous messages

if prompt := st.chat_input("Ask Jarvis anything..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Jarvis is searching the web..."):
            answer, sources = get_answer(
                prompt,
                st.session_state.messages
            )
            # pass full chat history to get_answer
            # so Jarvis has memory of conversation
            
            st.session_state.last_sources = sources
            # save sources to session_state
            # so sidebar can display them
        
        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })