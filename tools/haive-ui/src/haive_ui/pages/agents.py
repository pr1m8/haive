"""Agents page - browse and run agents with individual detail pages."""

import asyncio
import inspect
import time
import traceback

import streamlit as st

from haive_ui.utils.registry import (
    AGENT_REGISTRY,
    AgentInfo,
    get_agents_by_category,
    get_class_docstring,
    try_import,
    try_import_agent_config,
)
from haive_ui.utils.tracer import TraceCollector


def render():
    # Initialize tracer
    if "tracer" not in st.session_state:
        st.session_state.tracer = TraceCollector()

    # Check if user selected a specific agent
    selected = st.session_state.get("selected_agent")

    if selected is not None:
        _render_agent_detail(AGENT_REGISTRY[selected])
    else:
        _render_agent_list()


# -- Agent List View (Browse All) ----------------------------------------

def _render_agent_list():
    st.title("Agents")
    st.caption(f"{len(AGENT_REGISTRY)} agents across {len(get_agents_by_category())} categories")

    # Category filter + search
    col1, col2 = st.columns([1, 2])
    with col1:
        categories = list(get_agents_by_category().keys())
        selected_cats = st.multiselect(
            "Filter by category", categories, default=categories, key="agent_cat_filter"
        )
    with col2:
        search = st.text_input("Search agents", "", key="agent_search")

    # Filter agents
    filtered = [
        a for a in AGENT_REGISTRY
        if a.category in selected_cats
        and (not search or search.lower() in a.name.lower() or search.lower() in a.description.lower())
    ]

    st.caption(f"Showing {len(filtered)}/{len(AGENT_REGISTRY)} agents")
    st.divider()

    # Render as grid of cards, 3 per row
    by_cat = {}
    for a in filtered:
        by_cat.setdefault(a.category, []).append(a)

    for cat, agents in by_cat.items():
        st.subheader(f"{cat.title()} ({len(agents)})")
        rows = [agents[i:i + 3] for i in range(0, len(agents), 3)]
        for row in rows:
            cols = st.columns(3)
            for col, agent_info in zip(cols, row):
                with col:
                    _render_agent_tile(agent_info)
        st.divider()


def _render_agent_tile(info: AgentInfo):
    """Render a clickable tile for an agent."""
    idx = AGENT_REGISTRY.index(info)
    cls, err = try_import(info.module_path, info.class_name)
    status = "OK" if cls else "FAIL"

    with st.container(border=True):
        st.markdown(f"**{info.name}**")
        st.caption(info.description[:80] if info.description else "")
        tags_str = " ".join(f"`{t}`" for t in info.tags[:3]) if info.tags else ""
        if tags_str:
            st.markdown(tags_str)

        col_s, col_b = st.columns([1, 1])
        with col_s:
            if cls:
                st.success(status, icon=None)
            else:
                st.error(status, icon=None)
        with col_b:
            if st.button("Open", key=f"open_agent_{idx}", type="primary"):
                st.session_state.selected_agent = idx
                st.rerun()


# -- Agent Detail Page ----------------------------------------------------

def _render_agent_detail(info: AgentInfo):
    """Full detail page for a single agent."""
    idx = AGENT_REGISTRY.index(info)

    # Back button
    if st.button("< Back to Agents", key="back_agents"):
        st.session_state.selected_agent = None
        st.rerun()

    st.title(info.name)
    st.caption(f"Category: **{info.category}** | Module: `{info.module_path}`")

    # Import status
    cls, err = try_import(info.module_path, info.class_name)

    # Top info bar
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if cls:
            st.success("Import: OK")
        else:
            st.error("Import: FAIL")
    with col2:
        llm_cfg = st.session_state.llm_config
        st.info(f"LLM: {llm_cfg['provider']}/{llm_cfg['model']}")
    with col3:
        st.info(f"Temp: {llm_cfg['temperature']}")
    with col4:
        req = []
        if info.requires_docs:
            req.append("Documents")
        if info.requires_tools:
            req.append("Tools")
        st.info(f"Requires: {', '.join(req) if req else 'None'}")
    with col5:
        if info.is_abstract:
            st.warning("Abstract")
        elif info.is_function:
            st.info("Function")
        elif info.config_module:
            st.info("Config-based")
        else:
            st.success("Standard")

    if err:
        st.error(f"Import error: {err}")
        return

    # Tabs: Info, Run, Source, Trace History
    tab_info, tab_run, tab_source, tab_history = st.tabs(["Info", "Run", "Source", "Trace History"])

    with tab_info:
        _render_info_tab(info, cls)

    with tab_run:
        _render_run_tab(info, cls)

    with tab_source:
        _render_source_tab(info, cls)

    with tab_history:
        _render_trace_history(info)


