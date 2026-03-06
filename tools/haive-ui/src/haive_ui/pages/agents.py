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
    with st.expander(f"**{info.name}** -- {info.category}", expanded=False):
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

            if info.requires_docs:
                st.info("Requires documents (RAG agent)")
            if info.requires_tools:
                st.info("Requires tools")

        with col2:
            # Import status
            cls, err = try_import(info.module_path, info.class_name)
            if cls:
                st.success("Import OK")
            else:
                st.error(f"Import failed: {err}")
                return

            # LLM config from sidebar
            llm_cfg = st.session_state.llm_config.copy()
            st.caption(f"LLM: {llm_cfg['provider']}/{llm_cfg['model']}")
            st.caption(f"Temp: {llm_cfg['temperature']}")

        # Run agent section
        if not info.requires_docs:
            st.divider()
            query = st.text_input("Query", key=f"query_{info.name}", placeholder="Ask something...")

            col_run, col_inst = st.columns(2)
            with col_run:
                if st.button("Run Agent", key=f"run_{info.name}", type="primary") and query:
                    _run_agent(info, cls, query)
            with col_inst:
                if st.button("Test Instantiate", key=f"inst_{info.name}"):
                    _test_instantiate(info, cls)


def _test_instantiate(info: AgentInfo, cls):
    """Test instantiating an agent."""
    try:
        if info.factory_method == "from_documents":
            from langchain_core.documents import Document
            docs = [
                Document(page_content="Python is a programming language."),
                Document(page_content="Machine learning uses algorithms to learn from data."),
            ]
            obj = getattr(cls, info.factory_method)(documents=docs, name=f"test_{info.name}")
        else:
            # Try with engine first, then without
            try:
                engine = _make_engine()
                obj = cls(name=f"test_{info.name}", engine=engine)
            except Exception:
                obj = cls(name=f"test_{info.name}")
        st.success(f"Instantiated: {type(obj).__name__}")
    except Exception as e:
        st.error(f"Failed: {e}")
        with st.expander("Details"):
            st.code(traceback.format_exc())


def _make_engine():
    """Create AugLLMConfig from current sidebar settings."""
    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.core.models.llm.base import OpenAILLMConfig

    cfg = st.session_state.llm_config
    provider = cfg.get("provider", "openai")
    model = cfg.get("model", "gpt-4o-mini")
    temperature = cfg.get("temperature", 0.7)

    llm_config = OpenAILLMConfig(model=model)

    kwargs = {"name": "ui_engine", "llm_config": llm_config, "temperature": temperature}

    system_prompt = st.session_state.get("system_prompt", "")
    if system_prompt:
        kwargs["system_message"] = system_prompt

    return AugLLMConfig(**kwargs)


def _run_agent(info: AgentInfo, cls, query: str):
    """Run an agent with the given query."""
    tracer: TraceCollector = st.session_state.tracer

    try:
        trace = tracer.start_trace(f"{info.name}: {query[:50]}")
        tracer.log("input", info.name, query)

        with st.spinner(f"Running {info.name}..."):
            start = time.time()

            # Create agent with LLM config
            engine = _make_engine()

            if info.factory_method == "from_documents":
                from langchain_core.documents import Document
                docs = [Document(page_content="Test document for RAG agent.")]
                agent = getattr(cls, info.factory_method)(documents=docs, name=f"ui_{info.name}", engine=engine)
            else:
                try:
                    agent = cls(name=f"ui_{info.name}", engine=engine)
                except Exception:
                    agent = cls(name=f"ui_{info.name}")

            cfg = st.session_state.llm_config
            tracer.log("llm_call", info.name, f"Created agent with {cfg['provider']}/{cfg['model']}")

            # Run - try async first, fall back to sync
            try:
                loop = asyncio.new_event_loop()
                result = loop.run_until_complete(agent.arun(query))
                loop.close()
            except Exception:
                result = agent.run(query)

            duration = (time.time() - start) * 1000

            tracer.log("output", info.name, str(result)[:1000])
            tracer.end_trace("completed")

        st.success(f"Completed in {duration:.0f}ms")

        # Display result
        st.subheader("Result")
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
