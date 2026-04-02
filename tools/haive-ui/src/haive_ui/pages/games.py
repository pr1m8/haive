"""Games page - browse and run games with individual detail pages."""

import asyncio
import os
import re
import subprocess
import sys
import time
import inspect
import traceback

import streamlit as st

from haive_ui.utils.registry import (
    GAME_REGISTRY,
    GameInfo,
    get_games_by_category,
    try_import,
    try_import_game_config,
)
from haive_ui.utils.tracer import TraceCollector


HAIVE_ROOT = os.environ.get("HAIVE_ROOT", "/home/will/Projects/haive")


def render():
    # Initialize tracer
    if "tracer" not in st.session_state:
        st.session_state.tracer = TraceCollector()

    # Check if user selected a specific game
    selected = st.session_state.get("selected_game")

    if selected is not None:
        _render_game_detail(GAME_REGISTRY[selected])
    else:
        _render_game_list()


# -- Game List View (Browse All) ------------------------------------------

def _render_game_list():
    st.title("Games")
    st.caption(f"{len(GAME_REGISTRY)} games across {len(get_games_by_category())} categories")

    # Search
    search = st.text_input("Search games", "", key="game_search_main")

    # Render by category
    for cat, games in get_games_by_category().items():
        filtered = [
            g for g in games
            if not search or search.lower() in g.name.lower() or search.lower() in g.description.lower()
        ]
        if not filtered:
            continue

        st.subheader(f"{cat.replace('_', ' ').title()} ({len(filtered)})")
        rows = [filtered[i:i + 3] for i in range(0, len(filtered), 3)]
        for row in rows:
            cols = st.columns(3)
            for col, game_info in zip(cols, row):
                with col:
                    _render_game_tile(game_info)
        st.divider()


def _render_game_tile(g: GameInfo):
    """Render a clickable tile for a game."""
    idx = GAME_REGISTRY.index(g)
    cls, err = try_import(g.module_path, g.class_name)

    with st.container(border=True):
        st.markdown(f"**{g.name}**")
        st.caption(g.description[:80] if g.description else "")
        st.caption(f"Players: {g.min_players}-{g.max_players}")
        tags_str = " ".join(f"`{t}`" for t in g.tags[:3]) if g.tags else ""
        if tags_str:
            st.markdown(tags_str)

        col_s, col_b = st.columns([1, 1])
        with col_s:
            if cls:
                st.success("OK", icon=None)
            else:
                st.error("FAIL", icon=None)
        with col_b:
            if st.button("Open", key=f"open_game_{idx}", type="primary"):
                st.session_state.selected_game = idx
                st.rerun()


# -- Game Detail Page -----------------------------------------------------

def _render_game_detail(g: GameInfo):
    """Full detail page for a single game."""
    idx = GAME_REGISTRY.index(g)

    # Back button
    if st.button("< Back to Games", key="back_games"):
        st.session_state.selected_game = None
        st.rerun()

    st.title(g.name)
    st.caption(f"Category: **{g.category}** | Module: `{g.module_path}`")

    # Import status
    cls, err = try_import(g.module_path, g.class_name)
    cfg_cls, cfg_err = try_import_game_config(g)

    # Top info bar
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if cls:
            st.success("Agent: OK")
        else:
            st.error("Agent: FAIL")
    with col2:
        if cfg_cls:
            st.success("Config: OK")
        else:
            st.warning("Config: N/A" if "No config" in (cfg_err or "") else f"Config: FAIL")
    with col3:
        st.info(f"Players: {g.min_players}-{g.max_players}")
    with col4:
        st.info(f"Has UI: {'Yes' if g.has_ui else 'No'}")
    with col5:
        llm_cfg = st.session_state.llm_config
        st.info(f"LLM: {llm_cfg['model']}")

    if err:
        st.error(f"Import error: {err}")

    # Tabs
    tab_play, tab_info, tab_run, tab_source, tab_config = st.tabs(["Play", "Info", "Run Example", "Example Source", "Config"])

    with tab_play:
        _render_play_tab(g, cls, cfg_cls)

    with tab_info:
        _render_game_info(g, cls, cfg_cls)

    with tab_run:
        _render_game_run(g, cls)

    with tab_source:
        _render_game_source(g)

    with tab_config:
        _render_game_config_tab(g, cfg_cls)


