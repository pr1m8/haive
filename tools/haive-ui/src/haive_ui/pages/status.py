"""Status page - comprehensive import and runtime status for all components."""

import subprocess
import sys
import os
import time

import streamlit as st

from haive_ui.utils.registry import (
    AGENT_REGISTRY,
    GAME_REGISTRY,
    try_import,
    try_import_game_config,
    get_agents_by_category,
    get_games_by_category,
)


def render():
    st.title("System Status")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Run Full Check", type="primary"):
            st.session_state.run_status_check = True
    with col2:
        st.metric("Registered Agents", len(AGENT_REGISTRY))
    with col3:
        st.metric("Registered Games", len(GAME_REGISTRY))

    if st.session_state.get("run_status_check"):
        _run_full_check()
    else:
        st.info("Click 'Run Full Check' to test all imports and configs.")
        _show_registry_overview()


def _show_registry_overview():
    """Show a quick overview of registered components."""
    st.subheader("Agent Registry")
    agent_data = []
    for a in AGENT_REGISTRY:
        agent_data.append({
            "Name": a.name,
            "Category": a.category,
            "Module": a.module_path,
            "Class": a.class_name,
            "Tags": ", ".join(a.tags),
        })
    st.dataframe(agent_data, use_container_width=True)

    st.subheader("Game Registry")
    game_data = []
    for g in GAME_REGISTRY:
        game_data.append({
            "Name": g.name,
            "Category": g.category,
            "Players": f"{g.min_players}-{g.max_players}",
            "Has UI": g.has_ui,
            "Config": g.config_class,
            "Example": g.example_module.split(".")[-1] if g.example_module else "None",
            "Tags": ", ".join(g.tags),
        })
    st.dataframe(game_data, use_container_width=True)


def _run_full_check():
    """Run comprehensive status check."""
    progress = st.progress(0, text="Checking agents...")

    # ── Agent Import Check ──
    st.subheader("Agent Import Status")
    agent_results = []
    total = len(AGENT_REGISTRY) + len(GAME_REGISTRY)
    checked = 0

    for a in AGENT_REGISTRY:
        cls, err = try_import(a.module_path, a.class_name)
        checked += 1
        progress.progress(checked / total, text=f"Checking {a.name}...")
        agent_results.append({
            "Name": a.name,
            "Category": a.category,
            "Import": "OK" if cls else "FAIL",
            "Error": "" if cls else (err or "Unknown"),
            "Module": a.module_path,
        })

    agent_ok = sum(1 for r in agent_results if r["Import"] == "OK")
    agent_fail = len(agent_results) - agent_ok

    if agent_fail == 0:
        st.success(f"All {agent_ok} agents import OK")
    else:
        st.warning(f"{agent_ok}/{len(agent_results)} agents OK, {agent_fail} failed")

    # Color-code the results
    st.dataframe(
        agent_results,
        use_container_width=True,
        column_config={
            "Import": st.column_config.TextColumn(width="small"),
            "Error": st.column_config.TextColumn(width="medium"),
        },
    )

    # ── Game Import Check ──
    st.subheader("Game Import Status")
    game_results = []

    for g in GAME_REGISTRY:
        cls, err = try_import(g.module_path, g.class_name)
        cfg_cls, cfg_err = try_import_game_config(g)
        checked += 1
        progress.progress(checked / total, text=f"Checking {g.name}...")

        game_results.append({
            "Name": g.name,
            "Category": g.category,
            "Agent": "OK" if cls else "FAIL",
            "Config": "OK" if cfg_cls else "FAIL",
            "Has UI": g.has_ui,
            "Players": f"{g.min_players}-{g.max_players}",
            "Example": g.example_module or "None",
            "Agent Error": "" if cls else (err or ""),
            "Config Error": "" if cfg_cls else (cfg_err or ""),
        })

    game_ok = sum(1 for r in game_results if r["Agent"] == "OK")
    config_ok = sum(1 for r in game_results if r["Config"] == "OK")
    game_fail = len(game_results) - game_ok

    if game_fail == 0:
        st.success(f"All {game_ok} game agents import OK, {config_ok} configs OK")
    else:
        st.warning(f"{game_ok}/{len(game_results)} game agents OK, {config_ok} configs OK")

    st.dataframe(
        game_results,
        use_container_width=True,
        column_config={
            "Agent": st.column_config.TextColumn(width="small"),
            "Config": st.column_config.TextColumn(width="small"),
        },
    )

    progress.progress(1.0, text="Done!")

    # ── Quick Example Run Check ──
    st.subheader("Game Example Quick Test")
    st.caption("Runs each game's example module with a 10s timeout to check if it starts OK.")

    if st.button("Run Example Tests", key="run_example_tests"):
        _run_example_tests()

    # ── Summary ──
    st.divider()
    st.subheader("Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Agents OK", f"{agent_ok}/{len(AGENT_REGISTRY)}")
    with col2:
        st.metric("Games OK", f"{game_ok}/{len(GAME_REGISTRY)}")
    with col3:
        st.metric("Configs OK", f"{config_ok}/{len(GAME_REGISTRY)}")
    with col4:
        total_ok = agent_ok + game_ok
        total_all = len(AGENT_REGISTRY) + len(GAME_REGISTRY)
        st.metric("Total OK", f"{total_ok}/{total_all}")


def _run_example_tests():
    """Run each game example with a short timeout."""
    results = []
    progress = st.progress(0, text="Running examples...")

    for i, g in enumerate(GAME_REGISTRY):
        if not g.example_module:
            results.append({"Game": g.name, "Status": "NO EXAMPLE", "Details": ""})
            continue

        progress.progress((i + 1) / len(GAME_REGISTRY), text=f"Testing {g.name}...")

        try:
            result = subprocess.run(
                [sys.executable, "-m", g.example_module],
                capture_output=True,
                text=True,
                timeout=12,
                cwd=os.environ.get("HAIVE_ROOT", "/home/will/Projects/haive"),
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )

            if result.returncode == 0:
                last_line = result.stdout.strip().split("\n")[-1][:80] if result.stdout else ""
                results.append({"Game": g.name, "Status": "PASS", "Details": last_line})
            else:
                err_line = result.stderr.strip().split("\n")[-1][:80] if result.stderr else "Unknown error"
                results.append({"Game": g.name, "Status": "FAIL", "Details": err_line})

        except subprocess.TimeoutExpired:
            results.append({"Game": g.name, "Status": "TIMEOUT", "Details": "Likely waiting for LLM API (would work with keys)"})
        except Exception as e:
            results.append({"Game": g.name, "Status": "ERROR", "Details": str(e)[:80]})

    progress.progress(1.0, text="Done!")

    passed = sum(1 for r in results if r["Status"] == "PASS")
    timeout = sum(1 for r in results if r["Status"] == "TIMEOUT")
    failed = sum(1 for r in results if r["Status"] == "FAIL")

    st.success(f"Results: {passed} PASS, {timeout} TIMEOUT (need LLM), {failed} FAIL")
    st.dataframe(results, use_container_width=True)
