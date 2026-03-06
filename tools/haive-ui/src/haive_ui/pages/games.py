"""Games page - play and run tournaments with LLM agents."""

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

    tab1, tab2 = st.tabs(["Play Game", "Import Status"])

    with tab1:
        _render_play_tab()

    with tab2:
        _render_status_tab()


def _render_play_tab():
    """Single game play interface."""
    categories = list(get_games_by_category().keys())
    selected_cat = st.selectbox("Category", categories, key="game_cat")

    games_in_cat = [g for g in GAME_REGISTRY if g.category == selected_cat]
    game_names = [g.name for g in games_in_cat]
    selected_name = st.selectbox("Game", game_names, key="game_select")
    game_info = next(g for g in games_in_cat if g.name == selected_name)

    # Game info
    st.markdown(f"**{game_info.description}**")
    st.caption(
        f"Players: {game_info.min_players}-{game_info.max_players} | "
        f"Tags: {', '.join(game_info.tags)} | "
        f"Has UI: {'Yes' if game_info.has_ui else 'No'}"
    )
    st.code(f"from {game_info.module_path} import {game_info.class_name}", language="python")

    # Import check
    cls, err = try_import(game_info.module_path, game_info.class_name)
    if not cls:
        st.error(f"Agent import failed: {err}")
        return

    config_cls, config_err = try_import_game_config(game_info)
    if config_cls:
        st.success(f"Game loaded: {game_info.class_name} + {game_info.config_class}")
    else:
        st.warning(f"Agent OK, config import issue: {config_err}")

    st.divider()

    # View example source
    if game_info.example_module:
        with st.expander("View Example Source"):
            try:
                mod = __import__(game_info.example_module, fromlist=["__file__"])
                if hasattr(mod, "__file__") and mod.__file__:
                    with open(mod.__file__) as f:
                        st.code(f.read(), language="python", line_numbers=True)
                else:
                    st.info("Example module found but no source file available")
            except Exception as e:
                st.error(f"Cannot load example: {e}")

    # Run game via example module
    st.subheader("Run Game")
    st.caption("Games run via their example scripts and stream output to the terminal.")

    max_timeout = st.number_input("Timeout (seconds)", 30, 300, 120, key=f"timeout_{game_info.name}")

    if st.button("Run Game Example", type="primary", key=f"run_{game_info.name}"):
        _run_game_example(game_info, int(max_timeout))


def _run_game_example(game_info: GameInfo, timeout: int):
    """Run a game's example script via subprocess."""
    if not game_info.example_module:
        st.error("No example module configured for this game")
        return

    # Convert module path to -m arg
    module_path = game_info.example_module

    with st.spinner(f"Running {game_info.name} example..."):
        try:
            result = subprocess.run(
                [sys.executable, "-m", module_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.environ.get("HAIVE_ROOT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..")),
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )

            if result.returncode == 0:
                st.success(f"{game_info.name} example completed successfully")
            else:
                st.error(f"{game_info.name} example failed (exit {result.returncode})")

            if result.stdout:
                with st.expander("Output", expanded=True):
                    lines = result.stdout.strip().split("\n")
                    # Show last 100 lines
                    st.code("\n".join(lines[-100:]))

            if result.stderr and result.returncode != 0:
                with st.expander("Errors"):
                    st.code(result.stderr[-3000:])

        except subprocess.TimeoutExpired:
            st.error(f"{game_info.name} timed out ({timeout}s)")
        except Exception as e:
            st.error(f"Error: {e}")
            with st.expander("Traceback"):
                st.code(traceback.format_exc())


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
            "Agent": "OK" if cls else f"FAIL: {err}",
            "Config": "OK" if cfg_cls else f"FAIL: {cfg_err}" if cfg_err else "N/A",
            "Example": g.example_module or "None",
            "Has UI": "Yes" if g.has_ui else "No",
            "Players": f"{g.min_players}-{g.max_players}",
        })

    st.dataframe(results, use_container_width=True)

    # Summary
    agent_ok = sum(1 for r in results if r["Agent"] == "OK")
    config_ok = sum(1 for r in results if r["Config"] == "OK")
    st.caption(f"Agents: {agent_ok}/{len(results)} OK | Configs: {config_ok}/{len(results)} OK")