def _render_game_info(g: GameInfo, cls, cfg_cls):
    """Show detailed info about the game."""
    st.subheader("Description")
    st.markdown(g.description)

    # Import code
    st.subheader("Imports")
    st.code(f"from {g.module_path} import {g.class_name}", language="python")
    if g.config_module and g.config_class:
        st.code(f"from {g.config_module} import {g.config_class}", language="python")

    # Tags
    if g.tags:
        st.subheader("Tags")
        st.markdown(" ".join(f"`{t}`" for t in g.tags))

    # Docstring
    if cls and cls.__doc__:
        import inspect
        st.subheader("Documentation")
        st.markdown(inspect.cleandoc(cls.__doc__))

    # Class details
    if cls:
        st.subheader("Class Details")
        bases = [b.__name__ for b in cls.__mro__[1:4] if b.__name__ != "object"]
        st.markdown(f"**Class:** `{cls.__name__}`")
        if bases:
            st.markdown(f"**Inherits:** {' > '.join(bases)}")
        key_methods = [m for m in ["run_game", "play", "run", "arun", "invoke"] if hasattr(cls, m)]
        if key_methods:
            st.markdown("**Key Methods:** " + ", ".join(f"`{m}()`" for m in key_methods))

    # Quick usage example
    st.subheader("Quick Start")
    if g.config_module and g.config_class:
        st.code(f"""from {g.config_module} import {g.config_class}
from {g.module_path} import {g.class_name}

config = {g.config_class}()
agent = {g.class_name}(config)
# agent.run_game()  # or use the example module
""", language="python")
    else:
        st.code(f"""from {g.module_path} import {g.class_name}

agent = {g.class_name}()
# Run the game
""", language="python")

    if g.example_module:
        st.caption(f"Example: `python -m {g.example_module}`")


def _render_game_run(g: GameInfo, cls):
    """Run the game example."""
    st.subheader("Run Game")

    llm_cfg = st.session_state.llm_config
    st.caption(f"Using: {llm_cfg['provider']}/{llm_cfg['model']} (temp={llm_cfg['temperature']}) -- change in sidebar")

    if not g.example_module:
        st.warning("No example module configured for this game.")
        return

    st.markdown(f"**Example module:** `{g.example_module}`")

    # Run options
    timeout = st.slider("Timeout (seconds)", 15, 300, 120, key=f"timeout_{g.name}")

    col1, col2 = st.columns(2)
    with col1:
        run_btn = st.button("Run Game Example", type="primary", key=f"run_{g.name}")
    with col2:
        test_btn = st.button("Test Create Agent", key=f"test_create_{g.name}")

    if test_btn:
        _test_create_game_agent(g, cls)

    if run_btn:
        _run_game_example(g, timeout)

    # Show cached result
    cached = st.session_state.get(f"game_result_{g.name}")
    if cached:
        st.divider()
        st.subheader("Last Run Results")
        if cached["status"] == "success":
            st.success(f"Completed in {cached['duration']:.1f}s")
        elif cached["status"] == "timeout":
            st.warning(f"Timed out after {timeout}s (game was running, likely waiting for LLM)")
        else:
            st.error(f"Failed (exit {cached.get('returncode', '?')})")

        if cached.get("key_results"):
            st.markdown("**Key Results:**")
            for line in cached["key_results"]:
                st.markdown(f"- {line}")

        if cached.get("output"):
            with st.expander("Full Output", expanded=False):
                st.code(cached["output"])


