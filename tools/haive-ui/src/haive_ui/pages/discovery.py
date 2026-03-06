"""Discovery & MCP page - browse discovery agents and MCP tools."""

import traceback

import streamlit as st

from haive_ui.utils.registry import try_import


# -- Discovery Module Registry ------------------------------------------------

DISCOVERY_MODULES = [
    {
        "name": "Component Discovery Agent",
        "module": "haive.agents.discovery.component_discovery_agent",
        "class": "ComponentDiscoveryAgent",
        "description": "RAG-based agent for discovering components from documentation. "
                       "Uses MetaStateSchema for tracking and follows the Dynamic Activation Pattern.",
        "features": [
            "RAG-based component discovery",
            "MetaStateSchema integration",
            "Automatic document loading",
            "Component parsing & metadata",
            "Caching for performance",
        ],
        "usage": 'ComponentDiscoveryAgent(document_path="@haive-tools")',
    },
    {
        "name": "Dynamic Tool Selector",
        "module": "haive.agents.discovery.dynamic_tool_selector",
        "class": "DynamicToolSelector",
        "description": "LangGraph-style dynamic tool selection and management. "
                       "Context-aware selection, intelligent routing, usage learning.",
        "features": [
            "Dynamic tool selection",
            "Context-aware recommendation",
            "Tool usage learning",
            "LangGraph-style binding",
            "Iterative refinement",
        ],
        "usage": "create_dynamic_tool_selector(selection_mode=SelectionMode.DYNAMIC)",
    },
    {
        "name": "Semantic Discovery Engine",
        "module": "haive.agents.discovery.semantic_discovery",
        "class": "SemanticDiscoveryEngine",
        "description": "Vector-based tool discovery using semantic similarity. "
                       "Query analysis, capability matching, and tool recommendation.",
        "features": [
            "Vector-based tool discovery",
            "Semantic capability matching",
            "Query analysis & classification",
            "Hybrid selection strategies",
            "Component registry integration",
        ],
        "usage": "create_semantic_discovery()",
    },
    {
        "name": "Selection Strategies",
        "module": "haive.agents.discovery.selection_strategies",
        "class": "EnsembleSelectionStrategy",
        "description": "Multiple tool selection strategies: semantic, capability-based, "
                       "adaptive, contextual, ensemble, and learning-based.",
        "features": [
            "Semantic similarity selection",
            "Capability-based matching",
            "Adaptive learning selection",
            "Contextual conversation-aware",
            "Ensemble multi-strategy voting",
            "Learning from feedback",
        ],
        "usage": 'create_selection_strategy("ensemble")',
    },
]

MCP_MODULES = [
    {
        "name": "MCP Manager",
        "module": "haive.mcp.manager",
        "class": "MCPManager",
        "description": "Central manager for MCP server lifecycle, tool discovery, and integration.",
        "category": "core",
    },
    {
        "name": "Server Converter",
        "module": "haive.mcp.registry.server_converter",
        "class": "ServerConverter",
        "description": "Converts MCP server tools to LangChain-compatible tools.",
        "category": "registry",
    },
    {
        "name": "Bulk Installer",
        "module": "haive.mcp.installer.bulk_installer",
        "class": "MCPBulkInstaller",
        "description": "Install and configure multiple MCP servers in bulk.",
        "category": "installer",
    },
    {
        "name": "Browser Plugin",
        "module": "haive.mcp.plugins.browser_plugin",
        "class": "MCPBrowserPlugin",
        "description": "MCP plugin for browser automation and web interaction.",
        "category": "plugin",
    },
    {
        "name": "MCP Retrieval",
        "module": "haive.mcp.retrieval",
        "class": None,
        "description": "Retrieval-augmented MCP tool discovery and selection.",
        "category": "retrieval",
    },
]


def render():
    st.title("Discovery & MCP")

    tab1, tab2, tab3, tab4 = st.tabs(["Discovery Agents", "MCP Tools", "Self-Query Demo", "Import Status"])

    with tab1:
        _render_discovery_tab()

    with tab2:
        _render_mcp_tab()

    with tab3:
        _render_self_query_demo()

    with tab4:
        _render_import_status()


