"""Haive UI - Main Streamlit Application."""

import streamlit as st


def main():
    """Entry point for haive-ui CLI."""
    import subprocess
    import sys
    import os

    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path], check=True)


st.set_page_config(
    page_title="Haive AI",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state defaults
if "messages" not in st.session_state:
    st.session_state.messages = []
if "trace_log" not in st.session_state:
    st.session_state.trace_log = []
if "llm_config" not in st.session_state:
    st.session_state.llm_config = {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 2000,
    }

# Sidebar - Global LLM Config
with st.sidebar:
    st.title("Haive AI")
    st.caption("Agent Framework Dashboard")
    st.divider()

    # LLM Configuration
    st.subheader("LLM Configuration")
    provider = st.selectbox(
        "Provider",
        ["openai", "azure", "anthropic", "ollama"],
        index=0,
        key="provider_select",
    )
    if provider == "openai":
        models = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo", "o1-mini", "o1-preview"]
    elif provider == "azure":
        models = ["gpt-4o-mini", "gpt-4o", "gpt-4"]
    elif provider == "anthropic":
        models = ["claude-sonnet-4-6", "claude-haiku-4-5-20251001", "claude-opus-4-6"]
    else:
        models = ["llama3.1", "mistral", "codellama", "phi3"]

    model = st.selectbox("Model", models, key="model_select")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1, key="temp_slider")
    max_tokens = st.number_input("Max Tokens", 100, 16000, 2000, 100, key="max_tok")

    st.session_state.llm_config = {
        "provider": provider,
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    st.divider()
    st.subheader("System Prompt")
    system_prompt = st.text_area(
        "Custom system prompt (optional)",
        value=st.session_state.get("system_prompt", ""),
        height=100,
        key="sys_prompt",
        placeholder="You are a helpful assistant...",
    )
    st.session_state.system_prompt = system_prompt

    st.divider()

    # Navigation
    st.subheader("Navigation")
    page = st.radio(
        "Select Page",
        [
            "Home",
            "Agents",
            "Games",
            "Discovery & MCP",
            "Demos",
            "Status",
            "Trace Viewer",
        ],
        key="nav_radio",
    )

# Page routing
if page == "Home":
    from haive_ui.pages import home
    home.render()
elif page == "Agents":
    from haive_ui.pages import agents
    agents.render()
elif page == "Games":
    from haive_ui.pages import games
    games.render()
elif page == "Discovery & MCP":
    from haive_ui.pages import discovery
    discovery.render()
elif page == "Demos":
    from haive_ui.pages import demos
    demos.render()
elif page == "Status":
    from haive_ui.pages import status
    status.render()
elif page == "Trace Viewer":
    from haive_ui.pages import trace
    trace.render()