def _test_create_game_agent(g: GameInfo, cls):
    """Test creating a game agent (no actual game play)."""
    with st.spinner("Creating game agent..."):
        try:
            cfg_cls, _ = try_import_game_config(g)
            if cfg_cls:
                # Try with analysis/visualize disabled, fall back to defaults
                try:
                    config = cfg_cls(enable_analysis=False, visualize=False)
                except Exception:
                    try:
                        config = cfg_cls(visualize=False)
                    except Exception:
                        config = cfg_cls()
                agent = cls(config)
            else:
                agent = cls()

            st.success(f"Agent created: `{type(agent).__name__}`")

            # Show details
            if hasattr(agent, "app") and agent.app is not None:
                st.caption("Graph compiled: Yes")
            if hasattr(agent, "runnable_config"):
                rc = agent.runnable_config or {}
                rl = rc.get("recursion_limit", "default")
                st.caption(f"Recursion limit: {rl}")

        except Exception as e:
            st.error(f"Failed: {e}")
            with st.expander("Full traceback"):
                st.code(traceback.format_exc())


def _run_game_example(g: GameInfo, timeout: int):
    """Run a game's example module via subprocess."""
    tracer: TraceCollector = st.session_state.tracer
    trace = tracer.start_trace(f"Game: {g.name}")
    tracer.log("input", g.name, f"Running example: {g.example_module}")

    with st.spinner(f"Running {g.name}... (timeout: {timeout}s)"):
        try:
            result = subprocess.run(
                [sys.executable, "-m", g.example_module],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=HAIVE_ROOT,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )

            ansi_escape = re.compile(r'\x1b\[[0-9;]*m')

            if result.returncode == 0:
                st.success(f"{g.name} completed successfully")
                tracer.log("output", g.name, "Completed successfully")
                tracer.end_trace("completed")
            else:
                st.error(f"{g.name} failed (exit {result.returncode})")
                tracer.log("error", g.name, result.stderr[-500:] if result.stderr else "Unknown error")
                tracer.end_trace("error")

            # Process output
            if result.stdout:
                stdout_lines = result.stdout.strip().split("\n")
                clean_lines = [ansi_escape.sub('', line).strip() for line in stdout_lines]

                # Find key results
                key_results = [
                    l for l in clean_lines
                    if any(kw in l.lower() for kw in
                           ["completed", "winner", "result", "game over", "final", "score", "pass", "fail"])
                    and l.strip()
                ]

                # Cache result
                st.session_state[f"game_result_{g.name}"] = {
                    "status": "success" if result.returncode == 0 else "fail",
                    "returncode": result.returncode,
                    "duration": 0,  # subprocess doesn't track this easily
                    "output": "\n".join(clean_lines[-200:]),
                    "key_results": key_results[-5:],
                }

                # Show results inline
                if key_results:
                    st.subheader("Key Results")
                    for line in key_results[-5:]:
                        st.markdown(f"- {line}")

                with st.expander("Full Output", expanded=True):
                    st.code("\n".join(clean_lines[-200:]))

            if result.stderr and result.returncode != 0:
                with st.expander("Errors"):
                    clean_stderr = ansi_escape.sub('', result.stderr[-3000:])
                    st.code(clean_stderr)

        except subprocess.TimeoutExpired:
            st.warning(f"{g.name} timed out after {timeout}s (game was running, likely waiting for LLM API)")
            st.info("This means the game starts successfully but needs LLM API calls to complete.")
            tracer.log("output", g.name, f"Timed out after {timeout}s (game was running)")
            tracer.end_trace("completed")

            st.session_state[f"game_result_{g.name}"] = {
                "status": "timeout",
                "output": "",
                "key_results": [],
            }

        except Exception as e:
            st.error(f"Error: {e}")
            tracer.log("error", g.name, str(e))
            tracer.end_trace("error")
            with st.expander("Traceback"):
                st.code(traceback.format_exc())


