import streamlit as st
import os
import time
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env if available
load_dotenv(find_dotenv(), override=True)

# Page configuration
st.set_page_config(
    page_title="Futuristic AI Workspace",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS Animations, Glassmorphism, Neon Glows & Dynamic UI Effects
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Space+Grotesk:wght@500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Dynamic Animated Cyberpunk Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #0b0f19, #111827, #1e1b4b, #0f172a, #030712);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #f3f4f6;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glowing Glassmorphism Header */
    .animated-header {
        position: relative;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        overflow: hidden;
        animation: floatHeader 4s ease-in-out infinite;
    }

    @keyframes floatHeader {
        0% { transform: translateY(0px); box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.2); }
        50% { transform: translateY(-8px); box-shadow: 0 16px 48px 0 rgba(168, 85, 247, 0.35); }
        100% { transform: translateY(0px); box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.2); }
    }

    /* Neon Shimmer Title Text */
    .gradient-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #60a5fa, #a855f7, #ec4899, #3b82f6);
        background-size: 200% auto;
        color: transparent;
        -webkit-background-clip: text;
        animation: shine 4s linear infinite;
        letter-spacing: -0.5px;
        margin: 0;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    .sub-title {
        color: #9ca3af;
        font-size: 1.05rem;
        margin-top: 8px;
        font-weight: 400;
        letter-spacing: 0.5px;
    }

    /* Animated Cyber Pulse Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #34d399;
        margin-top: 14px;
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10b981;
        animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Chat Messages Styling & Animated Slide-In */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 20px !important;
        padding: 1.2rem !important;
        margin-bottom: 1rem !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        animation: slideInMessage 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        transition: all 0.3s ease;
    }

    .stChatMessage:hover {
        transform: translateY(-2px) scale(1.005);
        border-color: rgba(168, 85, 247, 0.4) !important;
        box-shadow: 0 8px 30px rgba(168, 85, 247, 0.15);
    }

    @keyframes slideInMessage {
        from { opacity: 0; transform: translateY(20px) scale(0.97); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* Sidebar Custom Glassmorphism Styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Animated Avatar Pulse */
    .sidebar-avatar {
        display: block;
        margin: 0 auto 10px auto;
        border-radius: 50%;
        box-shadow: 0 0 25px rgba(168, 85, 247, 0.5);
        animation: avatarPulse 3s ease-in-out infinite;
    }

    @keyframes avatarPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(99, 102, 241, 0.4); }
        50% { transform: scale(1.05); box-shadow: 0 0 35px rgba(236, 72, 153, 0.7); }
    }

    /* Custom Input Controls & Glow Effects */
    .stTextInput input, .stTextArea textarea {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #f3f4f6 !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #a855f7 !important;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.4) !important;
    }

    /* Animated Buttons */
    .stButton button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3) !important;
    }

    .stButton button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(168, 85, 247, 0.6) !important;
    }

    /* Custom Animated Chat Input Bar */
    [data-testid="stChatInput"] {
        border-radius: 20px !important;
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header Component
st.markdown("""
    <div class="animated-header">
        <h1 class="gradient-text">⚡ NEURAL CORE AI</h1>
        <p class="sub-title">Next-Generation Animated Conversational Workspace</p>
        <div class="status-badge">
            <span class="pulse-dot"></span>
            <span>SYSTEM ONLINE & READY</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown("""
        <img src="https://cdn-icons-png.flaticon.com/512/8649/8649595.png" width="100" class="sidebar-avatar">
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #a855f7; font-weight: 700;'>CONTROL PANEL</h2>", unsafe_allow_html=True)
    st.divider()

    # API Key Input Block
    env_api_key = os.getenv("OPENAI_API_KEY")
    
    if not env_api_key:
        api_key_input = st.text_input(
            "🔑 OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Enter your API key here to unlock the assistant."
        )
    else:
        api_key_input = env_api_key
        st.success("API Key detected from Environment!", icon="🔒")

    st.divider()

    system_message = st.text_area(
        label="🤖 System Persona",
        value="You are an extraordinarily intelligent, futuristic, and helpful AI assistant.",
        height=90,
        key="system_role"
    )

    st.divider()

    if st.button("🚀 Clear & Reset Session", use_container_width=True):
        st.session_state.messages = []
        st.toast("Conversation reset successfully!", icon="✨")
        st.rerun()

# Verification Check
if not api_key_input:
    st.info("👈 Please enter your **OpenAI API Key** in the glowing sidebar panel to get started.", icon="⚡")
    st.stop()

# Model Initialization
try:
    chat = ChatOpenAI(model="gpt-4o", openai_api_key=api_key_input)
except Exception as e:
    st.error(f"Error initializing AI engine: {e}")
    st.stop()

# --- DISPLAY CHAT HISTORY WITH AVATARS ---
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="👤"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="⚡"):
            st.write(msg.content)

# --- USER CHAT INPUT ---
user_prompt = st.chat_input("Ask anything or give a command...")

if user_prompt:
    # Append user input
    st.session_state.messages.append(HumanMessage(content=user_prompt))

    with st.chat_message("user", avatar="👤"):
        st.write(user_prompt)

    # Format history for AI
    messages_for_ai = [SystemMessage(content=system_message)] + st.session_state.messages

    # Generate response with typing effect simulation
    with st.chat_message("assistant", avatar="⚡"):
        with st.spinner("Processing neural response..."):
            try:
                response = chat.invoke(messages_for_ai)
                ai_content = response.content
                
                # Dynamic Stream Text Effect
                placeholder = st.empty()
                full_text = ""
                for chunk in ai_content.split(" "):
                    full_text += chunk + " "
                    placeholder.markdown(full_text + "▌")
                    time.sleep(0.02)
                placeholder.markdown(full_text)

                st.session_state.messages.append(AIMessage(content=ai_content))

            except Exception as e:
                st.error(f"Execution Error: {e}")