# -- Discovery Tab -----------------------------------------------------------

def _render_discovery_tab():
    """Browse and test discovery agents."""
    st.subheader("Discovery Agents")
    st.markdown(
        "These agents provide **dynamic tool/component discovery** using semantic search, "
        "capability matching, and adaptive selection strategies."
    )

    for mod_info in DISCOVERY_MODULES:
        _render_discovery_card(mod_info)


def _render_discovery_card(info: dict):
    """Render a single discovery module card."""
    cls, err = try_import(info["module"], info["class"])
    status = "OK" if cls else "FAIL"

    with st.expander(f"**{info['name']}** [{status}]"):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"**{info['description']}**")
            st.code(f"from {info['module']} import {info['class']}", language="python")

            if info.get("usage"):
                st.caption(f"Usage: `{info['usage']}`")

        with col2:
            if cls:
                st.success("Import OK")
            else:
                st.error(f"Import: {err}")

        # Features list
        if info.get("features"):
            st.markdown("**Capabilities:**")
            for feat in info["features"]:
                st.markdown(f"- {feat}")

        # Test instantiation
        if cls and st.button("Test Import Details", key=f"test_disc_{info['name']}"):
            _test_discovery_module(info, cls)


def _test_discovery_module(info: dict, cls):
    """Show details about a discovery module."""
    try:
        import inspect
        docstring = inspect.getdoc(cls)
        if docstring:
            st.caption(docstring[:500])

        methods = [m for m in dir(cls) if not m.startswith("_") and callable(getattr(cls, m, None))]
        if methods:
            st.markdown("**Public Methods:**")
            for m in methods[:15]:
                st.markdown(f"- `{m}()`")

    except Exception as e:
        st.error(f"Error inspecting: {e}")
        with st.expander("Details"):
            st.code(traceback.format_exc())


# -- MCP Tab -----------------------------------------------------------------

def _render_mcp_tab():
    """Browse MCP integration modules."""
    st.subheader("MCP Integration")
    st.markdown(
        "**Model Context Protocol** modules for connecting to external tools and data sources. "
        "MCP enables standardized tool integration across LLM frameworks."
    )

    # Group by category
    categories: dict[str, list[dict]] = {}
    for mod in MCP_MODULES:
        categories.setdefault(mod["category"], []).append(mod)

    for cat, modules in categories.items():
        st.markdown(f"### {cat.title()}")
        for mod_info in modules:
            _render_mcp_card(mod_info)


def _render_mcp_card(info: dict):
    """Render a single MCP module card."""
    if info["class"]:
        cls, err = try_import(info["module"], info["class"])
        status = "OK" if cls else "FAIL"
    else:
        try:
            import importlib
            importlib.import_module(info["module"])
            cls, err = True, None
            status = "OK"
        except Exception as e:
            cls, err = None, f"{type(e).__name__}: {str(e)[:80]}"
            status = "FAIL"

    with st.expander(f"**{info['name']}** [{status}]"):
        st.markdown(f"**{info['description']}**")

        if info["class"]:
            st.code(f"from {info['module']} import {info['class']}", language="python")
        else:
            st.code(f"import {info['module']}", language="python")

        if cls:
            st.success("Import OK")
        else:
            st.error(f"Import: {err}")


# -- Self-Query Demo ---------------------------------------------------------