def _render_game_source(g: GameInfo):
    """Show the example source code."""
    st.subheader("Example Source")

    if not g.example_module:
        st.info("No example module configured for this game.")
        return

    st.caption(f"Module: `{g.example_module}`")

    try:
        mod = __import__(g.example_module, fromlist=["__file__"])
        if hasattr(mod, "__file__") and mod.__file__:
            with open(mod.__file__) as f:
                st.code(f.read(), language="python", line_numbers=True)
        else:
            st.info("No source file found")
    except Exception as e:
        st.error(f"Cannot load source: {e}")
        with st.expander("Details"):
            st.code(traceback.format_exc())


def _render_game_config_tab(g: GameInfo, cfg_cls):
    """Show game configuration details."""
    st.subheader("Game Configuration")

    if not cfg_cls:
        st.info("No config class available for this game.")
        return

    st.code(f"from {g.config_module} import {g.config_class}", language="python")

    # Show config fields
    try:
        import inspect
        if cfg_cls.__doc__:
            st.markdown(inspect.cleandoc(cfg_cls.__doc__))

        # Try to show fields from Pydantic model
        if hasattr(cfg_cls, "model_fields"):
            st.subheader("Config Fields")
            for name, field_info in cfg_cls.model_fields.items():
                default = field_info.default
                if default is not None:
                    st.markdown(f"- **{name}**: `{default}` ({field_info.annotation.__name__ if hasattr(field_info.annotation, '__name__') else str(field_info.annotation)})")
                else:
                    st.markdown(f"- **{name}**: *required*")

        # Show source
        source_file = inspect.getfile(cfg_cls)
        st.caption(f"File: `{source_file}`")
        with st.expander("Config Source"):
            with open(source_file) as f:
                st.code(f.read(), language="python", line_numbers=True)

    except Exception as e:
        st.warning(f"Could not inspect config: {e}")


# -- Play Tab (Interactive Game) ---------------------------------------------

def _render_play_tab(g: GameInfo, cls, cfg_cls):
    """Interactive game play with LLM agents and live board rendering."""
    st.subheader("Play Game")

    if not cls:
        st.error("Cannot play - agent class failed to import.")
        return

    llm_cfg = st.session_state.llm_config
    st.caption(f"LLM: **{llm_cfg['model']}** | Temp: {llm_cfg['temperature']}")

    game_key = f"live_game_{g.name}"

    # Initialize or get game state
    col_start, col_reset = st.columns([1, 1])
    with col_start:
        start_btn = st.button("Start New Game", type="primary", key=f"start_{g.name}")
    with col_reset:
        reset_btn = st.button("Reset", key=f"reset_{g.name}")

    if reset_btn:
        st.session_state.pop(game_key, None)
        st.session_state.pop(f"{game_key}_log", None)
        st.rerun()

    if start_btn:
        with st.spinner("Creating game agent and compiling graph..."):
            try:
                agent, state = _create_game(g, cls, cfg_cls)
                st.session_state[game_key] = {"agent": agent, "state": state, "step": 0, "done": False}
                st.session_state[f"{game_key}_log"] = []
                st.success("Game created! Click 'Next Move' to play.")
            except Exception as e:
                st.error(f"Failed to create game: {e}")
                with st.expander("Details"):
                    st.code(traceback.format_exc())
                return

    game_data = st.session_state.get(game_key)
    if not game_data:
        st.info("Click **Start New Game** to begin.")
        return

    agent = game_data["agent"]
    state = game_data["state"]
    step = game_data["step"]
    done = game_data["done"]

    # Render game board
    _render_game_board(g, state)

    # Game status
    game_status = _get_game_status(state)
    if game_status:
        st.markdown(f"**Status:** {game_status}")

    # Move log
    move_log = st.session_state.get(f"{game_key}_log", [])

    if not done:
        move_btn = st.button("Next Move", type="primary", key=f"move_{g.name}_{step}")
        auto_play = st.checkbox("Auto-play (run full game)", key=f"auto_{g.name}")

        if move_btn or auto_play:
            _play_move(g, game_key, agent, state, move_log, auto_play)
    else:
        st.success("Game Over!")
        winner = getattr(state, "winner", None)
        if winner:
            st.markdown(f"### Winner: **{winner}**")

    # Show move history
    if move_log:
        with st.expander(f"Move History ({len(move_log)} moves)", expanded=False):
            for entry in move_log:
                st.markdown(f"- {entry}")


