#!/usr/bin/env python3
"""Screenshot documentation to verify CSS fixes are working."""

import asyncio

from playwright.async_api import async_playwright


async def screenshot_docs():
    """Take screenshots of key documentation pages to verify fixes."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Set viewport for consistent screenshots
        await page.set_viewport_size({"width": 1200, "height": 800})

        pages_to_test = [
            ("index", "http://localhost:8003/", "Main homepage"),
            (
                "introduction",
                "http://localhost:8003/introduction/",
                "Introduction page",
            ),
            ("agents", "http://localhost:8003/agents/", "Agents overview"),
            ("games", "http://localhost:8003/games/", "Games section"),
            ("api_core", "http://localhost:8003/api/haive.core.html", "Core API docs"),
            ("search", "http://localhost:8003/search.html", "Search functionality"),
        ]


        for page_name, url, description in pages_to_test:
            try:

                # Navigate with timeout
                await page.goto(url, wait_until="networkidle", timeout=10000)

                # Wait a moment for any dynamic content
                await page.wait_for_timeout(1000)

                # Take screenshot
                screenshot_path = f"docs_screenshot_{page_name}_fixed.png"
                await page.screenshot(path=screenshot_path, full_page=True)

                # Check basic page structure
                title = await page.title()

                # Check if Furo theme is working (look for sidebar)
                sidebar = await page.query_selector(".furo-sidebar")
                if sidebar:
                    pass")
                else:
                    passes")

                # Check for CSS loading
                stylesheets = await page.evaluate(
                    """
                    Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
                        .map(link => link.href.split('/').pop())
                        .filter(name => name.includes('furo') || name.includes('haive'))
                """
                )

                # Verify haive-minimal.css is NOT loaded
                has_minimal = any("haive-minimal" in css for css in stylesheets)
                if has_minimal:
                    pass")
                else:
                    pass")


            except Exception as e:
                pass")

        await browser.close()



if __name__ == "__main__":
    asyncio.run(screenshot_docs())
