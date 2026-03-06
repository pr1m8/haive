"""Games page - browse, configure, and run game agents."""

import subprocess
import sys
import os
import traceback

import streamlit as st

from haive_ui.utils.registry import (
    GAME_REGISTRY,
    GameInfo,
    get_games_by_category,
    try_import,
    try_import_game_config,
)


def render():
    st.title("Games")

    tab1, tab2, tab3 = st.tabs(["Browse Games", "Run Game", "Import Status"])

    with tab1:
        _render_browse_tab()

    with tab2:
        _render_run_tab()

    with tab3:
        _render_status_tab()


# ── Browse Tab ──────────────────────────────────────────────────────

def _render_browse_tab():
    """Browse all games with details."""
    search = st.text_input("Search games", "", key="game_search_browse")

    for cat, games in get_games_by_category().items():
        filtered = [g for g in games
                    if not search or search.lower() in g.name.lower()
                    or search.lower() in g.description.lower()]
        if not filtered:
            continue

        st.subheader(f"{cat.replace('_', ' ').title()} ({len(filtered)})")

        for g in filtered:
            _render_game_card(g)


def _render_game_card(g: GameInfo):
    """Render a single game info card."""
    cls, err = try_import(g.module_path, g.class_name)
    status_icon = "OK" if cls else "FAIL"

    with st.expander(f"**{g.name}** -- {g.description} [{status_icon}]"):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"**{g.description}**")
            st.caption(f"Players: {g.min_players}-{g.max_players} | Tags: {', '.join(g.tags)}")
            st.code(f"from {g.module_path} import {g.class_name}", language="python")

            if g.config_module and g.config_class:
                st.code(f"from {g.config_module} import {g.config_class}", language="python")

            if g.example_module:
                st.caption(f"Example: `python -m {g.example_module}`")

        with col2:
            if cls:
                st.success("Agent: OK")
            else:
                st.error(f"Agent: {err}")

            cfg_cls, cfg_err = try_import_game_config(g)
            if cfg_cls:
                st.success("Config: OK")
            else:
                st.warning(f"Config: {cfg_err}")

            st.caption(f"Has UI: {'Yes' if g.has_ui else 'No'}")

        # View example source
        if g.example_module:
            if st.button("View Example Source", key=f"view_src_{g.name}"):
                _show_example_source(g)


def _show_example_source(g: GameInfo):
    """Display example source code."""
    try:
        mod = __import__(g.example_module, fromlist=["__file__"])
        if hasattr(mod, "__file__") and mod.__file__:
            with open(mod.__file__) as f:
                st.code(f.read(), language="python", line_numbers=True)
        else:
            st.info("No source file found")
    except Exception as e:
        st.error(f"Cannot load: {e}")


# ── Run Tab ─────────────────────────────────────────────────────────

def _render_run_tab():
    """Run a specific game."""
    categories = list(get_games_by_category().keys())
    selected_cat = st.selectbox("Category", categories, key="game_run_cat")

    games_in_cat = [g for g in GAME_REGISTRY if g.category == selected_cat]
    game_names = [g.name for g in games_in_cat]
    selected_name = st.selectbox("Game", game_names, key="game_run_select")
    game_info = next(g for g in games_in_cat if g.name == selected_name)

    # Game info header
    st.markdown(f"### {game_info.name}")
    st.markdown(f"**{game_info.description}**")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Min Players", game_info.min_players)
    with col2:
        st.metric("Max Players", game_info.max_players)
    with col3:
        st.metric("Has UI", "Yes" if game_info.has_ui else "No")
    with col4:
        cls, _ = try_import(game_info.module_path, game_info.class_name)
        st.metric("Import", "OK" if cls else "FAIL")

    st.divider()

    # LLM config display
    llm_cfg = st.session_state.llm_config
    st.caption(f"Current LLM: {llm_cfg['provider']}/{llm_cfg['model']} (temp={llm_cfg['temperature']})")
    st.caption("Change LLM settings in the sidebar.")

    st.divider()

    # Run options
    timeout = st.slider("Timeout (seconds)", 15, 300, 60, key=f"timeout_run_{game_info.name}")

    col_run, col_view = st.columns(2)
    with col_run:
        if st.button("Run Game Example", type="primary", key=f"runbtn_{game_info.name}"):
            _run_game(game_info, timeout)
    with col_view:
        if st.button("View Example Source", key=f"viewbtn_{game_info.name}"):
            _show_example_source(game_info)


def _run_game(game_info: GameInfo, timeout: int):
    """Run a game's example via subprocess with rich output."""
    if not game_info.example_module:
        st.error("No example module configured")
        return

    with st.spinner(f"Running {game_info.name}..."):
        try:
            result = subprocess.run(
                [sys.executable, "-m", game_info.example_module],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.environ.get("HAIVE_ROOT", "/home/will/Projects/haive"),
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )

            if result.returncode == 0:
                st.success(f"{game_info.name} completed successfully")
            else:
                st.error(f"{game_info.name} failed (exit {result.returncode})")

            # Rich output display
            if result.stdout:
                stdout_lines = result.stdout.strip().split("\n")

                # Show summary metrics
                _show_output_summary(game_info, stdout_lines)

                # Full output in expander
                with st.expander("Full Output", expanded=True):
                    # Show last 200 lines (most games have a lot of rich output)
                    display_lines = stdout_lines[-200:]
                    # Strip ANSI codes for cleaner display
                    import re
                    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
                    clean_lines = [ansi_escape.sub('', line) for line in display_lines]
                    st.code("\n".join(clean_lines))

            if result.stderr and result.returncode != 0:
                with st.expander("Errors"):
                    st.code(result.stderr[-3000:])

        except subprocess.TimeoutExpired:
            st.warning(f"{game_info.name} timed out after {timeout}s (likely waiting for LLM API calls)")
            st.info("This usually means the game works but needs active LLM API keys to complete.")
        except Exception as e:
            st.error(f"Error: {e}")
            with st.expander("Traceback"):
                st.code(traceback.format_exc())


def _show_output_summary(game_info: GameInfo, lines: list[str]):
    """Extract and show key info from game output."""
    # Look for common game output patterns
    import re
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')

    clean_lines = [ansi_escape.sub('', line).strip() for line in lines]

    # Find status/result lines
    result_lines = [l for l in clean_lines if any(kw in l.lower() for kw in
                    ["completed", "winner", "result", "game over", "final", "score", "pass", "fail"])]

    if result_lines:
        st.subheader("Key Results")
        for line in result_lines[-5:]:
            if line:
                st.markdown(f"- {line}")


# ── Status Tab ──────────────────────────────────────────────────────

def _render_status_tab():
    """Show import status of all games."""
    st.subheader("Game Import Status")

    results = []
    for g in GAME_REGISTRY:
        cls, err = try_import(g.module_path, g.class_name)
        cfg_cls, cfg_err = try_import_game_config(g)

        results.append({
            "Game": g.name,
            "Category": g.category,
            "Agent": "OK" if cls else "FAIL",
            "Config": "OK" if cfg_cls else "FAIL",
            "Has UI": g.has_ui,
            "Players": f"{g.min_players}-{g.max_players}",
            "Example": g.example_module or "None",
        })

    st.dataframe(results, use_container_width=True)

    agent_ok = sum(1 for r in results if r["Agent"] == "OK")
    config_ok = sum(1 for r in results if r["Config"] == "OK")
    st.caption(f"Agents: {agent_ok}/{len(results)} OK | Configs: {config_ok}/{len(results)} OK")
