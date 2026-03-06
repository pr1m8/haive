"""Demos page - run and view all demo scripts."""

import subprocess
import sys
import os

import streamlit as st


DEMO_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "demos")
# Resolve to absolute path relative to the haive root
HAIVE_ROOT = os.environ.get("HAIVE_ROOT", os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))


def _find_demos() -> dict[str, list[dict]]:
    """Find all demo scripts organized by category."""
    demos_path = os.path.join(HAIVE_ROOT, "demos")
    if not os.path.isdir(demos_path):
        return {}

    result = {}
    for category in sorted(os.listdir(demos_path)):
        cat_path = os.path.join(demos_path, category)
        if not os.path.isdir(cat_path) or category.startswith("_"):
            continue

        scripts = []
        for f in sorted(os.listdir(cat_path)):
            if f.endswith(".py") and not f.startswith("_"):
                scripts.append({
                    "name": f.replace(".py", "").replace("_", " ").title(),
                    "file": f,
                    "path": os.path.join(cat_path, f),
                })
        if scripts:
            result[category] = scripts

    return result


def render():
    st.title("Demos")

    demos = _find_demos()

    if not demos:
        st.warning(f"No demos found. Set HAIVE_ROOT env var or check {HAIVE_ROOT}/demos/")
        return

    # Run all button
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Run All Demos", type="primary"):
            _run_all(demos)

    with col2:
        st.caption(f"Found {sum(len(v) for v in demos.values())} demos across {len(demos)} categories")

    st.divider()

    # Per-category view
    for category, scripts in demos.items():
        st.subheader(f"{category.title()} ({len(scripts)} demos)")

        for script in scripts:
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown(f"**{script['name']}**")
                st.caption(script["file"])

            with col2:
                if st.button("Run", key=f"run_{script['file']}"):
                    _run_demo(script)

            with col3:
                if st.button("View", key=f"view_{script['file']}"):
                    _view_demo(script)


def _run_demo(script: dict):
    """Run a single demo script."""
    with st.spinner(f"Running {script['name']}..."):
        try:
            result = subprocess.run(
                [sys.executable, script["path"]],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=HAIVE_ROOT,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )

            if result.returncode == 0:
                st.success(f"{script['name']} passed")
            else:
                st.error(f"{script['name']} failed (exit {result.returncode})")

            if result.stdout:
                with st.expander("Output"):
                    # Show last 50 lines
                    lines = result.stdout.strip().split("\n")
                    st.code("\n".join(lines[-50:]))

            if result.stderr and result.returncode != 0:
                with st.expander("Errors"):
                    st.code(result.stderr[-2000:])

        except subprocess.TimeoutExpired:
            st.error(f"{script['name']} timed out (120s)")
        except Exception as e:
            st.error(f"Error: {e}")


def _view_demo(script: dict):
    """View a demo script source."""
    try:
        with open(script["path"]) as f:
            source = f.read()
        st.code(source, language="python", line_numbers=True)
    except Exception as e:
        st.error(f"Cannot read: {e}")


def _run_all(demos: dict[str, list[dict]]):
    """Run all demos and show results."""
    total = sum(len(v) for v in demos.values())
    progress = st.progress(0)
    results = []
    ran = 0

    for category, scripts in demos.items():
        for script in scripts:
            ran += 1
            progress.progress(ran / total)

            try:
                result = subprocess.run(
                    [sys.executable, script["path"]],
                    capture_output=True,
                    text=True,
                    timeout=120,
                    cwd=HAIVE_ROOT,
                )
                status = "PASS" if result.returncode == 0 else "FAIL"
            except subprocess.TimeoutExpired:
                status = "TIMEOUT"
            except Exception:
                status = "ERROR"

            results.append({
                "Category": category,
                "Demo": script["name"],
                "Status": status,
            })

    # Show results table
    passed = sum(1 for r in results if r["Status"] == "PASS")
    st.subheader(f"Results: {passed}/{total} passed")
    st.dataframe(results, use_container_width=True)