def _render_self_query_demo():
    """Interactive demo of self-query and dynamic tool discovery."""
    st.subheader("Self-Query & Dynamic Tool Discovery")
    st.markdown(
        "Query the framework to discover agents, tools, and capabilities dynamically. "
        "This uses the discovery system to match your query to available components."
    )

    # Build tool/agent catalog from registries
    from haive_ui.utils.registry import AGENT_REGISTRY, GAME_REGISTRY

    all_components = []
    for a in AGENT_REGISTRY:
        all_components.append({
            "name": a.name,
            "type": "Agent",
            "category": a.category,
            "description": a.description,
            "module": a.module_path,
            "class": a.class_name,
            "tags": a.tags,
            "requires_docs": a.requires_docs,
            "requires_tools": a.requires_tools,
            "is_abstract": a.is_abstract,
            "is_function": a.is_function,
        })
    for g in GAME_REGISTRY:
        all_components.append({
            "name": g.name,
            "type": "Game",
            "category": g.category,
            "description": g.description,
            "module": g.module_path,
            "class": g.class_name,
            "tags": g.tags,
            "has_ui": g.has_ui,
            "players": f"{g.min_players}-{g.max_players}",
        })
    for d in DISCOVERY_MODULES:
        all_components.append({
            "name": d["name"],
            "type": "Discovery",
            "category": "discovery",
            "description": d["description"],
            "module": d["module"],
            "class": d["class"],
            "tags": [],
        })
    for m in MCP_MODULES:
        all_components.append({
            "name": m["name"],
            "type": "MCP",
            "category": m.get("category", "mcp"),
            "description": m["description"],
            "module": m["module"],
            "class": m.get("class", ""),
            "tags": [],
        })

    st.caption(f"Searching across {len(all_components)} registered components")

    # Query input
    query = st.text_input(
        "What are you looking for?",
        placeholder="e.g., 'RAG agent for document retrieval', 'strategy game', 'tool discovery'...",
        key="discovery_query",
    )

    col1, col2 = st.columns(2)
    with col1:
        type_filter = st.multiselect(
            "Component Type",
            ["Agent", "Game", "Discovery", "MCP"],
            default=["Agent", "Game", "Discovery", "MCP"],
            key="disc_type_filter",
        )
    with col2:
        max_results = st.slider("Max Results", 3, 20, 10, key="disc_max_results")

    if query:
        _run_self_query(query, all_components, type_filter, max_results)
    else:
        # Show all components grouped by type
        st.divider()
        st.subheader("All Components")
        for comp_type in ["Agent", "Game", "Discovery", "MCP"]:
            items = [c for c in all_components if c["type"] == comp_type]
            if items:
                with st.expander(f"**{comp_type}** ({len(items)})"):
                    for item in items:
                        tags = " ".join(f"`{t}`" for t in item.get("tags", [])[:3])
                        st.markdown(f"- **{item['name']}** ({item.get('category', '')}) {tags}")
                        st.caption(f"  {item['description'][:100]}")


def _run_self_query(query: str, components: list, type_filter: list, max_results: int):
    """Run a self-query against the component catalog."""
    query_lower = query.lower()
    query_terms = query_lower.split()

    scored = []
    for comp in components:
        if comp["type"] not in type_filter:
            continue

        score = 0
        text = f"{comp['name']} {comp['description']} {comp.get('category', '')} {' '.join(comp.get('tags', []))}"
        text_lower = text.lower()

        # Exact phrase match
        if query_lower in text_lower:
            score += 10

        # Individual term matches
        for term in query_terms:
            if term in text_lower:
                score += 3
            if term in comp["name"].lower():
                score += 5
            if term in comp.get("category", "").lower():
                score += 2
            for tag in comp.get("tags", []):
                if term in tag.lower():
                    score += 4

        if score > 0:
            scored.append((score, comp))

    scored.sort(key=lambda x: -x[0])
    results = scored[:max_results]

    st.divider()

    if not results:
        st.warning(f"No components found matching '{query}'. Try different keywords.")
        return

    st.success(f"Found {len(results)} matching components")

    for score, comp in results:
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{comp['name']}** ({comp['type']})")
                st.caption(comp["description"][:150])
            with col2:
                st.markdown(f"Category: `{comp.get('category', 'n/a')}`")
                tags = " ".join(f"`{t}`" for t in comp.get("tags", [])[:4])
                if tags:
                    st.markdown(tags)
            with col3:
                st.metric("Relevance", f"{score}")
                cls_name = comp.get("class", "")
                if cls_name:
                    st.code(f"from {comp['module']} import {cls_name}", language="python")

    # LLM-powered discovery option
    st.divider()
    st.subheader("LLM-Powered Discovery")
    st.caption("Use the LLM to analyze your query and recommend components with reasoning.")

    if st.button("Run LLM Discovery", key="llm_discovery_btn"):
        _run_llm_discovery(query, results)


