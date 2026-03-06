"""Agents page - browse, configure, and run agents."""

import asyncio
import time
import traceback

import streamlit as st

from haive_ui.utils.registry import (
    AGENT_REGISTRY,
    AgentInfo,
    get_agents_by_category,
    get_class_docstring,
    try_import,
)
from haive_ui.utils.tracer import TraceCollector


def render():
    st.title("Agents")

    # Initialize tracer
    if "tracer" not in st.session_state:
        st.session_state.tracer = TraceCollector()

    # Category filter
    categories = list(get_agents_by_category().keys())
    selected_cats = st.multiselect(
        "Filter by category",
        categories,
        default=categories,
        key="agent_cat_filter",
    )

    # Search
    search = st.text_input("Search agents", "", key="agent_search")

    # Filter agents
    filtered = [
        a for a in AGENT_REGISTRY
        if a.category in selected_cats
        and (not search or search.lower() in a.name.lower() or search.lower() in a.description.lower())
    ]

    st.caption(f"Showing {len(filtered)}/{len(AGENT_REGISTRY)} agents")

    # Agent cards
    for agent_info in filtered:
        _render_agent_card(agent_info)


def _render_agent_card(info: AgentInfo):
    """Render a single agent card with info and run capability."""
    with st.expander(f"**{info.name}** — {info.category}", expanded=False):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"**{info.description}**")

            # Get docstring
            docstring = get_class_docstring(info.module_path, info.class_name)
            if docstring:
                st.caption(docstring[:300])

            st.code(f"from {info.module_path} import {info.class_name}", language="python")

            if info.tags:
                st.markdown(" ".join(f"`{t}`" for t in info.tags))

        with col2:
            # Import status
            cls, err = try_import(info.module_path, info.class_name)
            if cls:
                st.success("Import OK")
            else:
                st.error(f"Import failed: {err}")
                return

            # Instantiation test
            if st.button("Test Instantiate", key=f"inst_{info.name}"):
                _test_instantiate(info, cls)

            # Run agent
            if not info.requires_docs and not info.requires_tools:
                query = st.text_input("Query", key=f"query_{info.name}", placeholder="Ask something...")
                if st.button("Run", key=f"run_{info.name}") and query:
                    _run_agent(info, cls, query)


def _test_instantiate(info: AgentInfo, cls):
    """Test instantiating an agent."""
    try:
        if info.factory_method == "from_documents":
            from langchain_core.documents import Document
            docs = [
                Document(page_content="Python is a programming language."),
                Document(page_content="Machine learning uses algorithms to learn from data."),
                Document(page_content="Neural networks are inspired by the brain."),
            ]
            obj = getattr(cls, info.factory_method)(documents=docs, name=f"test_{info.name}")
        else:
            obj = cls(name=f"test_{info.name}")
        st.success(f"Instantiated: {type(obj).__name__}")
    except Exception as e:
        st.error(f"Failed: {e}")


def _run_agent(info: AgentInfo, cls, query: str):
    """Run an agent with the given query."""
    tracer: TraceCollector = st.session_state.tracer

    try:
        from haive_ui.utils.llm_factory import make_llm_config

        config = st.session_state.llm_config.copy()
        config["system_prompt"] = st.session_state.get("system_prompt", "")

        trace = tracer.start_trace(f"{info.name}: {query[:50]}")
        tracer.log("input", info.name, query)

        with st.spinner(f"Running {info.name}..."):
            start = time.time()

            # Create agent with LLM config
            engine = make_llm_config(config)
            agent = cls(name=f"ui_{info.name}", engine=engine)

            tracer.log("llm_call", info.name, f"Created agent with {config['model']}")

            # Run
            result = asyncio.run(agent.arun(query))
            duration = (time.time() - start) * 1000

            tracer.log("output", info.name, str(result)[:1000])
            tracer.end_trace("completed")

        st.success(f"Completed in {duration:.0f}ms")

        # Display result
        if isinstance(result, dict):
            # Extract message content
            messages = result.get("messages", [])
            if messages:
                last = messages[-1]
                content = getattr(last, "content", str(last))
                st.markdown(content)
            else:
                st.json(result)
        elif isinstance(result, str):
            st.markdown(result)
        else:
            st.write(result)

    except Exception as e:
        tracer.log("error", info.name, str(e))
        tracer.end_trace("error")
        st.error(f"Error: {e}")
        with st.expander("Full traceback"):
            st.code(traceback.format_exc())