def _render_info_tab(info: AgentInfo, cls):
    """Show detailed information about the agent."""
    st.subheader("Description")
    st.markdown(info.description)

    # Full docstring
    docstring = get_class_docstring(info.module_path, info.class_name)
    if docstring:
        st.subheader("Documentation")
        st.markdown(docstring)

    # Import code
    st.subheader("Import")
    st.code(f"from {info.module_path} import {info.class_name}", language="python")

    # Tags
    if info.tags:
        st.subheader("Tags")
        st.markdown(" ".join(f"`{t}`" for t in info.tags))

    # Class info
    if cls:
        st.subheader("Class Details")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Class:** `{cls.__name__}`")
            bases = [b.__name__ for b in cls.__mro__[1:4] if b.__name__ != "object"]
            if bases:
                st.markdown(f"**Inherits:** {' > '.join(bases)}")
        with col2:
            # Count public methods
            public_methods = [m for m in dir(cls) if not m.startswith("_") and callable(getattr(cls, m, None))]
            st.markdown(f"**Public Methods:** {len(public_methods)}")
            if info.factory_method:
                st.markdown(f"**Factory:** `{info.factory_method}()`")

        # Show key methods
        key_methods = [m for m in ["run", "arun", "invoke", "ainvoke", "build_graph", "compile"] if hasattr(cls, m)]
        if key_methods:
            st.markdown("**Key Methods:** " + ", ".join(f"`{m}()`" for m in key_methods))