def _create_game(g: GameInfo, cls, cfg_cls):
    """Create a game agent and initial state."""
    if cfg_cls:
        try:
            config = cfg_cls(enable_analysis=False, visualize=False)
        except Exception:
            try:
                config = cfg_cls(visualize=False)
            except Exception:
                config = cfg_cls()
        agent = cls(config)
    else:
        agent = cls()

    # Get initial state
    state_module = g.module_path.rsplit(".", 1)[0] + ".state"
    try:
        import importlib
        sm = importlib.import_module(state_module)
        # Find the state class
        state_cls = None
        for name in dir(sm):
            obj = getattr(sm, name)
            if isinstance(obj, type) and name.endswith("State") and name != "BaseModel":
                state_cls = obj
                break
        if state_cls:
            state = state_cls()
        else:
            state = {}
    except Exception:
        state = {}

    # Try to initialize the game
    if hasattr(agent, "initialize_game"):
        try:
            state = agent.initialize_game(state)
        except Exception:
            pass

    return agent, state


def _render_game_board(g: GameInfo, state):
    """Render the game board based on game type."""
    game_name = g.name.lower().replace(" ", "_").replace("'", "")

    # TicTacToe
    if "tic_tac" in game_name:
        board = getattr(state, "board", None)
        if board:
            st.markdown("#### Board")
            for r, row in enumerate(board):
                cols = st.columns(3)
                for c, cell in enumerate(row):
                    with cols[c]:
                        val = cell if cell else "."
                        if val == "X":
                            st.markdown(f"<div style='text-align:center;font-size:2em;color:#e74c3c'>X</div>", unsafe_allow_html=True)
                        elif val == "O":
                            st.markdown(f"<div style='text-align:center;font-size:2em;color:#3498db'>O</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div style='text-align:center;font-size:2em;color:#ccc'>.</div>", unsafe_allow_html=True)

    # Chess
    elif "chess" in game_name:
        board = getattr(state, "board", None) or getattr(state, "board_state", None)
        if board:
            st.markdown("#### Board")
            if isinstance(board, str):
                st.code(board, language=None)
            elif isinstance(board, list):
                board_str = ""
                for row in board:
                    if isinstance(row, list):
                        board_str += " ".join(str(c) if c else "." for c in row) + "\n"
                    else:
                        board_str += str(row) + "\n"
                st.code(board_str, language=None)

    # Connect4
    elif "connect" in game_name:
        board = getattr(state, "board", None)
        if board:
            st.markdown("#### Board")
            for row in board:
                cols = st.columns(7)
                for c, cell in enumerate(row):
                    with cols[c]:
                        if cell == 1:
                            st.markdown("<div style='text-align:center;font-size:1.5em'>🔴</div>", unsafe_allow_html=True)
                        elif cell == 2:
                            st.markdown("<div style='text-align:center;font-size:1.5em'>🟡</div>", unsafe_allow_html=True)
                        else:
                            st.markdown("<div style='text-align:center;font-size:1.5em'>⚪</div>", unsafe_allow_html=True)

    # Nim
    elif "nim" in game_name:
        heaps = getattr(state, "heaps", None) or getattr(state, "board", None)
        if heaps and isinstance(heaps, list):
            st.markdown("#### Heaps")
            for i, h in enumerate(heaps):
                count = h if isinstance(h, int) else 0
                st.markdown(f"Pile {i+1}: {'🪨 ' * count} ({count})")

    # Reversi
    elif "reversi" in game_name:
        board = getattr(state, "board", None)
        if board:
            st.markdown("#### Board")
            board_str = ""
            for row in board:
                if isinstance(row, list):
                    for cell in row:
                        if cell == 1:
                            board_str += "⚫ "
                        elif cell == 2:
                            board_str += "⚪ "
                        else:
                            board_str += "· "
                    board_str += "\n"
            st.code(board_str, language=None)

    # Fallback: show state as JSON
    else:
        _render_generic_state(state)


