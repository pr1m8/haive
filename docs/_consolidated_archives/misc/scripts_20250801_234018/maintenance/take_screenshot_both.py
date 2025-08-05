#!/usr/bin/env python3
"""Screenshot tool that captures both full viewport and half-width views."""

import asyncio
import sys

from playwright.async_api import async_playwright


async def take_screenshots(url: str, output_base: str):
    """Take screenshots at different viewport sizes."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Full screen (1920x1080)
        page_full = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page_full.goto(url)
        await page_full.wait_for_load_state("networkidle")
        await asyncio.sleep(2)

        output_full = output_base.replace(".png", "_full.png")
        await page_full.screenshot(path=output_full, full_page=False)

        # Half width (960x1080) - shows centering issues better
        page_half = await browser.new_page(viewport={"width": 960, "height": 1080})
        await page_half.goto(url)
        await page_half.wait_for_load_state("networkidle")
        await asyncio.sleep(2)

        output_half = output_base.replace(".png", "_half.png")
        await page_half.screenshot(path=output_half, full_page=False)

        # Mobile view (375x812) - iPhone X size
        page_mobile = await browser.new_page(viewport={"width": 375, "height": 812})
        await page_mobile.goto(url)
        await page_mobile.wait_for_load_state("networkidle")
        await asyncio.sleep(2)

        output_mobile = output_base.replace(".png", "_mobile.png")
        await page_mobile.screenshot(path=output_mobile, full_page=False)

        await browser.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)

    asyncio.run(take_screenshots(sys.argv[1], sys.argv[2]))
