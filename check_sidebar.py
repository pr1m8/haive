#!/usr/bin/env python3
"""Quick script to analyze the sidebar structure in built docs."""

import re
from pathlib import Path

from bs4 import BeautifulSoup

# Path to built documentation
build_dir = Path("docs/build/html")
index_file = build_dir / "index.html"

if not index_file.exists():
    exit(1)

# Read and parse the index.html
with open(index_file) as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Find sidebar elements
sidebar = soup.find("div", class_="sidebar-tree")
if not sidebar:
    sidebar = soup.find("nav", class_="sidebar")
    if not sidebar:
        sidebar = soup.find(class_="toctree-wrapper")


if sidebar:
    # Find all links in sidebar
    links = sidebar.find_all("a", class_="reference")


    # Analyze problematic links
    problematic = []
    for i, link in enumerate(links[:20]):  # First 20 links
        text = link.get_text(strip=True)
        href = link.get("href", "no-href")

        # Check for issues
        issues = []
        if len(text) > 50:
            issues.append("TOO_LONG")
        if "." in text and not text.endswith("."):
            issues.append("SENTENCE")
        if text.startswith(("guides/", "api/")):
            issues.append("PATH_AS_TITLE")
        if not text or text.isspace():
            issues.append("EMPTY")

        if issues:
            problematic.append((text, href, issues))

        status = "❌" if issues else "✅"
        if issues:

    if problematic:
        for text, href, issues in problematic[:5]:
            # Suggest a better title
            if href and href != "no-href":
                suggested = href.replace(".html", "").replace("/", " > ")
                suggested = suggested.replace("_", " ").title()
else:
    pass")

# Check for toctree warnings in the page
warnings = soup.find_all(text=re.compile(r"toctree.*no link will be generated"))
if warnings:
    passML")

# Check what CSS/JS files are loaded
css_files = soup.find_all("link", rel="stylesheet")
js_files = soup.find_all("script", src=True)

for css in css_files:
    href = css.get("href", "")
    if "_static" in href:
        pass

for js in js_files:
    src = js.get("src", "")
    if "_static" in src:
        pass