def _render_generic_state(state):
    """Render game state as formatted info."""
    if isinstance(state, dict):
        display = {k: v for k, v in state.items() if k != "messages" and not k.startswith("_")}
        if display:
            st.json(display)
        return

    # Pydantic/dataclass state
    display = {}
    for attr in ["board", "board_state", "turn", "current_player", "game_status",
                 "winner", "score", "scores", "round", "phase", "heaps",
                 "move_history", "players", "hands", "pot", "community_cards"]:
        val = getattr(state, attr, None)
        if val is not None:
            if isinstance(val, list) and len(val) > 20:
                display[attr] = f"[{len(val)} items]"
            else:
                display[attr] = val

    if display:
        st.markdown("#### Game State")
        for k, v in display.items():
            if isinstance(v, list) and all(isinstance(r, list) for r in v):
                # Board-like
                board_str = "\n".join(" ".join(str(c) if c else "." for c in row) for row in v)
                st.markdown(f"**{k}:**")
                st.code(board_str, language=None)
            else:
                st.markdown(f"**{k}:** {v}")
    else:
        st.caption("No displayable state yet. Start the game and make a move.")


def _get_game_status(state) -> str:
    """Extract game status string."""
    status = getattr(state, "game_status", None)
    if status:
        return str(status)
    turn = getattr(state, "turn", None) or getattr(state, "current_player", None)
    if turn:
        return f"Turn: {turn}"
    return ""


def _play_move(g: GameInfo, game_key: str, agent, state, move_log: list, auto_play: bool):
    """Execute one or more game moves using the LLM agent."""
    max_moves = 50 if auto_play else 1

    for i in range(max_moves):
        # Check if game is over
        game_status = getattr(state, "game_status", "")
        if game_status and any(end in str(game_status).lower() for end in ["over", "finished", "complete", "won", "draw", "tie"]):
            st.session_state[game_key]["done"] = True
            break

        winner = getattr(state, "winner", None)
        if winner:
            st.session_state[game_key]["done"] = True
            break

        step = st.session_state[game_key]["step"]
        with st.spinner(f"Move {step + 1}... (LLM thinking)"):
            try:
                # Run the game agent for one step
                if hasattr(agent, "app") and agent.app is not None:
                    state_dict = state if isinstance(state, dict) else (
                        state.model_dump() if hasattr(state, "model_dump") else vars(state)
                    )
                    result = agent.app.invoke(state_dict)

                    # Update state from result
                    if isinstance(result, dict):
                        if hasattr(state, "model_validate"):
                            try:
                                state = state.__class__.model_validate(result)
                            except Exception:
                                state = result
                        else:
                            state = result
                    else:
                        state = result

                    # Log the move
                    move_hist = getattr(state, "move_history", None)
                    if move_hist and isinstance(move_hist, list) and len(move_hist) > step:
                        last_move = move_hist[-1]
                        move_log.append(f"Move {step+1}: {last_move}")
                    else:
                        turn = getattr(state, "turn", "?")
                        move_log.append(f"Move {step+1}: (turn={turn})")

                    st.session_state[game_key]["state"] = state
                    st.session_state[game_key]["step"] = step + 1
                    st.session_state[f"{game_key}_log"] = move_log

                else:
                    st.warning("Game agent has no compiled graph (app). Try 'Run Example' tab instead.")
                    return

            except Exception as e:
                err_msg = str(e)[:200]
                move_log.append(f"Move {step+1}: ERROR - {err_msg}")
                st.session_state[f"{game_key}_log"] = move_log
                st.error(f"Move failed: {err_msg}")
                with st.expander("Details"):
                    st.code(traceback.format_exc())
                return

    st.rerun()
