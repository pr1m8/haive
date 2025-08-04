"""Screenshot Documentation Script for Sphinx/Local Webapps.

Features:
- Rich UI logging and colored error/warning reporting.
- Handles scrolling, element-by-element screenshots (headers, sections).
- Hides sticky navbars for clarity.
- Works with any list of URLs, saving screenshots in timestamped runs.
- Robust timeout and error handling (skips invisible elements, logs all issues).
- Easily extensible: Add click/JS/scrolling for menus, themes, sidebars, etc.
- Structure: deep docstrings and comments for maintainability.
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path

from playwright.async_api import (
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.theme import Theme

# ------------------ Configuration ------------------

# List your doc URLs here:
URLS: list[str] = [
    "http://localhost:8003/index.html",
    "http://localhost:8003/agents/react/index.html",
    "http://localhost:8003/agents/demos/index.html",
    "http://localhost:8003/api/index.html",
    "http://localhost:8003/api/src/haive/core/common/index.html",
    "http://localhost:8003/api/src/haive/core/graph/branches/index.html",
    "http://localhost:8003/tools/index.html",
    "http://localhost:8003/games/chess/index.html",
    "http://localhost:8003/agents/demos/simple-demo.html",
]

SCREENSHOT_ROOT: Path = Path("docs/site/screenshots")
SCROLL_STEPS: int = 4  # How many scrolls per page (higher = more slices)
HEADERS_TO_CAPTURE: str = "h1, h2, h3, h4"  # CSS selectors

# ------------------- Rich Console Setup -------------------

console = Console(
    theme=Theme(
        {
            "progress.percentage": "bold green",
            "error": "bold red",
            "warn": "bold yellow",
            "action": "bold blue",
            "success": "bold green",
        },
    ),
)

# ------------------ Screenshot Utilities ------------------


def make_outdir(root: Path) -> Path:
    """Create a timestamped output directory for screenshots."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = root / ts
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir


async def try_click(page, selector: str, desc: str = "", timeout: int = 3000) -> bool:
    """Attempt to click an element, log result."""
    try:
        await page.click(selector, timeout=timeout)
        console.log(f"[action]Clicked {desc or selector}")
        return True
    except PlaywrightTimeoutError:
        console.log(f"[warn]Timeout clicking {desc or selector}[/warn]")
    except Exception as e:
        console.log(f"[error]Could not click {desc or selector}: {e}[/error]")
    return False


async def scroll_and_screenshot(page, save_dir: Path, url: str, scroll_steps: int = 3):
    """Scroll through a page in segments, taking screenshots at each step."""
    page_height = await page.evaluate("() => document.body.scrollHeight")
    for step in range(scroll_steps):
        y = int(page_height * step / max(1, scroll_steps - 1))
        await page.evaluate(f"window.scrollTo(0, {y})")
        await page.wait_for_timeout(400)
        fname = save_dir / f"screenshot_{step:02}.png"
        await page.screenshot(path=fname, full_page=False)
        console.log(f"[success]Saved page segment {step + 1}/{scroll_steps} to {fname}")


async def screenshot_headers(page, save_dir: Path, selector: str):
    """Screenshot all visible headers matching the selector."""
    headers = await page.query_selector_all(selector)
    for idx, h in enumerate(headers, 1):
        try:
            if not await h.is_visible():
                console.log(f"[warn]Header {idx} not visible, skipping[/warn]")
                continue
            await h.scroll_into_view_if_needed(timeout=2000)
            await page.wait_for_timeout(100)
            fname = save_dir / f"header_{idx:02}.png"
            await h.screenshot(path=fname)
            console.log(f"[success]Saved header {idx} to {fname}")
        except PlaywrightTimeoutError:
            console.log(f"[error]Timeout screenshotting header {idx}[/error]")
        except Exception as e:
            console.log(f"[error]Failed to screenshot header {idx}: {e}[/error]")


async def hide_sticky_navbars(page):
    """Hide common sticky/fixed navbars and headers to make screenshots.

    clearer.
    """
    await page.evaluate(
        """
        () => {
            for (const sel of ['header', '.navbar', '.sticky', '.site-header']) {
                document.querySelectorAll(sel).forEach(e => e.style.display = 'none');
            }
        }
    """,
    )
    await page.wait_for_timeout(100)


async def handle_page(
    page,
    url: str,
    outdir: Path,
    scroll_steps: int,
    headers_selector: str,
):
    """Main logic for screenshotting a single page (with error handling)."""
    page_dir = outdir / url.replace("://", "_").replace("/", "_")
    page_dir.mkdir(parents=True, exist_ok=True)
    try:
        console.rule(f"[action]Visiting {url}", style="blue")
        await page.goto(url, timeout=20000)
        await page.wait_for_load_state("networkidle", timeout=10000)
        await hide_sticky_navbars(page)
        # Example: Try opening sidebar or toggling theme (customize selectors for
        # your site)
        await try_click(page, "label.nav-overlay-icon", "Sidebar Toggle", 2000)
        await try_click(page, "button.theme-toggle", "Theme Toggle", 2000)

        await scroll_and_screenshot(page, page_dir, url, scroll_steps)
        console.log("[action]Screenshotting headers...")
        await screenshot_headers(page, page_dir, headers_selector)
    except Exception as e:
        console.print(Panel(str(e), title=f"[error]Error on {url}[/error]"))
    finally:
        await page.close()


async def screenshot_run(
    urls: list[str],
    outdir: Path,
    scroll_steps: int,
    headers_selector: str,
):
    """Visit each URL, screenshot page sections and headers, save to outdir."""
    async with async_playwright() as play:
        browser = await play.chromium.launch(headless=True)
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=False,
            console=console,
        ) as progress:
            task = progress.add_task("Processing pages...", total=len(urls))
            for url in urls:
                page = await browser.new_page()
                await handle_page(page, url, outdir, scroll_steps, headers_selector)
                progress.advance(task)
        await browser.close()


def main():
    """Entrypoint: Create output dir, run screenshot routine, log all steps."""
    outdir = make_outdir(SCREENSHOT_ROOT)
    console.print(f"[success]────── Saving screenshots to: {outdir} ───────[/success]")
    try:
        asyncio.run(screenshot_run(URLS, outdir, SCROLL_STEPS, HEADERS_TO_CAPTURE))
    except Exception as e:
        console.print(Panel(str(e), title="[error]Fatal error[/error]"))

    console.print(
        "[success]───────────────────────────── All done! ─────────────────────────────[/success]",
    )


# ------------- CLI Entrypoint -------------

if __name__ == "__main__":
    main()
