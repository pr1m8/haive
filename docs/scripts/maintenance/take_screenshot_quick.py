#!/usr/bin/env python3
"""Quick screenshot tool for documentation testing."""

import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright


async def take_screenshot(url: str, output_path: str):
    """Take a screenshot of the given URL."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)  # Extra wait for dynamic content

        await page.screenshot(path=output_path, full_page=True)
        await browser.close()

        print(f"✅ Screenshot saved to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python take_screenshot_quick.py <url> <output_path>")
        sys.exit(1)

    asyncio.run(take_screenshot(sys.argv[1], sys.argv[2]))