def _run_llm_discovery(query: str, keyword_results: list):
    """Use LLM to provide intelligent component recommendations."""
    import asyncio
    import time

    llm_cfg = st.session_state.llm_config

    # Build context from search results
    context = "Available components:\n"
    for score, comp in keyword_results:
        context += f"- {comp['name']} ({comp['type']}/{comp.get('category', '')}): {comp['description'][:100]}\n"

    with st.spinner(f"Querying {llm_cfg['model']}..."):
        try:
            from haive.core.engine.aug_llm import AugLLMConfig
            from haive.core.models.llm.base import OpenAILLMConfig
            from haive.agents.simple.agent import SimpleAgent

            engine = AugLLMConfig(
                llm_config=OpenAILLMConfig(model=llm_cfg.get("model", "gpt-4o-mini")),
                temperature=llm_cfg.get("temperature", 0.3),
                system_message=(
                    "You are a framework expert helping users discover the right components. "
                    "Given a user query and available components, recommend the best matches "
                    "with clear reasoning. Be concise."
                ),
            )

            agent = SimpleAgent(name="discovery_llm", engine=engine)

            prompt = (
                f"User query: {query}\n\n"
                f"{context}\n\n"
                "Which components best match this query? Recommend the top 3 with reasoning."
            )

            start = time.time()
            loop = asyncio.new_event_loop()
            result = loop.run_until_complete(agent.arun(prompt))
            loop.close()
            duration = (time.time() - start) * 1000

            st.success(f"LLM responded in {duration:.0f}ms")

            # Display result
            if isinstance(result, dict):
                messages = result.get("messages", [])
                if messages:
                    content = getattr(messages[-1], "content", str(messages[-1]))
                    st.markdown(content)
                else:
                    st.json(result)
            elif isinstance(result, str):
                st.markdown(result)
            else:
                st.write(result)

        except Exception as e:
            st.error(f"LLM discovery failed: {e}")
            with st.expander("Details"):
                st.code(traceback.format_exc())


# -- Import Status -----------------------------------------------------------

def _render_import_status():
    """Show import status for all discovery and MCP modules."""
    st.subheader("Import Status")

    results = []

    # Discovery modules
    for mod_info in DISCOVERY_MODULES:
        cls, err = try_import(mod_info["module"], mod_info["class"])
        results.append({
            "Component": mod_info["name"],
            "Type": "Discovery",
            "Module": mod_info["module"],
            "Status": "OK" if cls else "FAIL",
            "Error": "" if cls else (err or ""),
        })

    # MCP modules
    for mod_info in MCP_MODULES:
        if mod_info["class"]:
            cls, err = try_import(mod_info["module"], mod_info["class"])
        else:
            try:
                import importlib
                importlib.import_module(mod_info["module"])
                cls, err = True, None
            except Exception as e:
                cls, err = None, f"{type(e).__name__}: {str(e)[:80]}"

        results.append({
            "Component": mod_info["name"],
            "Type": "MCP",
            "Module": mod_info["module"],
            "Status": "OK" if cls else "FAIL",
            "Error": "" if cls else (err or ""),
        })

    st.dataframe(results, use_container_width=True)

    ok_count = sum(1 for r in results if r["Status"] == "OK")
    disc_ok = sum(1 for r in results if r["Type"] == "Discovery" and r["Status"] == "OK")
    mcp_ok = sum(1 for r in results if r["Type"] == "MCP" and r["Status"] == "OK")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Discovery", f"{disc_ok}/{len(DISCOVERY_MODULES)}")
    with col2:
        st.metric("MCP", f"{mcp_ok}/{len(MCP_MODULES)}")
    with col3:
        st.metric("Total OK", f"{ok_count}/{len(results)}")