def _render_run_tab(info: AgentInfo, cls):
    """Run the agent with a query."""
    st.subheader("Run Agent")

    if info.is_abstract:
        st.warning(f"{info.name} is an abstract base class and cannot be run directly. "
                   "Use one of its concrete subclasses instead.")
        return

    # LLM config summary
    llm_cfg = st.session_state.llm_config
    st.caption(f"Using: {llm_cfg['provider']}/{llm_cfg['model']} (temp={llm_cfg['temperature']}) -- change in sidebar")

    if info.requires_docs:
        st.info("This is a RAG agent that requires documents. Using sample documents for testing.")

    # Query input
    query = st.text_area(
        "Query",
        placeholder="Type your query here...",
        height=100,
        key=f"detail_query_{info.name}",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        run_btn = st.button("Run Agent", type="primary", key=f"detail_run_{info.name}")
    with col2:
        inst_btn = st.button("Test Instantiate", key=f"detail_inst_{info.name}")
    with col3:
        clear_btn = st.button("Clear Results", key=f"detail_clear_{info.name}")

    if clear_btn:
        st.session_state.pop(f"result_{info.name}", None)

    if inst_btn:
        _test_instantiate(info, cls)

    if run_btn and query:
        _run_agent(info, cls, query)
    elif run_btn and not query:
        st.warning("Please enter a query first.")

    # Show cached result
    cached = st.session_state.get(f"result_{info.name}")
    if cached:
        st.divider()
        st.subheader("Last Result")
        st.caption(f"Duration: {cached['duration']:.0f}ms | Query: {cached['query'][:100]}")
        _display_result(cached["result"])


def _render_source_tab(info: AgentInfo, cls):
    """Show the agent's source code."""
    st.subheader("Source Code")
    try:
        source_file = inspect.getfile(cls)
        st.caption(f"File: `{source_file}`")
        with open(source_file) as f:
            st.code(f.read(), language="python", line_numbers=True)
    except Exception as e:
        st.error(f"Could not load source: {e}")


def _render_trace_history(info: AgentInfo):
    """Show trace history for this agent."""
    st.subheader("Trace History")
    tracer: TraceCollector = st.session_state.tracer
    agent_traces = [t for t in tracer.traces if info.name in t.name]

    if not agent_traces:
        st.info("No traces yet. Run the agent to generate traces.")
        return

    for trace in reversed(agent_traces[-10:]):
        with st.expander(f"{trace.name} -- {trace.status} ({trace.total_duration_ms:.0f}ms)"):
            for event in trace.events:
                icon = {"input": ">>", "output": "<<", "llm_call": "AI", "error": "!!", "tool_call": "T>"}.get(event.event_type, "--")
                st.markdown(f"`{icon}` **{event.event_type}** ({event.agent_name}): {event.content[:200]}")


# -- Helpers ----------------------------------------------------------

def _make_engine():
    """Create AugLLMConfig from current sidebar settings."""
    from haive.core.engine.aug_llm import AugLLMConfig
    from haive.core.models.llm.base import OpenAILLMConfig

    cfg = st.session_state.llm_config
    model = cfg.get("model", "gpt-4o-mini")
    temperature = cfg.get("temperature", 0.7)

    llm_config = OpenAILLMConfig(model=model)
    kwargs = {"name": "ui_engine", "llm_config": llm_config, "temperature": temperature}

    system_prompt = st.session_state.get("system_prompt", "")
    if system_prompt:
        kwargs["system_message"] = system_prompt

    return AugLLMConfig(**kwargs)


def _create_agent_instance(info: AgentInfo, cls, engine=None):
    """Create an agent instance handling different init patterns."""
    import inspect as _inspect

    # Abstract classes can't be instantiated
    if info.is_abstract:
        raise RuntimeError(f"{info.name} is an abstract base class and cannot be instantiated directly.")

    # Factory method pattern (RAG from_documents)
    if info.factory_method == "from_documents":
        from langchain_core.documents import Document
        docs = [
            Document(page_content="Python is a high-level programming language created by Guido van Rossum."),
            Document(page_content="Machine learning is a subset of AI that uses algorithms to learn from data."),
            Document(page_content="LangChain is a framework for building LLM-powered applications."),
        ]
        if engine:
            try:
                return getattr(cls, info.factory_method)(documents=docs, name=f"ui_{info.name}", engine=engine)
            except Exception:
                pass
        return getattr(cls, info.factory_method)(documents=docs, name=f"ui_{info.name}")

    # Function pattern (self_discovery, create_synthesis_agent)
    # These return agent objects directly when called
    if info.is_function or (callable(cls) and not _inspect.isclass(cls)):
        obj = cls()
        # If the function returns something with run/arun, it's the agent
        if hasattr(obj, 'run') or hasattr(obj, 'arun') or hasattr(obj, 'invoke'):
            return obj
        # Otherwise it might be a config or something else
        return obj

    # Get init params
    try:
        sig = _inspect.signature(cls.__init__)
        params = list(sig.parameters.keys())
    except (ValueError, TypeError):
        params = []

    errors = []

    # If we have a known config class from registry, use it first
    if info.config_module and info.config_class:
        cfg_cls, cfg_err = try_import_agent_config(info)
        if cfg_cls:
            try:
                cfg_obj = cfg_cls()
                # Try multiple patterns with the config object
                for pattern_name, pattern_fn in [
                    ("name+config", lambda: cls(name=f"ui_{info.name}", config=cfg_obj)),
                    ("config-only", lambda: cls(config=cfg_obj)),
                    ("positional", lambda: cls(cfg_obj)),
                ]:
                    if pattern_name == "name+config" and "name" not in params:
                        continue
                    try:
                        return pattern_fn()
                    except Exception as e:
                        errors.append(f"registry-{pattern_name}: {e}")
            except Exception as e:
                errors.append(f"registry-config-create: {e}")

    # ReWOO-style: name + config (AugLLMConfig) + tools
    if "name" in params and "config" in params:
        cfg_to_use = engine or None
        if cfg_to_use:
            try:
                return cls(name=f"ui_{info.name}", config=cfg_to_use)
            except Exception as e:
                errors.append(f"name+augllm-config: {e}")
        # Try with default config
        try:
            return cls(name=f"ui_{info.name}")
        except Exception as e:
            errors.append(f"name+defaults: {e}")

    # Pydantic pattern: name + engine
    if engine:
        try:
            return cls(name=f"ui_{info.name}", engine=engine)
        except Exception as e:
            errors.append(f"name+engine: {e}")

    # Just engine
    if engine:
        try:
            return cls(engine=engine)
        except Exception as e:
            errors.append(f"engine: {e}")

    # No args
    try:
        return cls()
    except Exception as e:
        errors.append(f"no-args: {e}")

    # Just name
    try:
        return cls(name=f"ui_{info.name}")
    except Exception as e:
        errors.append(f"name-only: {e}")

    raise RuntimeError(f"Could not instantiate {info.name}. Tried {len(errors)} patterns. Errors: {'; '.join(errors[-3:])}")


def _test_instantiate(info: AgentInfo, cls):
    """Test instantiating an agent."""
    with st.spinner("Instantiating..."):
        try:
            engine = _make_engine()
            obj = _create_agent_instance(info, cls, engine)
            st.success(f"Instantiated: `{type(obj).__name__}`")

            # Show some details
            if hasattr(obj, "config"):
                st.caption(f"Config: {type(obj.config).__name__}")
            if hasattr(obj, "app") and obj.app is not None:
                st.caption("Graph compiled: Yes")
            elif hasattr(obj, "graph") and obj.graph is not None:
                st.caption("Graph compiled: Yes")

        except Exception as e:
            st.error(f"Failed: {e}")
            with st.expander("Full traceback"):
                st.code(traceback.format_exc())


def _run_agent(info: AgentInfo, cls, query: str):
    """Run an agent with the given query."""
    tracer: TraceCollector = st.session_state.tracer

    try:
        trace = tracer.start_trace(f"{info.name}: {query[:50]}")
        tracer.log("input", info.name, query)

        with st.spinner(f"Running {info.name}..."):
            start = time.time()

            # Create agent
            engine = _make_engine()
            agent = _create_agent_instance(info, cls, engine)

            cfg = st.session_state.llm_config
            tracer.log("llm_call", info.name, f"Created agent with {cfg['provider']}/{cfg['model']}")

            # Run - try multiple execution methods
            result = None
            run_errors = []
            for method_name in ["arun", "ainvoke", "run", "invoke"]:
                method = getattr(agent, method_name, None)
                if method is None:
                    continue
                try:
                    if method_name.startswith("a"):
                        loop = asyncio.new_event_loop()
                        result = loop.run_until_complete(method(query))
                        loop.close()
                    else:
                        result = method(query)
                    break
                except Exception as e:
                    run_errors.append(f"{method_name}: {e}")
                    continue
            if result is None and run_errors:
                raise RuntimeError(f"All run methods failed: {'; '.join(run_errors)}")

            duration = (time.time() - start) * 1000

            tracer.log("output", info.name, str(result)[:1000])
            tracer.end_trace("completed")

        st.success(f"Completed in {duration:.0f}ms")

        # Cache result
        st.session_state[f"result_{info.name}"] = {
            "result": result,
            "duration": duration,
            "query": query,
        }

        # Display result
        st.subheader("Result")
        _display_result(result)

    except Exception as e:
        tracer.log("error", info.name, str(e))
        tracer.end_trace("error")
        st.error(f"Error: {e}")
        with st.expander("Full traceback"):
            st.code(traceback.format_exc())


def _display_result(result):
    """Display agent result in a formatted way."""
    if isinstance(result, dict):
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
