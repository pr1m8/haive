"""Discovery & MCP page - browse discovery agents and MCP tools."""

import traceback

import streamlit as st

from haive_ui.utils.registry import try_import


# ── Discovery Module Registry ──────────────────────────────────────

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

    tab1, tab2, tab3 = st.tabs(["Discovery Agents", "MCP Tools", "Import Status"])

    with tab1:
        _render_discovery_tab()

    with tab2:
        _render_mcp_tab()

    with tab3:
        _render_import_status()


# ── Discovery Tab ──────────────────────────────────────────────────

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
        # Show class docstring
        docstring = inspect.getdoc(cls)
        if docstring:
            st.caption(docstring[:500])

        # Show public methods
        methods = [m for m in dir(cls) if not m.startswith("_") and callable(getattr(cls, m, None))]
        if methods:
            st.markdown("**Public Methods:**")
            for m in methods[:15]:
                st.markdown(f"- `{m}()`")

    except Exception as e:
        st.error(f"Error inspecting: {e}")
        with st.expander("Details"):
            st.code(traceback.format_exc())


# ── MCP Tab ────────────────────────────────────────────────────────

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
        # Module-level import check
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


# ── Import Status ──────────────────────────────────────────────────

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
    fail_count = len(results) - ok_count
    disc_ok = sum(1 for r in results if r["Type"] == "Discovery" and r["Status"] == "OK")
    mcp_ok = sum(1 for r in results if r["Type"] == "MCP" and r["Status"] == "OK")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Discovery", f"{disc_ok}/{len(DISCOVERY_MODULES)}")
    with col2:
        st.metric("MCP", f"{mcp_ok}/{len(MCP_MODULES)}")
    with col3:
        st.metric("Total OK", f"{ok_count}/{len(results)}")
