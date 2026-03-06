"""Home page - dashboard overview."""

import streamlit as st

from haive_ui.utils.registry import (
    AGENT_REGISTRY,
    GAME_REGISTRY,
    get_agents_by_category,
    get_games_by_category,
    try_import,
    try_import_game_config,
)


def render():
    st.title("Haive AI Agent Framework")
    st.markdown("**Dynamic agents, games, and multi-agent systems powered by LLMs.**")

    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Agents", len(AGENT_REGISTRY))
    with col2:
        st.metric("Games", len(GAME_REGISTRY))
    with col3:
        st.metric("Agent Categories", len(get_agents_by_category()))
    with col4:
        st.metric("Game Categories", len(get_games_by_category()))
    with col5:
        st.metric("Discovery/MCP", "9 modules")

    st.divider()

    # Current LLM config
    cfg = st.session_state.get("llm_config", {})
    st.subheader("Current LLM Configuration")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"**Provider:** {cfg.get('provider', 'openai')}")
    with col2:
        st.markdown(f"**Model:** {cfg.get('model', 'gpt-4o-mini')}")
    with col3:
        st.markdown(f"**Temperature:** {cfg.get('temperature', 0.7)}")
    with col4:
        st.markdown(f"**Max Tokens:** {cfg.get('max_tokens', 2000)}")

    sys_prompt = st.session_state.get("system_prompt", "")
    if sys_prompt:
        st.caption(f"System prompt: {sys_prompt[:100]}...")

    st.divider()

    # Agent categories overview
    st.subheader("Agent Categories")
    for cat, agents in get_agents_by_category().items():
        with st.expander(f"**{cat.title()}** ({len(agents)} agents)"):
            for a in agents:
                st.markdown(f"- **{a.name}** -- {a.description}")

    st.divider()

    # Game categories overview
    st.subheader("Game Categories")
    for cat, games in get_games_by_category().items():
        with st.expander(f"**{cat.replace('_', ' ').title()}** ({len(games)} games)"):
            for g in games:
                ui_tag = " [UI]" if g.has_ui else ""
                st.markdown(f"- **{g.name}** -- {g.description} ({g.min_players}-{g.max_players} players){ui_tag}")

    st.divider()

    # Quick health check
    st.subheader("Quick Health Check")
    if st.button("Run Import Check"):
        _run_health_check()


def _run_health_check():
    """Quick import check for all registered components."""
    progress = st.progress(0, text="Checking...")
    total = len(AGENT_REGISTRY) + len(GAME_REGISTRY)
    checked = 0

    # Agents
    agent_ok = agent_fail = 0
    agent_errors = []
    for a in AGENT_REGISTRY:
        cls, err = try_import(a.module_path, a.class_name)
        checked += 1
        progress.progress(checked / total)
        if cls:
            agent_ok += 1
        else:
            agent_fail += 1
            agent_errors.append(f"{a.name}: {err}")

    # Games
    game_ok = game_fail = 0
    game_errors = []
    for g in GAME_REGISTRY:
        cls, err = try_import(g.module_path, g.class_name)
        checked += 1
        progress.progress(checked / total)
        if cls:
            game_ok += 1
        else:
            game_fail += 1
            game_errors.append(f"{g.name}: {err}")

    progress.progress(1.0, text="Done!")

    col1, col2 = st.columns(2)
    with col1:
        if agent_fail == 0:
            st.success(f"Agents: {agent_ok}/{agent_ok} OK")
        else:
            st.warning(f"Agents: {agent_ok}/{agent_ok + agent_fail} OK")
            for e in agent_errors:
                st.error(f"  {e}")

    with col2:
        if game_fail == 0:
            st.success(f"Games: {game_ok}/{game_ok} OK")
        else:
            st.warning(f"Games: {game_ok}/{game_ok + game_fail} OK")
            for e in game_errors:
                st.error(f"  {e}")
