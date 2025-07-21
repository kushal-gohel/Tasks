import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq
from agno.vectordb.chroma import ChromaDb
from agno.embedder.huggingface import HuggingfaceCustomEmbedder
import os
from dotenv import load_dotenv


# --- Page setup ---
st.set_page_config(
    page_title="Techify RAG Assistant",
    page_icon="🤖",
    layout="centered"
)

# --- Styles and branding ---
def set_custom_css():
    st.markdown("""
        <style>
            .main {background-color: #fcfcfc;}
            footer {visibility: hidden;}
            .stButton>button {
                background-color: #2254f4;
                color: white;
                font-weight: 600;
            }
            .stChatMessage.user {background: #eaf2ff;}
            .stChatMessage.assistant {background: #e7f7e7;}
            .stTextInput>div>input {
                font-size: 16px;
            }
        </style>
    """, unsafe_allow_html=True)

set_custom_css()

# --- Sidebar ---
st.sidebar.title("🚀 Techify AI RAG Assistant")
st.sidebar.info(
    "Ask questions about Techify Solutions' industry presence and services.\n\n"
    "**Powered by:**\n- Agno Agent Framework\n- Groq LLM\n- Chroma Vector DB"
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Supervisor Instructions**\n1. Type a question\n2. Response is always from the Techify knowledge base with cited sources."
)
st.sidebar.markdown("---")
import datetime
now = datetime.datetime.now().strftime("%A, %B %d, %Y, %I:%M %p")
st.sidebar.caption(f"Demo | Current date: {now}")

# --- Environment & Agent setup ---
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY_temp_2")
if not GROQ_API_KEY:
    st.error("❌ Missing GROQ_API_KEY_temp_2 in .env file")
    st.stop()

KB_PATH = "./chroma_techify"
COLLECTION_NAME = "techify_collection"

@st.cache_resource(show_spinner="🔄 Loading RAG agent...")
def get_agent_and_kb():
    # Embedding model (must match that used during chunking)
    embedder = HuggingfaceCustomEmbedder(id="sentence-transformers/all-MiniLM-L6-v2")

    # Vector store - based on your working code
    vectordb = ChromaDb(
        collection=COLLECTION_NAME,
        path=KB_PATH,
        persistent_client=True,
        embedder=embedder
    )

    # Minimal KB wrapper - exactly like your working code
    class ChromaKnowledgeBase:
        def __init__(self, vectordb):
            self.vectordb = vectordb
            self.name = "Techify Solutions KB"
            self.description = "Knowledge base scraped from Techify website pages."

        def query(self, query: str, filters=None, top_k: int = 4):
            return self.vectordb.search(query, top_k=top_k)

        def validate_filters(self, filters):
            # No filters currently used; pass-through
            return filters or {}, []

    kb = ChromaKnowledgeBase(vectordb)

    # Agent setup - using knowledge parameter like your working code
    agent = Agent(
        model=Groq(id="deepseek-r1-distill-llama-70b", api_key=GROQ_API_KEY),
        knowledge=kb,
        description="You are a domain expert on Techify Solutions' industries and services.",
        instructions=[
            "Only use the provided knowledge base to answer questions.",
            "If no relevant information is found, say you don't know.",
            "Cite source URLs from the metadata when applicable."
        ],
        markdown=True,
        show_tool_calls=False  # Set to False for cleaner UI
    )
    return agent, kb

agent, kb = get_agent_and_kb()

# --- UI Header ---
st.header("🤖 Techify Solutions AI RAG Assistant")
st.write("Ask questions about Techify's industries and services. All answers are strictly retrieved from Techify's website knowledge base, with source citations.")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# --- Core: Use agent with knowledge base directly (like your working CLI version) ---
def ask_agent_directly(user_query):
    """Use the agent directly with its knowledge base, similar to CLI version"""
    msg_placeholder = st.empty()
    full_answer = ""
    try:
        # Use agent.run() like your CLI version, but capture the response
        response_generator = agent.run(user_query, stream=True)
        for chunk in response_generator:
            text = ""
            if hasattr(chunk, 'content') and chunk.content is not None:
                text = str(chunk.content)
            elif isinstance(chunk, dict) and 'content' in chunk and chunk['content'] is not None:
                text = str(chunk['content'])
            elif isinstance(chunk, str):
                text = chunk
            elif chunk is not None:
                text = str(chunk)
            
            # Only add non-empty text
            if text:
                full_answer += text
                msg_placeholder.markdown(full_answer)
    except Exception as e:
        error_msg = f"❌ Error: {e}"
        msg_placeholder.markdown(error_msg)
        full_answer = error_msg
    return full_answer

# --- Alternative: Non-streaming approach (more reliable) ---
def ask_agent_non_streaming(user_query):
    """Non-streaming version for more reliability"""
    try:
        # Get response without streaming
        response = agent.run(user_query, stream=False)
        if hasattr(response, 'content') and response.content:
            return response.content
        elif isinstance(response, str):
            return response
        else:
            return str(response) if response else "No response received."
    except Exception as e:
        return f"❌ Error: {e}"

# --- Input form ---
with st.form(key="chat_form", clear_on_submit=True):
    user_question = st.text_input("Your question:", placeholder="e.g. What IT services does Techify offer for healthcare?", key="user_input")
    submit = st.form_submit_button("🟦 Ask")

# --- Show previous conversation ---
for qa in st.session_state["chat_history"]:
    with st.chat_message("user"):
        st.markdown(qa["question"])
    with st.chat_message("assistant"):
        st.markdown(qa["answer"])

if submit and user_question.strip():
    with st.chat_message("user"):
        st.markdown(user_question)
    with st.chat_message("assistant"):
        response = ask_agent_directly(user_question)
    st.session_state["chat_history"].append({
        "question": user_question,
        "answer": response
    })

st.markdown("---")
st.caption("© 2025 Techify Solutions | RAG Assistant powered by Agno · Groq · ChromaDB · Streamlit")