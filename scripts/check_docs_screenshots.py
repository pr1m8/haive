#!/usr/bin/env python3
"""Take screenshots of documentation pages to check CSS fixes."""

import asyncio
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright


async def take_screenshots():
    """Take screenshots of key documentation pages."""
    # Create screenshots directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshots_dir = Path(f"docs/screenshots/css_fixes_{timestamp}")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    urls_to_check = [
        ("http://localhost:8004/", "index"),
        ("http://localhost:8004/agents/index.html", "agents_index"),
        ("http://localhost:8004/games/index.html", "games_index"),
        ("http://localhost:8004/gallery.html", "gallery"),
        ("http://localhost:8004/api/index.html", "api_index"),
        ("http://localhost:8004/examples/index.html", "examples_index"),
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Take screenshots at different viewport sizes
        viewports = [
            {"width": 1920, "height": 1080, "name": "desktop"},
            {"width": 768, "height": 1024, "name": "tablet"},
            {"width": 375, "height": 812, "name": "mobile"},
        ]

        for viewport in viewports:
            context = await browser.new_context(
                viewport={"width": viewport["width"], "height": viewport["height"]},
                device_scale_factor=2,  # High DPI screenshots
            )
            page = await context.new_page()

            for url, name in urls_to_check:
                try:
                    # Navigate to page
                    await page.goto(url, wait_until="networkidle")

                    # Wait for content to load
                    await page.wait_for_timeout(2000)

                    # Scroll to load all lazy content
                    await page.evaluate(
                        "window.scrollTo(0, document.body.scrollHeight)",
                    )
                    await page.wait_for_timeout(1000)
                    await page.evaluate("window.scrollTo(0, 0)")

                    # Take full page screenshot
                    screenshot_path = (
                        screenshots_dir / f"{name}_{viewport['name']}_full.png"
                    )
                    await page.screenshot(path=str(screenshot_path), full_page=True)

                    # Take viewport screenshot
                    screenshot_path = (
                        screenshots_dir / f"{name}_{viewport['name']}_viewport.png"
                    )
                    await page.screenshot(path=str(screenshot_path))

                    # Take specific element screenshots if they exist
                    elements_to_capture = [
                        (".sd-card", "card"),
                        (".sidebar-tree", "sidebar"),
                        (".highlight", "code_block"),
                        (".hero-section", "hero"),
                        (".furo-content", "content"),
                    ]

                    for selector, element_name in elements_to_capture:
                        try:
                            element = await page.query_selector(selector)
                            if element:
                                screenshot_path = (
                                    screenshots_dir
                                    / f"{name}_{viewport['name']}_{element_name}.png"
                                )
                                await element.screenshot(path=str(screenshot_path))
                        except Exception:
                            pass

                except Exception:
                    pass

            await context.close()

        await browser.close()


if __name__ == "__main__":
    asyncio.run(take_screenshots())
